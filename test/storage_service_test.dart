import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:hive/hive.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/model/model_pref.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';

void main() {
  TestWidgetsFlutterBinding.ensureInitialized();

  group('StorageService', () {
    late Directory tempDir;

    setUp(() async {
      tempDir = await Directory.systemTemp.createTemp(
        'selcukaiassistant_test_',
      );
    });

    tearDown(() async {
      await StorageService.close();
      await Hive.deleteFromDisk();
      await tempDir.delete(recursive: true);
    });

    test('initializes schema and boxes', () async {
      await StorageService.initializeForTesting(tempDir.path);

      expect(
        StorageService.metaBox.get('schema_version'),
        StorageService.currentSchemaVersion,
      );
      expect(StorageService.settingsBox.isOpen, isTrue);
      expect(StorageService.conversationsBox.isOpen, isTrue);
      expect(StorageService.modelPrefsBox.isOpen, isTrue);
    });

    test('migrates legacy settings', () async {
      Hive.init(tempDir.path);
      final legacy = await Hive.openBox<dynamic>('myData');
      await legacy.put('localeCode', 'tr');
      await legacy.put('selectedModel', 'llama3');
      await legacy.close();
      await Hive.close();

      await StorageService.initializeForTesting(tempDir.path);

      expect(StorageService.settingsBox.get('localeCode'), 'tr');
      final pref =
          StorageService.modelPrefsBox.get(defaultModelPreferenceId);
      expect(pref?.selectedModelId, 'llama3');
    });

    test('persists conversation messages', () async {
      await StorageService.initializeForTesting(tempDir.path);

      final conversation = Conversation(
        id: 'c1',
        title: 'Test',
        createdAt: DateTime.utc(2024),
        updatedAt: DateTime.utc(2024),
      );
      final message = ChatMessage(
        id: 'm1',
        content: 'Hello',
        isUser: true,
        createdAt: DateTime.utc(2024),
      );
      conversation.messages.add(message);

      await StorageService.conversationsBox.put(conversation.id, conversation);
      await StorageService.close();

      await StorageService.initializeForTesting(tempDir.path);
      final loaded = StorageService.conversationsBox.get('c1');
      expect(loaded, isNotNull);
      expect(loaded!.messages.length, 1);
      expect(loaded.messages.first.content, 'Hello');
    });
  });
}
