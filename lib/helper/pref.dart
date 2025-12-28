import 'dart:async';
import 'dart:developer';

import 'package:flutter/material.dart';
import 'package:hive/hive.dart';
import 'package:selcukaiassistant/model/model_pref.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';

class Pref {
  static Box<dynamic>? _box;
  static Box<ModelPreference>? _modelBox;

  static Future<void> initialize() async {
    await StorageService.initialize();
    _box = StorageService.settingsBox;
    _modelBox = StorageService.modelPrefsBox;
  }

  static Box<dynamic> get box {
    if (_box == null) {
      throw StateError('Pref not initialized');
    }
    return _box!;
  }

  static Box<ModelPreference> get modelBox {
    if (_modelBox == null) {
      throw StateError('Pref not initialized');
    }
    return _modelBox!;
  }

  static bool get showOnboarding =>
      box.get('showOnboarding', defaultValue: true) as bool;

  static set showOnboarding(bool v) => box.put('showOnboarding', v);

  // Normal Way - Get
  // how to call
  // showOnboarding()

  // static bool showOnboarding() {
  //   return _box.get('showOnboarding', defaultValue: true);
  // }

  // Normal Way - Set
  // how to call
  // showOnboarding(false)

  // static bool showOnboarding(bool v) {
  //   _box.put('showOnboarding', v);
  // }

  //for storing theme data
  static bool get isDarkMode => (box.get('isDarkMode') as bool?) ?? false;

  static set isDarkMode(bool v) => box.put('isDarkMode', v);

  static ThemeMode get defaultTheme {
    final data = box.get('isDarkMode');
    log('data: $data');
    if (data == null) return ThemeMode.system;
    if (data == true) return ThemeMode.dark;
    return ThemeMode.light;
  }

  static String? get selectedModel {
    final stored = modelBox.get(defaultModelPreferenceId)?.selectedModelId;
    if (stored != null && stored.isNotEmpty) {
      return stored;
    }
    final legacy = box.get('selectedModel') as String?;
    if (legacy != null && legacy.isNotEmpty) {
      final pref = ModelPreference(
        id: defaultModelPreferenceId,
        selectedModelId: legacy,
      );
      unawaited(modelBox.put(defaultModelPreferenceId, pref));
    }
    return legacy;
  }

  static set selectedModel(String? value) {
    final trimmed = value?.trim();
    if (trimmed == null || trimmed.isEmpty) {
      unawaited(modelBox.delete(defaultModelPreferenceId));
      return;
    }

    final pref = (modelBox.get(defaultModelPreferenceId) ??
          ModelPreference(id: defaultModelPreferenceId))
        ..selectedModelId = trimmed
        ..updatedAt = DateTime.now();
    unawaited(modelBox.put(defaultModelPreferenceId, pref));
  }

  static String? get localeCode =>
      box.get('localeCode') as String?;

  static set localeCode(String? value) => box.put('localeCode', value);

  static String? get backendUrlOverride =>
      box.get('backendUrlOverride') as String?;

  static set backendUrlOverride(String? value) {
    if (value == null || value.trim().isEmpty) {
      unawaited(box.delete('backendUrlOverride'));
    } else {
      unawaited(box.put('backendUrlOverride', value.trim()));
    }
  }

  static bool get ragEnabled =>
      (box.get('ragEnabled') as bool?) ?? false;

  static set ragEnabled(bool value) => box.put('ragEnabled', value);

  static bool get ragStrict =>
      (box.get('ragStrict') as bool?) ?? true;

  static set ragStrict(bool value) => box.put('ragStrict', value);

  static bool get voiceInputEnabled =>
      (box.get('voiceInputEnabled') as bool?) ?? true;

  static set voiceInputEnabled(bool value) =>
      box.put('voiceInputEnabled', value);

  static bool get markdownEnabled =>
      (box.get('markdownEnabled') as bool?) ?? true;

  static set markdownEnabled(bool value) =>
      box.put('markdownEnabled', value);

  static int get ragTopK => (box.get('ragTopK') as int?) ?? 4;

  static set ragTopK(int value) => box.put('ragTopK', value);
}
