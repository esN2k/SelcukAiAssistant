import 'package:flutter/material.dart';

class SelcukColors {
  static const Color gold = Color(0xFFF3C200);
  static const Color deepGold = Color(0xFFC99700);
  static const Color ink = Color(0xFF101010);
  static const Color slate = Color(0xFF2A2A2A);
  static const Color cloud = Color(0xFFF7F7F5);
  static const Color mist = Color(0xFFE5E2DC);
  static const Color success = Color(0xFF1E8E5A);
  static const Color danger = Color(0xFFE05252);
}

class SelcukTheme {
  static ThemeData light() {
    const colorScheme = ColorScheme.light(
      primary: SelcukColors.gold,
      onPrimary: SelcukColors.ink,
      secondary: SelcukColors.deepGold,
      onSecondary: SelcukColors.ink,
      onSurface: SelcukColors.ink,
      error: SelcukColors.danger,
      outline: SelcukColors.mist,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.light,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: SelcukColors.cloud,
      fontFamily: 'Roboto',
      fontFamilyFallback: const ['NotoSansSymbols', 'NotoSansSymbols2'],
      appBarTheme: const AppBarTheme(
        backgroundColor: SelcukColors.cloud,
        foregroundColor: SelcukColors.ink,
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardThemeData(
        color: Colors.white,
        elevation: 8,
        shadowColor: SelcukColors.mist,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: Colors.white,
        hintStyle: const TextStyle(color: SelcukColors.slate),
        labelStyle: const TextStyle(color: SelcukColors.slate),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.mist),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.mist),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.gold, width: 2),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: SelcukColors.gold,
          foregroundColor: SelcukColors.ink,
          textStyle: const TextStyle(fontWeight: FontWeight.w600),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(foregroundColor: SelcukColors.deepGold),
      ),
      iconTheme: const IconThemeData(color: SelcukColors.slate),
      dividerColor: SelcukColors.mist,
      snackBarTheme: SnackBarThemeData(
        backgroundColor: SelcukColors.slate,
        contentTextStyle: const TextStyle(color: SelcukColors.cloud),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: SelcukColors.gold,
      ),
    );
  }

  static ThemeData dark() {
    const colorScheme = ColorScheme.dark(
      primary: SelcukColors.gold,
      onPrimary: SelcukColors.ink,
      secondary: SelcukColors.deepGold,
      onSecondary: SelcukColors.ink,
      surface: SelcukColors.slate,
      onSurface: SelcukColors.cloud,
      error: SelcukColors.danger,
      onError: Colors.white,
      outline: SelcukColors.slate,
    );

    return ThemeData(
      useMaterial3: true,
      brightness: Brightness.dark,
      colorScheme: colorScheme,
      scaffoldBackgroundColor: SelcukColors.ink,
      fontFamily: 'Roboto',
      fontFamilyFallback: const ['NotoSansSymbols', 'NotoSansSymbols2'],
      appBarTheme: const AppBarTheme(
        backgroundColor: SelcukColors.ink,
        foregroundColor: SelcukColors.cloud,
        elevation: 0,
        centerTitle: true,
      ),
      cardTheme: CardThemeData(
        color: SelcukColors.slate,
        elevation: 4,
        shadowColor: Colors.black54,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(20),
        ),
      ),
      inputDecorationTheme: InputDecorationTheme(
        filled: true,
        fillColor: SelcukColors.slate,
        hintStyle: const TextStyle(color: SelcukColors.mist),
        labelStyle: const TextStyle(color: SelcukColors.mist),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.slate),
        ),
        enabledBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.slate),
        ),
        focusedBorder: OutlineInputBorder(
          borderRadius: BorderRadius.circular(14),
          borderSide: const BorderSide(color: SelcukColors.gold, width: 2),
        ),
      ),
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          backgroundColor: SelcukColors.gold,
          foregroundColor: SelcukColors.ink,
          textStyle: const TextStyle(fontWeight: FontWeight.w600),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      ),
      textButtonTheme: TextButtonThemeData(
        style: TextButton.styleFrom(foregroundColor: SelcukColors.gold),
      ),
      iconTheme: const IconThemeData(color: SelcukColors.cloud),
      dividerColor: SelcukColors.slate,
      snackBarTheme: SnackBarThemeData(
        backgroundColor: SelcukColors.slate,
        contentTextStyle: const TextStyle(color: SelcukColors.cloud),
        behavior: SnackBarBehavior.floating,
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(12),
        ),
      ),
      progressIndicatorTheme: const ProgressIndicatorThemeData(
        color: SelcukColors.gold,
      ),
    );
  }
}
