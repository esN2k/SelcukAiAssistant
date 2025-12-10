import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:hive_flutter/adapters.dart';

class Pref {
  static Box<dynamic>? _box;

  static Future<void> initialize() async {
    try {
      //for initializing hive to use app directory
      await Hive.initFlutter();
      _box = await Hive.openBox('myData');
    } catch (e) {
      log('Hive initialization failed: $e');
    }
  }

  static bool get showOnboarding =>
      _box?.get('showOnboarding', defaultValue: true) as bool? ?? true;

  static set showOnboarding(bool v) => _box?.put('showOnboarding', v);

  //for storing theme data
  static bool get isDarkMode => (_box?.get('isDarkMode') as bool?) ?? false;

  static set isDarkMode(bool v) => _box?.put('isDarkMode', v);

  static ThemeMode get defaultTheme {
    final data = _box?.get('isDarkMode');
    log('data: $data');
    if (data == null) return ThemeMode.system;
    if (data == true) return ThemeMode.dark;
    return ThemeMode.light;
  }
}
