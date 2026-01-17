/// DOSYA ADI: home_screen.dart
/// AMAÇ: Uygulama açılış akışını yönetmek.
/// NE YAPAR:
///   - Oturum kontrolü yapar.
///   - Giriş veya sohbet ekranına yönlendirir.
/// BAĞIMLILIKLAR:
///   - appwrite_service.dart: oturum kontrolü
/// SON DEĞİŞİKLİK: 17.01.2026
library;

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/auth/login_screen.dart';
import 'package:selcukaiassistant/screen/feature/new_chat_screen.dart';
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

    // Oturum durumunu kontrol edip yönlendir.
    WidgetsBinding.instance.addPostFrameCallback((_) async {
      await _checkAuthAndNavigate();
    });
  }

  Future<void> _checkAuthAndNavigate() async {
    try {
      // Appwrite servisi kontrolü
      // Eğer yapılandırılmamışsa giriş ekranına yönlendir.
      if (_appwriteService.account == null) {
        if (mounted) {
          // Appwrite yoksa giriş ekranına git.
          unawaited(Get.off<void>(() => const LoginScreen()));
        }
        return;
      }

      final user = await _appwriteService.getCurrentUser();

      if (mounted) {
        if (user != null) {
          // Kullanıcı giriş yaptıysa sohbet ekranına git.
          unawaited(Get.off<void>(() => const NewChatScreen()));
        } else {
          // Aktif oturum yoksa giriş ekranına git.
          unawaited(Get.off<void>(() => const LoginScreen()));
        }
      }
    } on Exception {
      // Oturum kontrolünde hata oluştuysa giriş ekranına git.
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
