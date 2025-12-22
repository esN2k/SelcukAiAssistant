import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:selcukaiassistant/screen/feature/new_chat_screen.dart';

enum HomeType { aiChatBot }

extension MyHomeType on HomeType {
  //title
  String get title => switch (this) {
        HomeType.aiChatBot => 'Yapay zeka akıllı diyalog',
      };

  //lottie
  String get lottie => switch (this) {
        HomeType.aiChatBot => 'ai_hand_waving.json',
      };

  //for alignment
  bool get leftAlign => switch (this) {
        HomeType.aiChatBot => true,
      };

  //for padding
  EdgeInsets get padding => switch (this) {
        HomeType.aiChatBot => EdgeInsets.zero,
      };

  //for navigation
  VoidCallback get onTap => switch (this) {
        HomeType.aiChatBot => () => Get.to<void>(() => const NewChatScreen()),
      };
}
