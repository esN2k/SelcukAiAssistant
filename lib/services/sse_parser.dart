import 'dart:async';
import 'dart:convert';

import 'package:selcukaiassistant/services/sse_client_types.dart';

String processSseChunk(
  String chunk,
  String buffer,
  StreamController<ChatStreamEvent> controller,
) {
  var workingBuffer = buffer + chunk;
  while (true) {
    final newlineIndex = workingBuffer.indexOf('\n');
    if (newlineIndex == -1) {
      return workingBuffer;
    }
    final line = workingBuffer.substring(0, newlineIndex).trimRight();
    workingBuffer = workingBuffer.substring(newlineIndex + 1);

    if (line.isEmpty) {
      continue;
    }

    if (!line.startsWith('data:')) {
      continue;
    }

    final jsonPart = line.substring(5).trim();
    if (jsonPart.isEmpty) {
      continue;
    }

    try {
      final data = jsonDecode(jsonPart) as Map<String, dynamic>;
      controller.add(ChatStreamEvent.fromJson(data));
    } on FormatException {
      continue;
    }
  }
}
