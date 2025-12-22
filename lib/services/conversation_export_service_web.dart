// Web-only implementation loaded via conditional imports.
// dart:html is required for browser downloads.
// ignore_for_file: avoid_web_libraries_in_flutter, deprecated_member_use

import 'dart:convert';
import 'dart:html' as html;

import 'package:selcukaiassistant/services/conversation_export_types.dart';

Future<ExportResult> exportConversationImpl(
  String filename,
  String content,
) async {
  final bytes = utf8.encode(content);
  final blob = html.Blob([bytes], 'application/json');
  final url = html.Url.createObjectUrlFromBlob(blob);
  html.AnchorElement(href: url)
    ..setAttribute('download', filename)
    ..click();
  html.Url.revokeObjectUrl(url);
  return ExportResult(downloaded: true);
}
