import 'dart:io' show Platform;

import 'package:flutter/foundation.dart' show kIsWeb;
import 'package:flutter/material.dart' show Size;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class Global {
  // App constants
  static const String appName = 'Selçuk AI Assistant';

  // Media query size (should be initialized in app)
  static Size mq = Size.zero;

  static String get backendUrl {
    final envUrl = dotenv.env['BACKEND_URL']?.trim();
    if (envUrl != null && envUrl.isNotEmpty) {
      if (kIsWeb && (envUrl.contains('10.0.2.2') || envUrl.contains('10.0.3.2'))) {
        return 'http://localhost:8000';
      }
      if (!kIsWeb &&
          Platform.isAndroid &&
          (envUrl.contains('localhost') || envUrl.contains('127.0.0.1'))) {
        return 'http://10.0.2.2:8000';
      }
      return envUrl;
    }
    if (kIsWeb) {
      return 'http://localhost:8000';
    }
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    }
    return 'http://localhost:8000';
  }

  static String get chatEndpoint => '$backendUrl/chat';
  static String get chatStreamEndpoint => '$backendUrl/chat/stream';
  static String get modelsEndpoint => '$backendUrl/models';
}
