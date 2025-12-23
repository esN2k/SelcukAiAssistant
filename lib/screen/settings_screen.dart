// ignore_for_file: deprecated_member_use // TODO: migrate to RadioGroup APIs.

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/screen/diagnostics_screen.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';
import 'package:selcukaiassistant/services/model_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final RxBool _isDarkMode = Get.isDarkMode.obs;
  final RxString _selectedModel = ''.obs;
  final RxBool _speechEnabled = true.obs;
  final RxBool _markdownEnabled = true.obs;
  final RxString _selectedLanguage =
      (Pref.localeCode ?? L10n.fallbackLocale.languageCode).obs;
  List<ModelInfo> _models = [];
  bool _isLoadingModels = false;

  @override
  void initState() {
    super.initState();
    _isDarkMode.value = Get.isDarkMode;
    _selectedModel.value = Pref.selectedModel ?? '';
    unawaited(_loadModels());
  }

  Future<void> _loadModels() async {
    setState(() => _isLoadingModels = true);
    final models = await ModelService.fetchModels();
    if (mounted) {
      setState(() {
        _models = models;
        _isLoadingModels = false;
      });
      _ensureSelectedModel();
    }
  }

  void _ensureSelectedModel() {
    if (_models.isEmpty) return;

    final stored = Pref.selectedModel;
    if (stored != null && _models.any((m) => m.id == stored)) {
      _selectedModel.value = stored;
      return;
    }

    final availableModels = _models.where((m) => m.available).toList();
    var defaultModel = _models.firstWhere(
      (m) => m.isDefault,
      orElse: () =>
          availableModels.isNotEmpty ? availableModels.first : _models.first,
    );
    if (!defaultModel.available && availableModels.isNotEmpty) {
      defaultModel = availableModels.first;
    }
    _selectedModel.value = defaultModel.id;
    Pref.selectedModel = defaultModel.id;
  }

  Future<void> _clearAllData() async {
    final l10n = context.l10n;
    final confirmed = await Get.dialog<bool>(
      AlertDialog(
        title: Text(l10n.clearAllDataTitle),
        content: Text(l10n.clearAllDataMessage),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: false),
            child: Text(l10n.cancel),
          ),
          TextButton(
            onPressed: () => Get.back(result: true),
            child: Text(
              l10n.deleteAll,
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirmed ?? false) {
      await ConversationService.clearAll();
      if (mounted) {
        Get.snackbar(
          l10n.clearAllSuccessTitle,
          l10n.clearAllSuccessMessage,
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    }
  }

  String _resolvedBackendUrl() => BackendConfig.baseUrl;

  Future<void> _editBackendUrl() async {
    final l10n = context.l10n;
    final controller = TextEditingController(
      text: Pref.backendUrlOverride ?? '',
    );

    final action = await Get.dialog<String>(
      AlertDialog(
        title: Text(l10n.backendUrlTitle),
        content: TextField(
          controller: controller,
          decoration: InputDecoration(
            hintText: l10n.backendUrlHint,
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: 'cancel'),
            child: Text(l10n.cancel),
          ),
          TextButton(
            onPressed: () => Get.back(result: 'clear'),
            child: Text(l10n.backendUrlClear),
          ),
          TextButton(
            onPressed: () => Get.back(result: 'save'),
            child: Text(l10n.backendUrlSave),
          ),
        ],
      ),
    );

    if (!mounted || action == null || action == 'cancel') {
      return;
    }

    if (action == 'clear') {
      Pref.backendUrlOverride = null;
      setState(() {});
      Get.snackbar(
        l10n.successTitle,
        l10n.backendUrlCleared,
        snackPosition: SnackPosition.BOTTOM,
      );
      return;
    }

    Pref.backendUrlOverride = controller.text;
    setState(() {});
    Get.snackbar(
      l10n.successTitle,
      l10n.backendUrlSaved,
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  ModelInfo? _selectedModelInfo() {
    final selected = _selectedModel.value;
    if (selected.isEmpty) return null;
    for (final model in _models) {
      if (model.id == selected) {
        return model;
      }
    }
    return null;
  }

  Future<void> _openModelPicker() async {
    if (_models.isEmpty) return;
    final l10n = context.l10n;
    final localModels = _models.where((model) => model.isLocal).toList();
    final remoteModels = _models.where((model) => model.isRemote).toList();

    await Get.dialog<void>(
      AlertDialog(
        title: Text(l10n.selectModelTitle),
        content: SizedBox(
          width: double.maxFinite,
          child: ListView(
            shrinkWrap: true,
            children: [
              _buildModelSection(
                context,
                l10n.modelLocalSection,
                localModels,
              ),
              _buildModelSection(
                context,
                l10n.modelRemoteSection,
                remoteModels,
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildModelSection(
    BuildContext context,
    String title,
    List<ModelInfo> models,
  ) {
    if (models.isEmpty) return const SizedBox.shrink();
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.only(bottom: 8, top: 12),
          child: Text(
            title,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
        ...models.map((model) => _buildModelTile(context, model)),
      ],
    );
  }

  Widget _buildModelTile(BuildContext context, ModelInfo model) {
    final l10n = context.l10n;
    final subtitles = <Widget>[
      Text('${model.provider}: ${model.modelId}'),
    ];
    if (!model.available && model.reasonUnavailable.isNotEmpty) {
      subtitles.add(Text(l10n.modelUnavailableReason(model.reasonUnavailable)));
    }
    if (!model.available && model.provider == 'ollama') {
      final command = 'ollama pull ${model.modelId}';
      subtitles.add(Text(l10n.modelInstallCommand(command)));
    }

    return RadioListTile<String>(
      title: Wrap(
        spacing: 8,
        runSpacing: 4,
        crossAxisAlignment: WrapCrossAlignment.center,
        children: [
          Text(model.displayName),
          _buildAvailabilityChip(context, model),
        ],
      ),
      subtitle: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: subtitles,
      ),
      value: model.id,
      groupValue: _selectedModel.value,
      onChanged: model.available
          ? (value) {
              if (value != null) {
                _selectedModel.value = value;
                Pref.selectedModel = value;
                Get.back<void>();
              }
            }
          : null,
    );
  }

  Widget _buildAvailabilityChip(BuildContext context, ModelInfo model) {
    final l10n = context.l10n;
    final scheme = Theme.of(context).colorScheme;
    final available = model.available;
    final label = available ? l10n.modelAvailable : l10n.modelUnavailable;
    final background =
        available ? scheme.secondaryContainer : scheme.surfaceVariant;
    final foreground =
        available ? scheme.onSecondaryContainer : scheme.onSurfaceVariant;

    return Chip(
      label: Text(label),
      labelStyle: TextStyle(color: foreground),
      backgroundColor: background,
      visualDensity: VisualDensity.compact,
    );
  }

  Widget _buildSection(
    BuildContext context,
    String title,
    List<Widget> children,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
          child: Text(
            title,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
        Card(
          margin: const EdgeInsets.symmetric(horizontal: 16),
          child: Column(children: children),
        ),
      ],
    );
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final stats = ConversationService.getStatistics();

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.settingsTitle),
        centerTitle: true,
      ),
      body: ListView(
        children: [
          // Appearance Section
          _buildSection(
            context,
            l10n.sectionAppearance,
            [
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.darkModeTitle),
                  subtitle: Text(l10n.darkModeSubtitle),
                  value: _isDarkMode.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) {
                    final newMode = value ? ThemeMode.dark : ThemeMode.light;
                    Get.changeThemeMode(newMode);
                    _isDarkMode.value = value;
                    Pref.isDarkMode = value;
                  },
                  secondary: Icon(
                    _isDarkMode.value ? Icons.dark_mode : Icons.light_mode,
                  ),
                ),
              ),
            ],
          ),

          // Language Section
          _buildSection(
            context,
            l10n.sectionLanguage,
            [
              Obx(
                () => ListTile(
                  title: Text(l10n.languageTitle),
                  subtitle: Text(l10n.languageSubtitle),
                  leading: const Icon(Icons.language),
                  trailing: DropdownButtonHideUnderline(
                    child: DropdownButton<String>(
                      value: _selectedLanguage.value,
                      items: [
                        DropdownMenuItem(
                          value: 'tr',
                          child: Text(l10n.languageTurkish),
                        ),
                        DropdownMenuItem(
                          value: 'en',
                          child: Text(l10n.languageEnglish),
                        ),
                      ],
                      onChanged: (value) {
                        if (value == null) return;
                        _selectedLanguage.value = value;
                        Pref.localeCode = value;
                        unawaited(Get.updateLocale(Locale(value)));
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),

          // AI Model Section
          _buildSection(
            context,
            l10n.sectionAiModel,
            [
              Obx(
                () {
                  final selectedInfo = _selectedModelInfo();
                  final subtitle = selectedInfo == null
                      ? l10n.modelNotSelected
                      : '${selectedInfo.displayName} '
                          '(${selectedInfo.provider}: ${selectedInfo.modelId})';
                  return ListTile(
                    title: Text(l10n.modelLabel),
                    subtitle: Text(subtitle),
                    leading: const Icon(Icons.psychology),
                    trailing: _isLoadingModels
                        ? const SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: _models.isEmpty ? null : _openModelPicker,
                  );
                },
              ),
            ],
          ),

          // Server Section
          _buildSection(
            context,
            l10n.sectionServer,
            [
              ListTile(
                title: Text(l10n.backendUrlTitle),
                subtitle: Text(
                  l10n.backendUrlSubtitle(_resolvedBackendUrl()),
                ),
                leading: const Icon(Icons.link),
                trailing: const Icon(Icons.edit, size: 16),
                onTap: _editBackendUrl,
              ),
            ],
          ),

          // Chat Settings Section
          _buildSection(
            context,
            l10n.sectionChatSettings,
            [
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.voiceInputTitle),
                  subtitle: Text(l10n.voiceInputSubtitle),
                  value: _speechEnabled.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) {
                    _speechEnabled.value = value;
                  },
                  secondary: const Icon(Icons.mic),
                ),
              ),
              const Divider(height: 1),
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.markdownSupportTitle),
                  subtitle: Text(l10n.markdownSupportSubtitle),
                  value: _markdownEnabled.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) {
                    _markdownEnabled.value = value;
                  },
                  secondary: const Icon(Icons.code),
                ),
              ),
            ],
          ),

          // Diagnostics Section
          _buildSection(
            context,
            l10n.sectionDiagnostics,
            [
              ListTile(
                title: Text(l10n.diagnosticsTitle),
                subtitle: Text(l10n.diagnosticsSubtitle),
                leading: const Icon(Icons.monitor_heart),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: () {
                  unawaited(Get.to<void>(() => const DiagnosticsScreen()));
                },
              ),
            ],
          ),

          // Statistics Section
          _buildSection(
            context,
            l10n.sectionStatistics,
            [
              ListTile(
                title: Text(l10n.totalConversations),
                trailing: Text(
                  '${stats['totalConversations']}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                leading: const Icon(Icons.chat),
              ),
              const Divider(height: 1),
              ListTile(
                title: Text(l10n.totalMessages),
                trailing: Text(
                  '${stats['totalMessages']}',
                  style: const TextStyle(
                    fontSize: 16,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                leading: const Icon(Icons.message),
              ),
            ],
          ),

          // Data Management Section
          _buildSection(
            context,
            l10n.sectionDataManagement,
            [
              ListTile(
                title: Text(l10n.clearAllConversationsTitle),
                subtitle: Text(l10n.clearAllConversationsSubtitle),
                leading: const Icon(Icons.delete_forever, color: Colors.red),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _clearAllData,
              ),
            ],
          ),

          // About Section
          _buildSection(
            context,
            l10n.sectionAbout,
            [
              ListTile(
                title: Text(l10n.versionLabel),
                trailing: const Text('1.0.2'),
                leading: const Icon(Icons.info),
              ),
              const Divider(height: 1),
              ListTile(
                title: Text(l10n.developerLabel),
                trailing: Text(l10n.developerValue),
                leading: const Icon(Icons.person),
              ),
            ],
          ),

          const SizedBox(height: 32),
        ],
      ),
    );
  }
}
