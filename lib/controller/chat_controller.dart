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

  // 语音识别相关
  final SpeechToText _speechToText = SpeechToText();
  final RxBool isListening = false.obs;
  final RxBool speechEnabled = false.obs;
  final RxString recognizedText = ''.obs;

  final RxList<Message> list = <Message>[
    Message(msg: '你好！我是AI助手，有什么可以帮助你的吗？', msgType: MessageType.bot),
  ].obs;

  @override
  void onInit() {
    super.onInit();
    _initSpeech();
  }

  /// 初始化语音识别
  Future<void> _initSpeech() async {
    speechEnabled.value = await _speechToText.initialize(
      onError: (error) {
        // 语音识别错误处理
        isListening.value = false;
      },
      onStatus: (status) {
        // 语音识别状态处理
        if (status == 'done' || status == 'notListening') {
          isListening.value = false;
        }
      },
    );
  }

  /// 开始语音识别
  Future<void> startListening() async {
    // 检查麦克风权限
    final status = await Permission.microphone.request();
    if (status != PermissionStatus.granted) {
      MyDialog.info('需要麦克风权限才能使用语音输入功能');
      return;
    }

    if (!speechEnabled.value) {
      MyDialog.info('语音识别功能不可用');
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
        localeId: 'zh_CN', // 中文识别
      );
    }
  }

  /// 停止语音识别
  Future<void> stopListening() async {
    if (isListening.value) {
      await _speechToText.stop();
      isListening.value = false;
    }
  }

  /// 发送问题
  Future<void> askQuestion() async {
    if (textC.text.trim().isNotEmpty) {
      // 用户消息
      list.add(Message(msg: textC.text, msgType: MessageType.user));
      list.add(Message(msg: '', msgType: MessageType.bot));
      _scrollDown();

      final question = textC.text;
      textC.text = '';

      try {
        final res = await APIs.getAnswer(question);

        // AI回复
        list.removeLast();
        list.add(Message(msg: res, msgType: MessageType.bot));
        _scrollDown();
      } catch (e) {
        list.removeLast();
        list.add(Message(msg: '抱歉，出现了一些问题，请稍后重试。', msgType: MessageType.bot));
        _scrollDown();
      }
    } else {
      MyDialog.info('请输入问题或使用语音输入！');
    }
  }

  /// 滚动到底部
  void _scrollDown() {
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (scrollC.hasClients) {
        scrollC.animateTo(
          scrollC.position.maxScrollExtent,
          duration: const Duration(milliseconds: 500),
          curve: Curves.ease,
        );
      }
    });
  }

  @override
  void onClose() {
    textC.dispose();
    scrollC.dispose();
    _speechToText.cancel();
    super.onClose();
  }
}
