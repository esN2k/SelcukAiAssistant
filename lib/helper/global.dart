import 'package:flutter/foundation.dart'
    show TargetPlatform, defaultTargetPlatform, kIsWeb, kReleaseMode;
import 'package:flutter/material.dart' show Size;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:selcukaiassistant/helper/pref.dart';

class Global {
  // App constants
  static const String appName = 'Selcuk AI Assistant';

  // Media query size (should be initialized in app)
  static Size mq = Size.zero;

  static String get backendUrl {
    final override = Pref.backendUrlOverride?.trim();
    if (override != null && override.isNotEmpty) {
      return _normalizeBaseUrl(_adjustForPlatform(override));
    }

    final envUrl = dotenv.env['BACKEND_URL']?.trim();
    if (envUrl != null && envUrl.isNotEmpty) {
      return _normalizeBaseUrl(_adjustForPlatform(envUrl));
    }

    if (kIsWeb) {
      return kReleaseMode ? '/api' : 'http://localhost:8000';
    }
    if (_isAndroid()) {
      return 'http://10.0.2.2:8000';
    }
    return 'http://localhost:8000';
  }

  static String get chatEndpoint => '$backendUrl/chat';
  static String get chatStreamEndpoint => '$backendUrl/chat/stream';
  static String get modelsEndpoint => '$backendUrl/models';

  static String _adjustForPlatform(String url) {
    if (kIsWeb &&
        (url.contains('10.0.2.2') || url.contains('10.0.3.2'))) {
      return 'http://localhost:8000';
    }
    if (_isAndroid() &&
        (url.contains('localhost') || url.contains('127.0.0.1'))) {
      return 'http://10.0.2.2:8000';
    }
    return url;
  }

  static String _normalizeBaseUrl(String url) {
    var normalized = url.trim();
    if (normalized.endsWith('/')) {
      normalized = normalized.substring(0, normalized.length - 1);
    }
    return normalized;
  }

  static bool _isAndroid() {
    return !kIsWeb && defaultTargetPlatform == TargetPlatform.android;
  }
}
