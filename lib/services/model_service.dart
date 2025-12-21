import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/model/model_info.dart';

class ModelService {
  static Future<List<ModelInfo>> fetchModels() async {
    try {
      final response = await http.get(
        Uri.parse(Global.modelsEndpoint),
        headers: {'Content-Type': 'application/json; charset=utf-8'},
      );

      if (response.statusCode != 200) {
        log('Models endpoint error: ${response.statusCode}');
        return [];
      }

      final payload = jsonDecode(utf8.decode(response.bodyBytes))
          as Map<String, dynamic>;
      final items = payload['models'] as List<dynamic>? ?? [];
      return items
          .map((item) => ModelInfo.fromJson(item as Map<String, dynamic>))
          .toList();
    } on Exception catch (e) {
      log('Failed to fetch models: $e');
      return [];
    }
  }
}
