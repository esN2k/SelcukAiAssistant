import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';

import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/feature/chatbot_feature.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  @override
  void initState() {
    super.initState();
    unawaited(SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge));
    Pref.showOnboarding = false;

    // 直接跳转到聊天界面
    WidgetsBinding.instance.addPostFrameCallback((_) {
      unawaited(Get.off<void>(() => const ChatBotFeature()));
    });
  }

  @override
  Widget build(BuildContext context) {
    return const Scaffold(
      body: Center(
        child: CircularProgressIndicator(),
      ),
    );
  }
}
