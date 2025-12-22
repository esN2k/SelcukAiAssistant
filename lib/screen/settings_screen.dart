// ignore_for_file: deprecated_member_use // TODO: migrate to RadioGroup APIs.

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
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

    final defaultModel = _models.firstWhere(
      (m) => m.isDefault,
      orElse: () => _models.first,
    );
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
                () => ListTile(
                  title: Text(l10n.modelLabel),
                  subtitle: Text(
                    _selectedModel.value.isEmpty
                        ? l10n.modelNotSelected
                        : _selectedModel.value,
                  ),
                  leading: const Icon(Icons.psychology),
                  trailing: _isLoadingModels
                      ? const SizedBox(
                          width: 16,
                          height: 16,
                          child: CircularProgressIndicator(strokeWidth: 2),
                        )
                      : const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: _models.isEmpty
                      ? null
                      : () {
                          unawaited(
                            Get.dialog<void>(
                              AlertDialog(
                                title: Text(l10n.selectModelTitle),
                                content: SizedBox(
                                  width: double.maxFinite,
                                  child: ListView.builder(
                                    shrinkWrap: true,
                                    itemCount: _models.length,
                                    itemBuilder: (context, index) {
                                      final model = _models[index];
                                      return RadioListTile<String>(
                                        title: Text(model.displayName),
                                        subtitle: Text(
                                          '${model.provider}: ${model.modelId}',
                                        ),
                                        value: model.id,
                                        groupValue: _selectedModel.value,
                                        onChanged: (value) {
                                          if (value != null) {
                                            _selectedModel.value = value;
                                            Pref.selectedModel = value;
                                            Get.back<void>();
                                          }
                                        },
                                      );
                                    },
                                  ),
                                ),
                              ),
                            ),
                          );
                        },
                ),
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
