// ════════════════════════════════════════════════════════════════════
// DOSYA ADI: splash_screen.dart
// AMAÇ: Uygulama açılış ekranı (splash screen)
// KULLANIM: main.dart'tan ilk açılan ekran
// İLGİLİ EKRANLAR: OnboardingScreen, HomeScreen
// YAZAN: esN2k - Selçuk Üniversitesi
// ════════════════════════════════════════════════════════════════════
//
// DETAYLI AÇIKLAMA:
// Bu ekran, uygulama açıldığında 2 saniye gösterilen karşılama
// ekranıdır. Logo ve yükleme göstergesi içerir.
//
// AKIŞ:
// 1. Uygulama açılır → SplashScreen görünür
// 2. 2 saniye beklenir
// 3. İlk kullanımsa → OnboardingScreen'e yönlendir
// 4. Değilse → HomeScreen'e yönlendir
//
// ÖRNEK KULLANIM:
// home: const SplashScreen(),
// ════════════════════════════════════════════════════════════════════

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/screen/home_screen.dart';
import 'package:selcukaiassistant/screen/onboarding_screen.dart';
import 'package:selcukaiassistant/widget/custom_loading.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    // wait for some time on splash & then move to next screen
    Future.delayed(const Duration(seconds: 2), () {
      unawaited(
        Get.off<Widget>(
          () => Pref.showOnboarding
              ? const OnboardingScreen()
              : const HomeScreen(),
        ),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    // initializing device size
    Global.mq = MediaQuery.sizeOf(context);
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final maxLogoSize = Global.mq.width * 0.3; // Daha küçük logo

    return Scaffold(
      backgroundColor: Theme.of(context).scaffoldBackgroundColor,
      body: SafeArea(
        child: Center(
          child: SingleChildScrollView(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 40),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Container(
                    padding: const EdgeInsets.all(20),
                    decoration: BoxDecoration(
                      color: isDark
                          ? Theme.of(context).colorScheme.surface
                          : Colors.white,
                      borderRadius: BorderRadius.circular(24),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black
                              .withValues(alpha: isDark ? 0.4 : 0.08),
                          blurRadius: 24,
                          offset: const Offset(0, 12),
                        ),
                      ],
                    ),
                    child: Image.asset(
                      'assets/branding/selcuk_seal.jpg',
                      width: maxLogoSize,
                      height: maxLogoSize,
                      fit: BoxFit.contain,
                    ),
                  ),
                  const SizedBox(height: 24),
                  Text(
                    context.l10n.splashSubtitle,
                    textAlign: TextAlign.center,
                    style: Theme.of(context).textTheme.titleMedium?.copyWith(
                          fontWeight: FontWeight.w600,
                          color: Theme.of(context).colorScheme.onSurface,
                        ),
                  ),
                  const SizedBox(height: 40),
                  const CustomLoading(),
                  const SizedBox(height: 40),
                ],
              ),
            ),
          ),
        ),
      ),
    );
  }
}
