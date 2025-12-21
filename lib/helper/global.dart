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
    final envUrl = dotenv.env['BACKEND_URL'];
    if (envUrl != null && envUrl.isNotEmpty) {
      return envUrl;
    }
    if (kIsWeb) {
      return 'http://localhost:8000';
    } else if (Platform.isAndroid) {
      return 'http://10.0.2.2:8000';
    } else {
      return 'http://localhost:8000';
    }
  }

  static String get chatEndpoint => '$backendUrl/chat';
  static String get chatStreamEndpoint => '$backendUrl/chat/stream';
  static String get modelsEndpoint => '$backendUrl/models';
}
