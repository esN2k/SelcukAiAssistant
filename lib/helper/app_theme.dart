import 'package:flutter/material.dart';

extension AppTheme on ThemeData {
  //light text color
  Color get lightTextColor {
    final alpha = brightness == Brightness.dark ? 0.7 : 0.6;
    return colorScheme.onSurface.withValues(alpha: alpha);
  }

  //button color
  Color get buttonColor => colorScheme.primary;
}
