import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/services/model_service.dart';

class SettingsController extends GetxController {
  SettingsController({
    Future<List<ModelInfo>> Function()? fetchModels,
  }) : _fetchModels = fetchModels ?? ModelService.fetchModels;

  final Future<List<ModelInfo>> Function() _fetchModels;
  final RxBool isDarkMode = Get.isDarkMode.obs;
  final RxString selectedModel = (Pref.selectedModel ?? '').obs;
  final RxBool voiceInputEnabled = Pref.voiceInputEnabled.obs;
  final RxBool markdownEnabled = Pref.markdownEnabled.obs;
  final RxBool ragEnabled = Pref.ragEnabled.obs;
  final RxBool ragStrict = Pref.ragStrict.obs;
  final RxString selectedLanguage =
      (Pref.localeCode ?? L10n.fallbackLocale.languageCode).obs;
  final RxString backendUrlOverride = (Pref.backendUrlOverride ?? '').obs;
  final RxList<ModelInfo> models = <ModelInfo>[].obs;
  final RxBool isLoadingModels = false.obs;

  @override
  void onInit() {
    super.onInit();
    unawaited(loadModels());
  }

  Future<void> loadModels() async {
    isLoadingModels.value = true;
    final fetched = await _fetchModels();
    models.assignAll(fetched);
    isLoadingModels.value = false;
    ensureSelectedModel();
  }

  void ensureSelectedModel() {
    if (models.isEmpty) {
      return;
    }

    final stored = Pref.selectedModel;
    if (stored != null && models.any((m) => m.id == stored)) {
      selectedModel.value = stored;
      return;
    }

    final availableModels = models.where((m) => m.available).toList();
    var defaultModel = models.firstWhere(
      (m) => m.isDefault,
      orElse: () =>
          availableModels.isNotEmpty ? availableModels.first : models.first,
    );
    if (!defaultModel.available && availableModels.isNotEmpty) {
      defaultModel = availableModels.first;
    }
    selectModel(defaultModel.id);
  }

  ModelInfo? selectedModelInfo() {
    final selected = selectedModel.value;
    if (selected.isEmpty) {
      return null;
    }
    for (final model in models) {
      if (model.id == selected) {
        return model;
      }
    }
    return null;
  }

  void selectModel(String id) {
    selectedModel.value = id;
    Pref.selectedModel = id;
  }

  void setDarkMode({required bool value}) {
    final newMode = value ? ThemeMode.dark : ThemeMode.light;
    Get.changeThemeMode(newMode);
    isDarkMode.value = value;
    Pref.isDarkMode = value;
  }

  void setLanguage(String code) {
    selectedLanguage.value = code;
    Pref.localeCode = code;
    unawaited(Get.updateLocale(Locale(code)));
  }

  void setBackendUrlOverride(String value) {
    final trimmed = value.trim();
    backendUrlOverride.value = trimmed;
    Pref.backendUrlOverride = trimmed;
  }

  void clearBackendUrlOverride() {
    backendUrlOverride.value = '';
    Pref.backendUrlOverride = null;
  }

  void setVoiceInputEnabled({required bool value}) {
    voiceInputEnabled.value = value;
    Pref.voiceInputEnabled = value;
  }

  void setMarkdownEnabled({required bool value}) {
    markdownEnabled.value = value;
    Pref.markdownEnabled = value;
  }

  void setRagEnabled({required bool value}) {
    ragEnabled.value = value;
    Pref.ragEnabled = value;
  }

  void setRagStrict({required bool value}) {
    ragStrict.value = value;
    Pref.ragStrict = value;
  }
}
