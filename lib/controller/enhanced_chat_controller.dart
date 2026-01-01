import 'dart:async';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:selcukaiassistant/apis/apis.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/services/conversation_export_service.dart';
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
      return 'You are a helpful assistant for Selçuk University. '
          'Reply in English. Do not reveal reasoning or internal thoughts. '
          'If the user greets vaguely (e.g. "Hello"), ask what they need about '
          'Selçuk University.';
    }
    return 'Sel\u00e7uk \u00dcniversitesi i\u00e7in yard\u0131mc\u0131 bir '
        'asistans\u0131n. Yan\u0131tlar\u0131n\u0131 T\u00fcrk\u00e7e ver. '
        'Ak\u0131l y\u00fcr\u00fctme veya i\u00e7 konu\u015fma '
        'payla\u015fma. Kullan\u0131c\u0131 genel bir selam verirse '
        '(\u00f6r. "Merhaba"), Sel\u00e7uk \u00dcniversitesi ile ilgili '
        'neye ihtiya\u00e7 duydu\u011funu sor.';
  }

  Future<void> _initializeConversation() async {
    await ConversationService.init();

    final conversations = ConversationService.getActiveConversations();
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
    if (!Pref.voiceInputEnabled) {
      MyDialog.info(
        l10n?.voiceInputSubtitle ??
            'Sesli mesajlar için mikrofonu etkinleştirin.',
      );
      return;
    }
    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      MyDialog.info(
        l10n?.microphonePermissionRequired ??
            'Sesli giriş için mikrofon izni gereklidir.',
      );
      return;
    }

    if (!speechEnabled.value) {
      MyDialog.info(
        l10n?.speechNotAvailable ?? 'Ses tanıma kullanılamıyor.',
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

  Future<void> sendMessage({
    String? imageUrl,
    String? overrideText,
    String? parentMessageId,
  }) async {
    final l10n = L10n.current();
    final rawText = overrideText ?? textC.text;
    final messageText = rawText.trim();
    if (messageText.isEmpty) {
      MyDialog.info(
        l10n?.enterMessagePrompt ??
            'Lütfen bir mesaj yazın ya da sesli giriş kullanın!',
      );
      return;
    }

    final userMessage = ChatMessage(
      id: _uuid.v4(),
      content: messageText,
      isUser: true,
      createdAt: DateTime.now(),
      imageUrl: imageUrl,
      parentMessageId: parentMessageId,
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
      createdAt: DateTime.now(),
    );
    messages.add(aiMessage);
    _scrollDown();

    if (overrideText == null) {
      textC.clear();
    }
    isGenerating.value = true;
    _stopRequested = false;
    aiMessage
      ..error = null
      ..errorCode = null;

    final payloadMessages = _buildPayloadMessages();
    // Model seçimi - geçersiz model varsa null gönder (backend varsayılanı kullanır)
    String? selectedModel = Pref.selectedModel;
    if (selectedModel == 'selcuk_ai_assistant') {
      // Eski model ismi - backend'de artık yok, null gönder
      selectedModel = null;
      Pref.selectedModel = null; // Tercih temizle
    }

    try {
      await _streamResponse(
        payloadMessages,
        aiMessage,
        model: selectedModel,
      );

      if (!_stopRequested) {
        aiMessage
          ..error = null
          ..errorCode = null;
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
      aiMessage
        ..error = e.toString()
        ..errorCode = 'stream_error';
      if (aiMessage.content.isEmpty) {
        final fallback = await APIs.sendChat(
          messages: payloadMessages,
          model: selectedModel,
        );
        aiMessage
          ..content = ResponseCleaner.clean(fallback.answer)
          ..citations = fallback.citations;
      } else {
        aiMessage.content +=
            "\n\n${l10n?.streamInterruptedTag ?? '[Akış kesildi]'}";
      }
      messages.refresh();
      await ConversationService.addMessage(
        currentConversationId.value,
        aiMessage,
      );
      Get.snackbar(
        l10n?.streamErrorTitle ?? 'Akış hatası',
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

  List<Map<String, String>> _buildPayloadMessages({
    int? lastMessageIndex,
  }) {
    final limitIndex =
        lastMessageIndex ?? (messages.isEmpty ? -1 : messages.length - 1);
    final slice =
        limitIndex >= 0 ? messages.sublist(0, limitIndex + 1) : <ChatMessage>[];
    final history =
        slice.where((msg) => msg.content.trim().isNotEmpty).toList();

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

  ChatMessage _cloneMessage(ChatMessage message) {
    return ChatMessage(
      id: _uuid.v4(),
      content: message.content,
      isUser: message.isUser,
      createdAt: message.createdAt,
      imageUrl: message.imageUrl,
      role: message.role,
      provider: message.provider,
      modelId: message.modelId,
      error: message.error,
      errorCode: message.errorCode,
      parentMessageId: message.parentMessageId,
      citations: List<String>.from(message.citations),
    );
  }

  int? _findPreviousUserIndex(int fromIndex) {
    for (var i = fromIndex - 1; i >= 0; i--) {
      if (messages[i].isUser) {
        return i;
      }
    }
    return null;
  }

  Future<void> editLastUserMessage(ChatMessage message) async {
    if (isGenerating.value) {
      return;
    }

    final lastUserIndex = messages.lastIndexWhere((m) => m.isUser);
    final messageIndex = messages.indexOf(message);
    if (messageIndex == -1 || messageIndex != lastUserIndex) {
      return;
    }

    final l10n = L10n.current();
    final controller = TextEditingController(text: message.content);

    final updated = await Get.dialog<String>(
      AlertDialog(
        title: Text(l10n?.editMessageTitle ?? 'Mesajı düzenle'),
        content: TextField(
          controller: controller,
          autofocus: true,
          maxLines: null,
          decoration: InputDecoration(
            hintText: l10n?.editMessageHint ?? 'Mesajınızı güncelleyin',
            border: const OutlineInputBorder(),
          ),
          onSubmitted: (value) => Get.back(result: value),
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back<String>(),
            child: Text(l10n?.cancel ?? 'İptal'),
          ),
          TextButton(
            onPressed: () => Get.back<String>(result: controller.text),
            child: Text(l10n?.editMessageAction ?? 'Yeniden gönder'),
          ),
        ],
      ),
    );

    controller.dispose();

    final trimmed = updated?.trim();
    if (trimmed == null ||
        trimmed.isEmpty ||
        trimmed == message.content.trim()) {
      return;
    }

    final newConversation = await ConversationService.createConversation();
    final history = messages.take(messageIndex).map(_cloneMessage).toList();

    await ConversationService.setMessages(newConversation.id, history);
    newConversation
      ..title = ConversationService.generateTitle(trimmed)
      ..updatedAt = DateTime.now();
    await newConversation.save();

    currentConversation.value = newConversation;
    currentConversationId.value = newConversation.id;
    messages.value = List.from(history);
    _scrollDown();

    await sendMessage(
      overrideText: trimmed,
      parentMessageId: message.id,
    );
  }

  Future<void> regenerateResponse(ChatMessage message) async {
    if (isGenerating.value || message.isUser) {
      return;
    }

    final lastAssistantIndex = messages.lastIndexWhere((msg) => !msg.isUser);
    final messageIndex = messages.indexOf(message);
    if (messageIndex == -1 || messageIndex != lastAssistantIndex) {
      return;
    }

    final userIndex = _findPreviousUserIndex(messageIndex);
    if (userIndex == null) {
      return;
    }

    message
      ..content = ''
      ..error = null
      ..errorCode = null
      ..citations = []
      ..createdAt = DateTime.now();
    messages.refresh();

    final l10n = L10n.current();
    isGenerating.value = true;
    _stopRequested = false;

    final payloadMessages = _buildPayloadMessages(lastMessageIndex: userIndex);
    final selectedModel = Pref.selectedModel;

    String? errorMessage;
    String? errorCode;
    List<String>? citations;

    try {
      await _streamResponse(
        payloadMessages,
        message,
        model: selectedModel,
      );
      citations = message.citations;
    } on Exception catch (e) {
      if (!_stopRequested) {
        errorMessage = e.toString();
        errorCode = 'stream_error';
        message
          ..error = errorMessage
          ..errorCode = errorCode;
        messages.refresh();
        Get.snackbar(
          l10n?.streamErrorTitle ?? 'Akış hatası',
          e.toString(),
          snackPosition: SnackPosition.BOTTOM,
          backgroundColor: Colors.red,
          colorText: Colors.white,
        );
      }
    } finally {
      await ConversationService.updateMessage(
        currentConversationId.value,
        message.id,
        newContent: message.content,
        error: errorMessage ?? '',
        errorCode: errorCode ?? '',
        citations: citations,
      );
      isGenerating.value = false;
      _stopRequested = false;
      _scrollDown();
    }
  }

  Future<void> retryResponse(ChatMessage message) async {
    await regenerateResponse(message);
  }

  Future<void> _streamResponse(
    List<Map<String, String>> messagesPayload,
    ChatMessage aiMessage, {
    String? model,
  }) async {
    final cleaner = ResponseCleaner();
    const updateInterval = Duration(milliseconds: 50);
    var lastUpdate = DateTime.fromMillisecondsSinceEpoch(0);
    _streamSession = await APIs.streamChat(
      messages: messagesPayload,
      model: model,
    );

    final completer = Completer<void>();
    _streamSubscription = _streamSession!.stream.listen(
      (ChatStreamEvent event) {
        if (event.type == 'token' && event.token != null) {
          aiMessage.content = cleaner.push(event.token!);
          final now = DateTime.now();
          if (now.difference(lastUpdate) >= updateInterval) {
            messages.refresh();
            _scrollDown();
            lastUpdate = now;
          }
        } else if (event.type == 'end') {
          aiMessage.content = cleaner.finalize();
          if (event.citations != null) {
            aiMessage.citations = event.citations!;
          }
          messages.refresh();
          _scrollDown();
          if (!completer.isCompleted) {
            completer.complete();
          }
        } else if (event.type == 'error') {
          if (!completer.isCompleted) {
            completer.completeError(event.message ?? 'Akış hatası');
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
        title: Text(l10n?.clearConversationTitle ?? 'Sohbeti temizle'),
        content: Text(
          l10n?.clearConversationMessage ??
              'Bu sohbeti temizlemek istediğinize emin misiniz? '
                  'Bu işlem geri alınamaz.',
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: false),
            child: Text(l10n?.cancel ?? 'İptal'),
          ),
          TextButton(
            onPressed: () => Get.back(result: true),
            child: Text(
              l10n?.clear ?? 'Temizle',
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
          l10n?.exportFailedTitle ?? 'Dışa aktarma başarısız',
          l10n?.noMessagesToExport ?? 'Dışa aktarılacak mesaj yok',
          snackPosition: SnackPosition.BOTTOM,
        );
        return;
      }

      final jsonData = ConversationService.exportConversation(conversation.id);
      final jsonString = const JsonEncoder.withIndent('  ').convert(jsonData);

      final filename = 'chat_${conversation.id.substring(0, 8)}.json';
      final result = await exportConversation(filename, jsonString);

      await Clipboard.setData(ClipboardData(text: jsonString));

      final successMessage = result.path != null
          ? l10n?.exportSuccessMessage(result.path!) ??
              'Dosyaya kaydedildi: ${result.path}\nAyrıca panoya kopyalandı'
          : l10n?.exportSuccessWebMessage ??
              'Dosya indirildi ve panoya kopyalandı';

      Get.snackbar(
        l10n?.exportSuccessTitle ?? 'Dışa aktarma başarılı',
        successMessage,
        snackPosition: SnackPosition.BOTTOM,
        duration: const Duration(seconds: 4),
      );
    } on Exception catch (e) {
      Get.snackbar(
        l10n?.exportFailedTitle ?? 'Dışa aktarma başarısız',
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
