import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:selcukaiassistant/apis/apis.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';
import 'package:selcukaiassistant/model/message.dart';
import 'package:speech_to_text/speech_to_text.dart';

class ChatController extends GetxController {
  final textC = TextEditingController();
  final scrollC = ScrollController();

  final SpeechToText _speechToText = SpeechToText();
  final RxBool isListening = false.obs;
  final RxBool speechEnabled = false.obs;
  final RxString recognizedText = ''.obs;

  final RxList<Message> list = <Message>[
    Message(
      msg: 'Merhaba! Ben bir yapay zeka asistanıyım, '
          'size nasıl yardımcı olabilirim?',
      msgType: MessageType.bot,
    ),
  ].obs;

  @override
  void onInit() {
    super.onInit();
    unawaited(_initSpeech());
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
        'Ses girişi özelliğini kullanmak için '
        'mikrofon izni gereklidir',
      );
      return;
    }

    if (!speechEnabled.value) {
      MyDialog.info('Ses tanıma kullanılamıyor');
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
        localeId: 'tr_TR',
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
    if (textC.text.trim().isNotEmpty) {
      list
        ..add(Message(msg: textC.text, msgType: MessageType.user))
        ..add(Message(msg: '', msgType: MessageType.bot));
      _scrollDown();

      final question = textC.text;
      textC.text = '';

      try {
        final res = await APIs.getAnswer(question);

        // AI response
        list
          ..removeLast()
          ..add(Message(msg: res, msgType: MessageType.bot));
        _scrollDown();
      } on Exception {
        list
          ..removeLast()
          ..add(
            Message(
              msg: 'Üzgünüz, bir şeyler ters gitti, '
                  'lütfen daha sonra tekrar deneyin.',
              msgType: MessageType.bot,
            ),
          );
        _scrollDown();
      }
    } else {
      MyDialog.info(
        'Lütfen bir soru girin veya sesli girişi kullanın！',
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
