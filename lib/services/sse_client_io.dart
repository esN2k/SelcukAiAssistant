/// DOSYA ADI: sse_client_io.dart
/// AMAÇ: SSE akışını mobil/masaüstü platformlarında yönetmek.
/// NE YAPAR:
///   - Backend stream endpoint'ine bağlanır.
///   - SSE verisini parse ederek ChatStreamEvent üretir.
/// BAĞIMLILIKLAR:
///   - sse_parser.dart: SSE ayrıştırma
///   - error_messages.dart: Türkçe hata metinleri
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:async';
import 'dart:convert';

import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
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
      throw AppException(
        ErrorMessages.akisBasarisiz,
        detail: 'HTTP ${response.statusCode}',
        code: 'stream_error',
      );
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
