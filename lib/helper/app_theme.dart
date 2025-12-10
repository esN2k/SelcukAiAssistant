import 'package:flutter/material.dart';

extension AppTheme on ThemeData {
  //light text color
  Color get lightTextColor =>
      brightness == Brightness.dark ? Colors.white70 : Colors.black54;

  //button color
  Color get buttonColor => brightness == Brightness.dark
      ? Colors.cyan.withValues(alpha: 0.5)
      : Colors.amber;
}
