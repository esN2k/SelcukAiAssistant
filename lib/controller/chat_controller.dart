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
        msg: l10n?.startChatHint ?? 'Yapay zeka asistanıyla sohbete başlayın!',
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
              msg: l10n?.errorUnexpected ??
                  'Hata: Beklenmeyen bir hata oluştu.',
              msgType: MessageType.bot,
            ),
          );
        _scrollDown();
      }
    } else {
      MyDialog.info(
        l10n?.enterMessagePrompt ??
            'Lütfen bir mesaj yazın ya da sesli giriş kullanın!',
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
