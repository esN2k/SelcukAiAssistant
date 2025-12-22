import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:selcukaiassistant/apis/apis.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';
import 'package:selcukaiassistant/services/response_cleaner.dart';
import 'package:selcukaiassistant/services/sse_client.dart';
import 'package:speech_to_text/speech_to_text.dart';
import 'package:uuid/uuid.dart';

class EnhancedChatController extends GetxController {
  final textC = TextEditingController();
  final scrollC = ScrollController();

  final SpeechToText _speechToText = SpeechToText();
  final RxBool isListening = false.obs;
  final RxBool speechEnabled = false.obs;
  final RxBool isGenerating = false.obs;

  final RxList<ChatMessage> messages = <ChatMessage>[].obs;
  final Rx<Conversation?> currentConversation = Rx<Conversation?>(null);
  final RxString currentConversationId = ''.obs;

  final _uuid = const Uuid();
  bool _stopRequested = false;
  ChatStreamSession? _streamSession;
  StreamSubscription<ChatStreamEvent>? _streamSubscription;

  @override
  void onInit() {
    super.onInit();
    unawaited(_initSpeech());
    unawaited(_initializeConversation());
  }

  String _languageCode() {
    return Pref.localeCode ?? L10n.fallbackLocale.languageCode;
  }

  String _speechLocaleId() {
    return _languageCode() == 'en' ? 'en_US' : 'tr_TR';
  }

  String _systemPrompt() {
    if (_languageCode() == 'en') {
      return 'You are a helpful assistant for Selcuk University. '
          'Reply in English. Do not reveal reasoning or internal thoughts. '
          'If the user greets vaguely (e.g. "Hello"), ask what they need about '
          'Selcuk University.';
    }
    return 'Sel?uk ?niversitesi i?in yard?mc? bir asistans?n. '
        'Yan?tlar?n? T?rk?e ver. Ak?l y?r?tme veya i? konu?ma payla?ma. '
        'Kullan?c? genel bir selam verirse (?r. "Merhaba"), '
        'Sel?uk ?niversitesi ile ilgili neye ihtiya? duydu?unu sor.';
  }

  Future<void> _initializeConversation() async {
    await ConversationService.init();

    final conversations = ConversationService.getAllConversations();
    if (conversations.isEmpty) {
      final newConversation = await ConversationService.createConversation();
      currentConversation.value = newConversation;
      currentConversationId.value = newConversation.id;
    } else {
      currentConversation.value = conversations.first;
      currentConversationId.value = conversations.first.id;
      messages.value = List.from(conversations.first.messages);
    }
  }

  Future<void> loadConversation(String conversationId) async {
    final conversation = ConversationService.getConversation(conversationId);
    if (conversation != null) {
      currentConversation.value = conversation;
      currentConversationId.value = conversationId;
      messages.value = List.from(conversation.messages);
      _scrollDown();
    }
  }

  Future<void> _initSpeech() async {
    speechEnabled.value = await _speechToText.initialize(
      onError: (error) {
        isListening.value = false;
      },
      onStatus: (status) {
        if (status == 'done' || status == 'notListening') {
          isListening.value = false;
        }
      },
    );
  }

  Future<void> startListening() async {
    final l10n = L10n.current();
    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      MyDialog.info(
        l10n?.microphonePermissionRequired ??
            'Microphone permission is required for voice input',
      );
      return;
    }

    if (!speechEnabled.value) {
      MyDialog.info(
        l10n?.speechNotAvailable ?? 'Speech recognition is not available',
      );
      return;
    }

    if (!isListening.value) {
      isListening.value = true;

      await _speechToText.listen(
        onResult: (result) {
          textC.text = result.recognizedWords;
          if (result.finalResult) {
            isListening.value = false;
          }
        },
        localeId: _speechLocaleId(),
      );
    }
  }

  Future<void> stopListening() async {
    if (isListening.value) {
      await _speechToText.stop();
      isListening.value = false;
    }
  }

  void stopGeneration() {
    _stopRequested = true;
    isGenerating.value = false;
    _cancelStreamSubscription();
    _streamSession?.close();
  }

  Future<void> sendMessage({String? imageUrl}) async {
    final l10n = L10n.current();
    if (textC.text.trim().isEmpty) {
      MyDialog.info(
        l10n?.enterMessagePrompt ??
            'Please enter a message or use voice input!',
      );
      return;
    }

    final userMessage = ChatMessage(
      id: _uuid.v4(),
      content: textC.text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
      imageUrl: imageUrl,
    );

    messages.add(userMessage);
    await ConversationService.addMessage(
      currentConversationId.value,
      userMessage,
    );

    final aiMessage = ChatMessage(
      id: _uuid.v4(),
      content: '',
      isUser: false,
      timestamp: DateTime.now(),
    );
    messages.add(aiMessage);
    _scrollDown();

    textC.clear();
    isGenerating.value = true;
    _stopRequested = false;

    final payloadMessages = _buildPayloadMessages();
    final selectedModel = Pref.selectedModel;

    try {
      await _streamResponse(
        payloadMessages,
        aiMessage,
        model: selectedModel,
      );

      if (!_stopRequested) {
        await ConversationService.addMessage(
          currentConversationId.value,
          aiMessage,
        );
      } else if (aiMessage.content.isNotEmpty) {
        await ConversationService.addMessage(
          currentConversationId.value,
          aiMessage,
        );
      } else {
        messages.remove(aiMessage);
      }
    } on Exception catch (e) {
      if (_stopRequested) {
        return;
      }
      if (aiMessage.content.isEmpty) {
        final fallback = await APIs.sendChat(
          messages: payloadMessages,
          model: selectedModel,
        );
        aiMessage.content = ResponseCleaner.clean(fallback);
      } else {
        aiMessage.content +=
            "\n\n${l10n?.streamInterruptedTag ?? '[Stream interrupted]'}";
      }
      messages.refresh();
      await ConversationService.addMessage(
        currentConversationId.value,
        aiMessage,
      );
      Get.snackbar(
        l10n?.streamErrorTitle ?? 'Stream error',
        e.toString(),
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    } finally {
      isGenerating.value = false;
      _stopRequested = false;
      _scrollDown();
    }
  }

  List<Map<String, String>> _buildPayloadMessages() {
    final history = messages
        .where((msg) => msg.content.trim().isNotEmpty)
        .toList();

    const maxHistory = 20;
    final recent = history.length > maxHistory
        ? history.sublist(history.length - maxHistory)
        : history;

    final payload = <Map<String, String>>[
      {
        'role': 'system',
        'content': _systemPrompt(),
      },
      ...recent.map(
        (msg) => {
          'role': msg.isUser ? 'user' : 'assistant',
          'content': msg.content,
        },
      ),
    ];

    return payload;
  }

  Future<void> _streamResponse(
    List<Map<String, String>> messagesPayload,
    ChatMessage aiMessage, {
    String? model,
  }) async {
    final cleaner = ResponseCleaner();
    _streamSession = await APIs.streamChat(
      messages: messagesPayload,
      model: model,
    );

    final completer = Completer<void>();
    _streamSubscription = _streamSession!.stream.listen(
      (ChatStreamEvent event) {
        if (event.type == 'token' && event.token != null) {
          aiMessage.content = cleaner.push(event.token!);
          messages.refresh();
          _scrollDown();
        } else if (event.type == 'end') {
          aiMessage.content = cleaner.finalize();
          messages.refresh();
          if (!completer.isCompleted) {
            completer.complete();
          }
        } else if (event.type == 'error') {
          if (!completer.isCompleted) {
            completer.completeError(event.message ?? 'Stream error');
          }
        }
      },
      onError: (Object error) {
        if (!completer.isCompleted) {
          completer.completeError(error);
        }
      },
      onDone: () {
        if (!completer.isCompleted) {
          completer.complete();
        }
      },
      cancelOnError: true,
    );

    await completer.future;
    aiMessage.content = cleaner.finalize();
    messages.refresh();
    _streamSession?.close();
  }

  void _scrollDown() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scrollC.hasClients) {
        unawaited(
          scrollC.animateTo(
            scrollC.position.maxScrollExtent,
            duration: const Duration(milliseconds: 300),
            curve: Curves.easeOut,
          ),
        );
      }
    });
  }

  Future<void> clearCurrentConversation() async {
    final l10n = L10n.current();
    final confirmed = await Get.dialog<bool>(
      AlertDialog(
        title: Text(l10n?.clearConversationTitle ?? 'Clear conversation'),
        content: Text(
          l10n?.clearConversationMessage ??
              'Are you sure you want to clear this conversation? '
                  'This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: false),
            child: Text(l10n?.cancel ?? 'Cancel'),
          ),
          TextButton(
            onPressed: () => Get.back(result: true),
            child: Text(
              l10n?.clear ?? 'Clear',
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirmed ?? false) {
      await ConversationService.deleteConversation(currentConversationId.value);
      final newConversation = await ConversationService.createConversation();
      unawaited(loadConversation(newConversation.id));
    }
  }

  Future<void> exportCurrentConversation() async {
    final l10n = L10n.current();
    try {
      final conversation = currentConversation.value;
      if (conversation == null || conversation.messages.isEmpty) {
        Get.snackbar(
          l10n?.exportFailedTitle ?? 'Export failed',
          l10n?.noMessagesToExport ?? 'No messages to export',
          snackPosition: SnackPosition.BOTTOM,
        );
        return;
      }

      final jsonData = ConversationService.exportConversation(conversation.id);
      final jsonString = const JsonEncoder.withIndent('  ').convert(jsonData);

      final directory = await getApplicationDocumentsDirectory();
      final file = File(
        '${directory.path}/chat_${conversation.id.substring(0, 8)}.json',
      );
      await file.writeAsString(jsonString);

      await Clipboard.setData(ClipboardData(text: jsonString));

      Get.snackbar(
        l10n?.exportSuccessTitle ?? 'Export successful',
        l10n?.exportSuccessMessage(file.path) ??
            'Saved to ${file.path}\nAlso copied to clipboard',
        snackPosition: SnackPosition.BOTTOM,
        duration: const Duration(seconds: 4),
      );
    } on Exception catch (e) {
      Get.snackbar(
        l10n?.exportFailedTitle ?? 'Export failed',
        '$e',
        snackPosition: SnackPosition.BOTTOM,
        backgroundColor: Colors.red,
        colorText: Colors.white,
      );
    }
  }

  @override
  void onClose() {
    textC.dispose();
    scrollC.dispose();
    unawaited(_speechToText.cancel());
    _cancelStreamSubscription();
    _streamSession?.close();
    super.onClose();
  }

  void _cancelStreamSubscription() {
    final cancelFuture = _streamSubscription?.cancel();
    if (cancelFuture != null) {
      unawaited(cancelFuture);
    }
  }
}
