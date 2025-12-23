import 'package:flutter/material.dart' show Size;
import 'package:selcukaiassistant/config/backend_config.dart';

class Global {
  // App constants
  static const String appName = 'Sel\u00e7uk YZ Asistan';

  // Media query size (should be initialized in app)
  static Size mq = Size.zero;

  static String get backendUrl => BackendConfig.baseUrl;

  static String get chatEndpoint => BackendConfig.chatEndpoint;
  static String get chatStreamEndpoint => BackendConfig.chatStreamEndpoint;
  static String get modelsEndpoint => BackendConfig.modelsEndpoint;
}
