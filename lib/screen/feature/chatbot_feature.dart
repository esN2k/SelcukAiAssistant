// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:selcukaiassistant/controller/chat_controller.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/widget/message_card.dart';

class ChatBotFeature extends StatefulWidget {
  const ChatBotFeature({super.key});

  @override
  State<ChatBotFeature> createState() => _ChatBotFeatureState();
}

class _ChatBotFeatureState extends State<ChatBotFeature> {
  final _c = ChatController();
  final RxBool _isDarkMode = Get.isDarkMode.obs;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      // 应用栏
      appBar: AppBar(
        title: const Text('AI 智能助手'),
        centerTitle: true,
        elevation: 1,
        actions: [
          // 主题切换按钮
          IconButton(
            padding: const EdgeInsets.only(right: 10),
            onPressed: () {
              Get.changeThemeMode(
                _isDarkMode.value ? ThemeMode.light : ThemeMode.dark,
              );
              _isDarkMode.value = !_isDarkMode.value;
            },
            icon: Obx(
              () => Icon(
                _isDarkMode.value
                    ? Icons.brightness_2_rounded
                    : Icons.brightness_5_rounded,
                size: 24,
              ),
            ),
          ),
        ],
      ),

      // 输入区域
      bottomNavigationBar: Container(
        padding: EdgeInsets.only(
          left: 16,
          right: 16,
          bottom: MediaQuery.of(context).viewInsets.bottom + 16,
          top: 16,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          border: Border(
            top: BorderSide(
              color: Theme.of(context).dividerColor,
              width: 0.5,
            ),
          ),
        ),
        child: SafeArea(
          child: Row(
            children: [
              // 语音输入按钮
              Obx(
                () => GestureDetector(
                  onTapDown: (_) => _c.startListening(),
                  onTapUp: (_) => _c.stopListening(),
                  onTapCancel: _c.stopListening,
                  child: Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: _c.isListening.value
                          ? Colors.red.withOpacity(0.1)
                          : Colors.blue.withOpacity(0.1),
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: _c.isListening.value ? Colors.red : Colors.blue,
                        width: 2,
                      ),
                    ),
                    child: Icon(
                      _c.isListening.value ? Icons.mic : Icons.mic_none,
                      color: _c.isListening.value ? Colors.red : Colors.blue,
                      size: 24,
                    ),
                  ),
                ),
              ),

              const SizedBox(width: 12),

              // 文本输入框
              Expanded(
                child: Container(
                  decoration: BoxDecoration(
                    color: Theme.of(context).brightness == Brightness.dark
                        ? Colors.grey[800]
                        : Colors.grey[100],
                    borderRadius: BorderRadius.circular(24),
                  ),
                  child: TextFormField(
                    controller: _c.textC,
                    maxLines: null,
                    textInputAction: TextInputAction.send,
                    onFieldSubmitted: (_) => _c.askQuestion(),
                    decoration: InputDecoration(
                      hintText: '输入消息或长按语音输入...',
                      hintStyle: TextStyle(
                        fontSize: 14,
                        color: Theme.of(context)
                            .textTheme
                            .bodyMedium
                            ?.color
                            ?.withOpacity(0.6),
                      ),
                      border: InputBorder.none,
                      contentPadding: const EdgeInsets.symmetric(
                        horizontal: 16,
                        vertical: 12,
                      ),
                    ),
                  ),
                ),
              ),

              const SizedBox(width: 12),

              // 发送按钮
              GestureDetector(
                onTap: _c.askQuestion,
                child: Container(
                  width: 48,
                  height: 48,
                  decoration: const BoxDecoration(
                    color: Colors.blue,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.send_rounded,
                    color: Colors.white,
                    size: 20,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),

      // 消息列表
      body: Obx(
        () => Column(
          children: [
            // 语音识别状态提示
            if (_c.isListening.value)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                color: Colors.red.withOpacity(0.1),
                child: const Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Icon(Icons.mic, color: Colors.red, size: 16),
                    SizedBox(width: 8),
                    Text(
                      '正在听取语音输入...',
                      style: TextStyle(
                        color: Colors.red,
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),

            // 消息列表
            Expanded(
              child: _c.list.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.chat_bubble_outline,
                            size: 64,
                            color: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.color
                                ?.withOpacity(0.3),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            '开始与AI助手对话吧！',
                            style: TextStyle(
                              fontSize: 16,
                              color: Theme.of(context)
                                  .textTheme
                                  .bodyMedium
                                  ?.color
                                  ?.withOpacity(0.6),
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      physics: const BouncingScrollPhysics(),
                      controller: _c.scrollC,
                      padding: EdgeInsets.only(
                        top: mq.height * .02,
                        bottom: 16,
                        left: 8,
                        right: 8,
                      ),
                      itemCount: _c.list.length,
                      itemBuilder: (context, index) {
                        return MessageCard(message: _c.list[index]);
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
