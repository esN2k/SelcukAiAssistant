import 'package:hive_flutter/hive_flutter.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/model/model_pref.dart';
import 'package:selcukaiassistant/services/storage/migrations.dart';

class StorageService {
  static const int currentSchemaVersion = 1;
  static const String metadataBoxName = 'storage_meta';
  static const String settingsBoxName = 'settings';
  static const String conversationsBoxName = 'conversations';
  static const String modelPrefsBoxName = 'model_prefs';

  static bool _initialized = false;
  static Box<dynamic>? _metaBox;
  static Box<dynamic>? _settingsBox;
  static Box<Conversation>? _conversationsBox;
  static Box<ModelPreference>? _modelPrefsBox;

  static Future<void> initialize({String? basePath}) async {
    if (_initialized) {
      return;
    }

    if (basePath == null) {
      await Hive.initFlutter();
    } else {
      Hive.init(basePath);
    }

    _registerAdapters();

    _metaBox = await Hive.openBox<dynamic>(metadataBoxName);
    _settingsBox = await Hive.openBox<dynamic>(settingsBoxName);
    _conversationsBox = await Hive.openBox<Conversation>(conversationsBoxName);
    _modelPrefsBox = await Hive.openBox<ModelPreference>(modelPrefsBoxName);

    await _runMigrations();
    _initialized = true;
  }

  static Future<void> initializeForTesting(String basePath) async {
    await initialize(basePath: basePath);
  }

  static Box<dynamic> get metaBox => _requireBox(_metaBox, metadataBoxName);
  static Box<dynamic> get settingsBox =>
      _requireBox(_settingsBox, settingsBoxName);
  static Box<Conversation> get conversationsBox =>
      _requireBox(_conversationsBox, conversationsBoxName);
  static Box<ModelPreference> get modelPrefsBox =>
      _requireBox(_modelPrefsBox, modelPrefsBoxName);

  static Future<void> close() async {
    await Hive.close();
    _initialized = false;
    _metaBox = null;
    _settingsBox = null;
    _conversationsBox = null;
    _modelPrefsBox = null;
  }

  static Box<T> _requireBox<T>(Box<T>? box, String name) {
    if (box == null) {
      throw StateError('StorageService not initialized: $name');
    }
    return box;
  }

  static void _registerAdapters() {
    if (!Hive.isAdapterRegistered(0)) {
      Hive.registerAdapter(ConversationAdapter());
    }
    if (!Hive.isAdapterRegistered(1)) {
      Hive.registerAdapter(ChatMessageAdapter());
    }
    if (!Hive.isAdapterRegistered(2)) {
      Hive.registerAdapter(ModelPreferenceAdapter());
    }
  }

  static Future<void> _runMigrations() async {
    final storedVersion =
        metaBox.get('schema_version', defaultValue: 0) as int;
    if (storedVersion >= currentSchemaVersion) {
      return;
    }

    final context = StorageMigrationContext(
      metaBox: metaBox,
      settingsBox: settingsBox,
      conversationsBox: conversationsBox,
      modelPrefsBox: modelPrefsBox,
    );

    for (var version = storedVersion + 1;
        version <= currentSchemaVersion;
        version++) {
      final migration = storageMigrations[version];
      if (migration != null) {
        await migration(context);
      }
    }

    await metaBox.put('schema_version', currentSchemaVersion);
  }
}
