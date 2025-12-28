import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/controller/settings_controller.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/screen/diagnostics_screen.dart';
import 'package:selcukaiassistant/screen/model_picker_screen.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  late final SettingsController _controller;

  @override
  void initState() {
    super.initState();
    _controller = Get.isRegistered<SettingsController>()
        ? Get.find<SettingsController>()
        : Get.put(SettingsController());
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
      text: _controller.backendUrlOverride.value,
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
      _controller.clearBackendUrlOverride();
      Get.snackbar(
        l10n.successTitle,
        l10n.backendUrlCleared,
        snackPosition: SnackPosition.BOTTOM,
      );
      return;
    }

    _controller.setBackendUrlOverride(controller.text);
    Get.snackbar(
      l10n.successTitle,
      l10n.backendUrlSaved,
      snackPosition: SnackPosition.BOTTOM,
    );
  }

  ModelInfo? _selectedModelInfo() {
    return _controller.selectedModelInfo();
  }

  Future<void> _openModelPicker() async {
    final models = _controller.models.toList();
    if (models.isEmpty) return;
    final selected = await Get.to<String>(
      () => ModelPickerScreen(initialModels: models),
    );
    if (selected != null && selected.isNotEmpty) {
      _controller.selectModel(selected);
    }
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
          // Görünüm ayarları
          _buildSection(
            context,
            l10n.sectionAppearance,
            [
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.darkModeTitle),
                  subtitle: Text(l10n.darkModeSubtitle),
                  value: _controller.isDarkMode.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) => _controller.setDarkMode(value: value),
                  secondary: Icon(
                    _controller.isDarkMode.value
                        ? Icons.dark_mode
                        : Icons.light_mode,
                  ),
                ),
              ),
            ],
          ),

          // Dil seçimi
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
                      value: _controller.selectedLanguage.value,
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
                        _controller.setLanguage(value);
                      },
                    ),
                  ),
                ),
              ),
            ],
          ),

          // Yapay zeka modeli seçimi
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
                    trailing: _controller.isLoadingModels.value
                        ? const SizedBox(
                            width: 16,
                            height: 16,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Icon(Icons.arrow_forward_ios, size: 16),
                    onTap: _controller.models.isEmpty ? null : _openModelPicker,
                  );
                },
              ),
            ],
          ),

          // Sunucu ayarları
          _buildSection(
            context,
            l10n.sectionServer,
            [
              Obx(
                () {
                  final backendUrlOverride =
                      _controller.backendUrlOverride.value;
                  return ListTile(
                    key: ValueKey(backendUrlOverride),
                    title: Text(l10n.backendUrlTitle),
                    subtitle: Text(
                      l10n.backendUrlSubtitle(_resolvedBackendUrl()),
                    ),
                    leading: const Icon(Icons.link),
                    trailing: const Icon(Icons.edit, size: 16),
                    onTap: _editBackendUrl,
                  );
                },
              ),
            ],
          ),

          // Sohbet ayarları
          _buildSection(
            context,
            l10n.sectionChatSettings,
            [
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.voiceInputTitle),
                  subtitle: Text(l10n.voiceInputSubtitle),
                  value: _controller.voiceInputEnabled.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) =>
                      _controller.setVoiceInputEnabled(value: value),
                  secondary: const Icon(Icons.mic),
                ),
              ),
              const Divider(height: 1),
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.markdownSupportTitle),
                  subtitle: Text(l10n.markdownSupportSubtitle),
                  value: _controller.markdownEnabled.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) =>
                      _controller.setMarkdownEnabled(value: value),
                  secondary: const Icon(Icons.code),
                ),
              ),
              const Divider(height: 1),
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.ragEnabledTitle),
                  subtitle: Text(l10n.ragEnabledSubtitle),
                  value: _controller.ragEnabled.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: (value) => _controller.setRagEnabled(value: value),
                  secondary: const Icon(Icons.menu_book_outlined),
                ),
              ),
              const Divider(height: 1),
              Obx(
                () => SwitchListTile(
                  title: Text(l10n.ragStrictTitle),
                  subtitle: Text(l10n.ragStrictSubtitle),
                  value: _controller.ragStrict.value,
                  activeThumbColor: Theme.of(context).colorScheme.primary,
                  onChanged: _controller.ragEnabled.value
                      ? (value) => _controller.setRagStrict(value: value)
                      : null,
                  secondary: const Icon(Icons.verified_outlined),
                ),
              ),
            ],
          ),

          // Teşhis ekranı
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

          // İstatistikler
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

          // Veri yönetimi
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

          // Hakkında
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
