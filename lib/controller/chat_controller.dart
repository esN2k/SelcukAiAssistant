import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:selcukaiassistant/apis/apis.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/message.dart';
import 'package:selcukaiassistant/services/response_cleaner.dart';
import 'package:speech_to_text/speech_to_text.dart';

class ChatController extends GetxController {
  final textC = TextEditingController();
  final scrollC = ScrollController();

  final SpeechToText _speechToText = SpeechToText();
  final RxBool isListening = false.obs;
  final RxBool speechEnabled = false.obs;
  final RxString recognizedText = ''.obs;

  final RxList<Message> list = <Message>[].obs;

  @override
  void onInit() {
    super.onInit();
    _initDefaultMessage();
    unawaited(_initSpeech());
  }

  void _initDefaultMessage() {
    final l10n = L10n.current();
    list.assignAll([
      Message(
        msg: l10n?.startChatHint ?? 'Start chatting with the AI assistant!',
        msgType: MessageType.bot,
      ),
    ]);
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
    return 'Sel\u00e7uk \u00dcniversitesi i\u00e7in yard\u0131mc\u0131 bir '
        'asistans\u0131n. Yan\u0131tlar\u0131n\u0131 T\u00fcrk\u00e7e ver. '
        'Ak\u0131l y\u00fcr\u00fctme veya i\u00e7 konu\u015fma '
        'payla\u015fma. Kullan\u0131c\u0131 genel bir selam verirse '
        '(\u00f6r. "Merhaba"), Sel\u00e7uk \u00dcniversitesi ile ilgili '
        'neye ihtiya\u00e7 duydu\u011funu sor.';
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
      recognizedText.value = '';

      await _speechToText.listen(
        onResult: (result) {
          recognizedText.value = result.recognizedWords;
          if (result.finalResult) {
            textC.text = recognizedText.value;
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

  Future<void> askQuestion() async {
    final l10n = L10n.current();
    if (textC.text.trim().isNotEmpty) {
      list
        ..add(Message(msg: textC.text, msgType: MessageType.user))
        ..add(Message(msg: '', msgType: MessageType.bot));
      _scrollDown();

      final question = textC.text;
      textC.text = '';

      final payload = [
        {'role': 'system', 'content': _systemPrompt()},
        {'role': 'user', 'content': question},
      ];

      try {
        final res = await APIs.sendChat(
          messages: payload,
          model: Pref.selectedModel,
        );

        list
          ..removeLast()
          ..add(
            Message(
              msg: ResponseCleaner.clean(res.answer),
              msgType: MessageType.bot,
            ),
          );
        _scrollDown();
      } on Exception {
        list
          ..removeLast()
          ..add(
            Message(
              msg: l10n?.errorUnexpected ?? 'Error: Unexpected error.',
              msgType: MessageType.bot,
            ),
          );
        _scrollDown();
      }
    } else {
      MyDialog.info(
        l10n?.enterMessagePrompt ??
            'Please enter a message or use voice input!',
      );
    }
  }

  void _scrollDown() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scrollC.hasClients) {
        unawaited(
          scrollC.animateTo(
            scrollC.position.maxScrollExtent,
            duration: const Duration(milliseconds: 500),
            curve: Curves.ease,
          ),
        );
      }
    });
  }

  @override
  void onClose() {
    textC.dispose();
    scrollC.dispose();
    unawaited(_speechToText.cancel());
    super.onClose();
  }
}
