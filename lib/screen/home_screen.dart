import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/auth/login_screen.dart';
import 'package:selcukaiassistant/screen/feature/chatbot_feature.dart';
import 'package:selcukaiassistant/services/appwrite_service.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _appwriteService = AppwriteService();

  @override
  void initState() {
    super.initState();
    unawaited(SystemChrome.setEnabledSystemUIMode(SystemUiMode.edgeToEdge));
    Pref.showOnboarding = false;

    // Check auth status and navigate
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await _checkAuthAndNavigate();
    });
  }

  Future<void> _checkAuthAndNavigate() async {
    try {
      final user = await _appwriteService.getCurrentUser();

      if (mounted) {
        if (user != null) {
          // User is logged in, go to chat
          unawaited(Get.off<void>(() => const ChatBotFeature()));
        } else {
          // No active session, go to login
          unawaited(Get.off<void>(() => const LoginScreen()));
        }
      }
    } on Exception {
      // Error checking session, go to login
      if (mounted) {
        unawaited(Get.off<void>(() => const LoginScreen()));
      }
    }
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
