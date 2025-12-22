import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/services/sse_client_types.dart';
import 'package:selcukaiassistant/services/sse_parser.dart';

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
        buffer = processSseChunk(chunk, buffer, controller);
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
}
