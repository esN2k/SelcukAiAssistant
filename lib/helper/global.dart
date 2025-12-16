import 'dart:io' show Platform;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart' show Size;

class Global {
  // App constants
  static const String appName = 'Selçuk AI Assistant';

  // Media query size (should be initialized in app)
  static Size mq = Size.zero;

  static String get backendUrl {
    if (kIsWeb) {
      return 'http://localhost:8000';
    } else if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    } else {
      return 'http://localhost:8000';
    }
  }

  static String get chatEndpoint => '$backendUrl/chat';
}
