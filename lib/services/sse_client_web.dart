/// DOSYA ADI: sse_client_web.dart
/// AMAÇ: Web platformunda SSE akışını yönetmek.
/// NE YAPAR:
///   - XHR ile stream bağlantısı kurar.
///   - SSE verisini parse ederek ChatStreamEvent üretir.
/// BAĞIMLILIKLAR:
///   - sse_parser.dart: SSE ayrıştırma
///   - error_messages.dart: Türkçe hata metinleri
/// SON DEĞİŞİKLİK: 17.01.2026
library;
// This file is the web-specific implementation for the SSE client.
// It uses `dart:html` to make HTTP requests for Server-Sent Events,
// which is why `avoid_web_libraries_in_flutter` is ignored.
// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use

import 'dart:async';
import 'dart:html' as html;

import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
import 'package:selcukaiassistant/services/sse_client_types.dart';
import 'package:selcukaiassistant/services/sse_parser.dart';

class SseClient {
  Future<ChatStreamSession> connect({
    required Uri url,
    required Map<String, String> headers,
    required String body,
  }) async {
    final controller = StreamController<ChatStreamEvent>();
    final request = html.HttpRequest()
      ..open('POST', url.toString())
      ..responseType = 'text';

    headers.forEach(request.setRequestHeader);

    var buffer = '';
    var lastIndex = 0;
    var sawError = false;

    request.onReadyStateChange.listen((_) {
      if (request.readyState == html.HttpRequest.HEADERS_RECEIVED &&
          request.status != 200 &&
          !sawError) {
        sawError = true;
        controller.addError(
          AppException(
            ErrorMessages.akisBasarisiz,
            detail: 'HTTP ${request.status} ${request.statusText}',
            code: 'stream_error',
          ),
        );
        request.abort();
      }
    });

    request.onProgress.listen((_) {
      final responseText = request.responseText ?? '';
      if (responseText.length <= lastIndex) {
        return;
      }
      final chunk = responseText.substring(lastIndex);
      lastIndex = responseText.length;
      buffer = processSseChunk(chunk, buffer, controller);
    });

    request.onError.listen((_) {
      if (!sawError) {
        sawError = true;
        controller.addError(
          AppException(
            ErrorMessages.akisBasarisiz,
            code: 'stream_error',
          ),
        );
      }
    });

    request.onLoadEnd.listen((_) {
      unawaited(controller.close());
    });

    request.send(body);

    return ChatStreamSession(
      stream: controller.stream,
      close: () {
        request.abort();
        unawaited(controller.close());
      },
    );
  }
}
