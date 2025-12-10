import 'dart:developer';

import 'package:appwrite/appwrite.dart';
import 'package:selcukaiassistant/helper/global.dart';

class AppWrite {
  static final _client = Client();
  static final _database = Databases(_client);

  static Future<void> init() async {
    _client
        .setEndpoint('https://cloud.appwrite.io/v1')
        .setProject('658813fd62bd45e744cd')
        .setSelfSigned();
    await getApiKey();
  }

  static Future<String> getApiKey() async {
    try {
      // Using deprecated getDocument until SDK is updated to support TablesDB
      // ignore: deprecated_member_use
      final d = await _database.getDocument(
        databaseId: 'MyDatabase',
        collectionId: 'ApiKey',
        documentId: 'chatGptKey',
      );

      apiKey = d.data['apiKey'] as String;
      log(apiKey);
      return apiKey;
    } on Exception catch (e) {
      log('$e');
      return '';
    }
  }
}
