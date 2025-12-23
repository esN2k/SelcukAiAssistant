import 'package:flutter/foundation.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/pref.dart';

enum BackendUrlSource {
  override,
  dartDefine,
  dotenv,
  webRelease,
  webDev,
  androidEmulator,
  desktop,
}

class BackendUrlResolution {
  const BackendUrlResolution({
    required this.url,
    required this.source,
  });

  final String url;
  final BackendUrlSource source;
}

class BackendConfig {
  static BackendUrlResolution get resolution => _resolve();

  static String get baseUrl => resolution.url;

  static String get chatEndpoint => '$baseUrl/chat';
  static String get chatStreamEndpoint => '$baseUrl/chat/stream';
  static String get modelsEndpoint => '$baseUrl/models';

  static Future<bool> testConnection() async {
    try {
      final response = await http.get(Uri.parse('$baseUrl/health'));
      return response.statusCode == 200;
    } on Exception {
      return false;
    }
  }

  static BackendUrlResolution _resolve() {
    final override = Pref.backendUrlOverride?.trim();
    if (override != null && override.isNotEmpty) {
      return BackendUrlResolution(
        url: _normalizeBaseUrl(_adjustForPlatform(override)),
        source: BackendUrlSource.override,
      );
    }

    const envUrl = String.fromEnvironment('BACKEND_URL');
    if (envUrl.isNotEmpty) {
      return BackendUrlResolution(
        url: _normalizeBaseUrl(_adjustForPlatform(envUrl)),
        source: BackendUrlSource.dartDefine,
      );
    }

    final dotenvUrl = dotenv.env['BACKEND_URL']?.trim();
    if (dotenvUrl != null && dotenvUrl.isNotEmpty) {
      return BackendUrlResolution(
        url: _normalizeBaseUrl(_adjustForPlatform(dotenvUrl)),
        source: BackendUrlSource.dotenv,
      );
    }

    if (kIsWeb) {
      if (kReleaseMode) {
        return BackendUrlResolution(
          url: _normalizeBaseUrl('${Uri.base.origin}/api'),
          source: BackendUrlSource.webRelease,
        );
      }
      return const BackendUrlResolution(
        url: 'http://localhost:8000',
        source: BackendUrlSource.webDev,
      );
    }
    if (_isAndroid()) {
      return const BackendUrlResolution(
        url: 'http://10.0.2.2:8000',
        source: BackendUrlSource.androidEmulator,
      );
    }
    return const BackendUrlResolution(
      url: 'http://localhost:8000',
      source: BackendUrlSource.desktop,
    );
  }

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
