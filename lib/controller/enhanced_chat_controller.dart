import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:http/http.dart' as http;
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';
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
  bool _shouldStopGeneration = false;

  @override
  void onInit() {
    super.onInit();
    unawaited(_initSpeech());
    unawaited(_initializeConversation());
  }

  Future<void> _initializeConversation() async {
    await ConversationService.init();

    // Get or create the first conversation
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
    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      MyDialog.info(
        'Microphone permission is required for voice input',
      );
      return;
    }

    if (!speechEnabled.value) {
      MyDialog.info('Speech recognition is not available');
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
        localeId: 'en_US', // Changed to English
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
    _shouldStopGeneration = true;
    isGenerating.value = false;
  }

  Future<void> sendMessage({String? imageUrl}) async {
    if (textC.text.trim().isEmpty) {
      MyDialog.info('Please enter a message or use voice input!');
      return;
    }

    final userMessage = ChatMessage(
      id: _uuid.v4(),
      content: textC.text.trim(),
      isUser: true,
      timestamp: DateTime.now(),
      imageUrl: imageUrl,
    );

    // Add user message
    messages.add(userMessage);
    await ConversationService.addMessage(
      currentConversationId.value,
      userMessage,
    );

    // Create placeholder for AI response
    final aiMessage = ChatMessage(
      id: _uuid.v4(),
      content: '',
      isUser: false,
      timestamp: DateTime.now(),
    );
    messages.add(aiMessage);

    _scrollDown();

    final question = textC.text;
    textC.clear();

    // Start generation
    isGenerating.value = true;
    _shouldStopGeneration = false;

    try {
      await _streamResponse(question, aiMessage);

      if (!_shouldStopGeneration) {
        // Save the complete AI response
        await ConversationService.addMessage(
          currentConversationId.value,
          aiMessage,
        );
      } else {
        // If stopped, update with partial response
        messages.removeLast();
        if (aiMessage.content.isNotEmpty) {
          messages.add(aiMessage);
          await ConversationService.addMessage(
            currentConversationId.value,
            aiMessage,
          );
        }
      }
    } on Exception catch (e) {
      messages.removeLast();
      final errorMessage = ChatMessage(
        id: _uuid.v4(),
        content: 'Sorry, something went wrong: $e',
        isUser: false,
        timestamp: DateTime.now(),
      );
      messages.add(errorMessage);
      await ConversationService.addMessage(
        currentConversationId.value,
        errorMessage,
      );
    } finally {
      isGenerating.value = false;
      _shouldStopGeneration = false;
      _scrollDown();
    }
  }

  Future<void> _streamResponse(String question, ChatMessage aiMessage) async {
    try {
      final response = await http.post(
        Uri.parse(Global.chatEndpoint),
        headers: {'Content-Type': 'application/json; charset=utf-8'},
        body: jsonEncode({'question': question}),
      );

      if (response.statusCode == 200) {
        final responseData =
            jsonDecode(utf8.decode(response.bodyBytes)) as Map<String, dynamic>;
        final answer = (responseData['answer'] as String?) ??
            'Sorry, no response generated.';

        // Simulate streaming by revealing text gradually
        var currentIndex = 0;
        const chunkSize = 5; // Characters per update
        const delayMs = 20; // Milliseconds between updates

        while (currentIndex < answer.length && !_shouldStopGeneration) {
          final endIndex = (currentIndex + chunkSize).clamp(0, answer.length);
          aiMessage.content = answer.substring(0, endIndex);

          // Trigger UI update
          messages.refresh();
          _scrollDown();

          if (endIndex < answer.length) {
            await Future<void>.delayed(const Duration(milliseconds: delayMs));
          }

          currentIndex = endIndex;
        }
      } else {
        aiMessage.content =
            'Error: Server returned status ${response.statusCode}';
        messages.refresh();
      }
    } on Exception catch (e) {
      aiMessage.content = 'Error: $e';
      messages.refresh();
    }
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
    final confirmed = await Get.dialog<bool>(
      AlertDialog(
        title: const Text('Clear Conversation'),
        content: const Text(
          'Are you sure you want to clear this conversation? '
          'This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Get.back(result: true),
            child: const Text('Clear', style: TextStyle(color: Colors.red)),
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
    try {
      final conversation = currentConversation.value;
      if (conversation == null || conversation.messages.isEmpty) {
        Get.snackbar(
          'Export Failed',
          'No messages to export',
          snackPosition: SnackPosition.BOTTOM,
        );
        return;
      }

      final jsonData = ConversationService.exportConversation(conversation.id);
      final jsonString = const JsonEncoder.withIndent('  ').convert(jsonData);

      // Save to downloads directory
      final directory = await getApplicationDocumentsDirectory();
      final file = File(
        '${directory.path}/chat_${conversation.id.substring(0, 8)}.json',
      );
      await file.writeAsString(jsonString);

      // Copy to clipboard
      await Clipboard.setData(ClipboardData(text: jsonString));

      Get.snackbar(
        'Export Successful',
        'Saved to ${file.path}\nAlso copied to clipboard',
        snackPosition: SnackPosition.BOTTOM,
        duration: const Duration(seconds: 4),
      );
    } on Exception catch (e) {
      Get.snackbar(
        'Export Failed',
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
    super.onClose();
  }
}
