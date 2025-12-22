import 'dart:io';

import 'package:path_provider/path_provider.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

Future<ExportResult> exportConversationImpl(
  String filename,
  String content,
) async {
  final directory = await getApplicationDocumentsDirectory();
  final file = File('${directory.path}/$filename');
  await file.writeAsString(content);
  return ExportResult(path: file.path);
}
