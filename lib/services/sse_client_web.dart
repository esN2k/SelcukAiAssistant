// Web-only implementation loaded via conditional imports.
// dart:html is required for streaming XHR in the browser.
// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use

import 'dart:async';
import 'dart:html' as html;

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
          'Stream request failed: ${request.status} ${request.statusText}',
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
        controller.addError('Stream request failed');
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
