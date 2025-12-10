import 'dart:async';
import 'dart:developer';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/ad_helper.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/splash_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Safely initialize dependencies without blocking the UI indefinitely
  await _initServices();

  runApp(const MyApp());
}

Future<void> _initServices() async {
  try {
    // Initialize preferences with a timeout to prevent hanging
    await Pref.initialize().timeout(
      const Duration(seconds: 1),
      onTimeout: () {
        log('Pref.initialize timed out');
      },
    );
  } catch (e, stack) {
    log('Error initializing Pref: $e\n$stack');
  }

  try {
    // Load environment variables with timeout
    await dotenv.load().timeout(
      const Duration(seconds: 1),
      onTimeout: () {
        log('dotenv.load timed out');
      },
    );
  } catch (e, stack) {
    log('Error loading .env: $e\n$stack');
  }

  // Mobile-only initializations
  if (!kIsWeb) {
    try {
      AdHelper.init();
    } catch (e, stack) {
      log('Error initializing AdHelper: $e\n$stack');
    }

    try {
      await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
      await SystemChrome.setPreferredOrientations(
        [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown],
      );
    } catch (e, stack) {
      log('Error setting system chrome: $e\n$stack');
    }
  }
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: appName,
      debugShowCheckedModeBanner: false,

      themeMode: Pref.defaultTheme,

      //dark
      darkTheme: ThemeData(
        useMaterial3: false,
        brightness: Brightness.dark,
        appBarTheme: const AppBarTheme(
          elevation: 1,
          centerTitle: true,
          titleTextStyle: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
        ),
      ),

      //light
      theme: ThemeData(
        useMaterial3: false,
        appBarTheme: const AppBarTheme(
          elevation: 1,
          centerTitle: true,
          backgroundColor: Colors.white,
          iconTheme: IconThemeData(color: Colors.amber),
          titleTextStyle: TextStyle(
            color: Colors.amber,
            fontSize: 20,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),

      //
      home: const SplashScreen(),
    );
  }
}
