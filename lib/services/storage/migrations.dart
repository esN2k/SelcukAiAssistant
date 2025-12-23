import 'package:hive/hive.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/model/model_pref.dart';

typedef StorageMigration = Future<void> Function(
  StorageMigrationContext context,
);

class StorageMigrationContext {
  StorageMigrationContext({
    required this.metaBox,
    required this.settingsBox,
    required this.conversationsBox,
    required this.modelPrefsBox,
  });

  final Box<dynamic> metaBox;
  final Box<dynamic> settingsBox;
  final Box<Conversation> conversationsBox;
  final Box<ModelPreference> modelPrefsBox;
}

final Map<int, StorageMigration> storageMigrations = {
  1: _migrateToV1,
};

Future<void> _migrateToV1(StorageMigrationContext context) async {
  if (!await Hive.boxExists('myData')) {
    return;
  }

  final legacyBox = await Hive.openBox<dynamic>('myData');
  const legacyKeys = [
    'showOnboarding',
    'isDarkMode',
    'selectedModel',
    'localeCode',
    'backendUrlOverride',
  ];

  for (final key in legacyKeys) {
    if (legacyBox.containsKey(key) && !context.settingsBox.containsKey(key)) {
      await context.settingsBox.put(key, legacyBox.get(key));
    }
  }

  final selectedModel = legacyBox.get('selectedModel') as String?;
  if (selectedModel != null &&
      context.modelPrefsBox.get(defaultModelPreferenceId) == null) {
    await context.modelPrefsBox.put(
      defaultModelPreferenceId,
      ModelPreference(
        id: defaultModelPreferenceId,
        selectedModelId: selectedModel,
      ),
    );
  }

  await legacyBox.close();
}
