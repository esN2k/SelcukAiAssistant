import 'package:selcukaiassistant/services/conversation_export_service_stub.dart'
    if (dart.library.io)
        'package:selcukaiassistant/services/conversation_export_service_io.dart'
    if (dart.library.html)
        'package:selcukaiassistant/services/conversation_export_service_web.dart';
import 'package:selcukaiassistant/services/conversation_export_types.dart';

Future<ExportResult> exportConversation(String filename, String content) {
  return exportConversationImpl(filename, content);
}
