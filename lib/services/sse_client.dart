import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;

class ChatStreamEvent {
  ChatStreamEvent({
    required this.type,
    required this.requestId,
    this.token,
    this.message,
    this.usage,
  });

  factory ChatStreamEvent.fromJson(Map<String, dynamic> json) {
    return ChatStreamEvent(
      type: json['type'] as String? ?? '',
      requestId: json['request_id'] as String? ?? '',
      token: json['token'] as String?,
      message: json['message'] as String?,
      usage: json['usage'] as Map<String, dynamic>?,
    );
  }

  final String type;
  final String requestId;
  final String? token;
  final String? message;
  final Map<String, dynamic>? usage;
}

class ChatStreamSession {
  ChatStreamSession({
    required this.stream,
    required this.close,
  });

  final Stream<ChatStreamEvent> stream;
  final void Function() close;
}

class SseClient {
  SseClient() : _client = http.Client();

  final http.Client _client;

  Future<ChatStreamSession> connect({
    required Uri url,
    required Map<String, String> headers,
    required String body,
  }) async {
    final request = http.Request('POST', url);
    request.headers.addAll(headers);
    request.body = body;

    final response = await _client.send(request);
    if (response.statusCode != 200) {
      _client.close();
      throw Exception('Stream request failed: ${response.statusCode}');
    }

    final controller = StreamController<ChatStreamEvent>();
    var buffer = '';
    final subscription = response.stream.transform(utf8.decoder).listen(
      (chunk) {
        buffer = _processChunk(chunk, buffer, controller);
      },
      onError: (Object error) {
        controller.addError(error);
      },
      onDone: () {
        unawaited(controller.close());
      },
      cancelOnError: true,
    );

    return ChatStreamSession(
      stream: controller.stream,
      close: () {
        unawaited(subscription.cancel());
        _client.close();
      },
    );
  }

  String _processChunk(
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
}
