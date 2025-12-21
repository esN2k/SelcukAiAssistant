// ignore_for_file: deprecated_member_use // TODO: migrate to RadioGroup APIs.

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
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
    final confirmed = await Get.dialog<bool>(
      AlertDialog(
        title: const Text('Clear All Data'),
        content: const Text(
          'Are you sure you want to delete all conversations? '
          'This action cannot be undone.',
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back(result: false),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Get.back(result: true),
            child: const Text(
              'Delete All',
              style: TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirmed ?? false) {
      await ConversationService.clearAll();
      if (mounted) {
        Get.snackbar(
          'Success',
          'All conversations deleted',
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    }
  }

  Widget _buildSection(String title, List<Widget> children) {
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
              color: Colors.amber.shade700,
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
    final stats = ConversationService.getStatistics();

    return Scaffold(
      appBar: AppBar(
        title: const Text('Settings'),
        centerTitle: true,
      ),
      body: ListView(
        children: [
          // Appearance Section
          _buildSection(
            'APPEARANCE',
            [
              Obx(
                () => SwitchListTile(
                  title: const Text('Dark Mode'),
                  subtitle: const Text('Toggle between light and dark theme'),
                  value: _isDarkMode.value,
                  activeThumbColor: Colors.amber,
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

          // AI Model Section
          _buildSection(
            'AI MODEL',
            [
              Obx(
                () => ListTile(
                  title: const Text('Model'),
                  subtitle: Text(
                    _selectedModel.value.isEmpty
                        ? 'Not selected'
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
                                title: const Text('Select Model'),
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
            'CHAT SETTINGS',
            [
              Obx(
                () => SwitchListTile(
                  title: const Text('Voice Input'),
                  subtitle: const Text('Enable microphone for voice messages'),
                  value: _speechEnabled.value,
                  activeThumbColor: Colors.amber,
                  onChanged: (value) {
                    _speechEnabled.value = value;
                  },
                  secondary: const Icon(Icons.mic),
                ),
              ),
              const Divider(height: 1),
              Obx(
                () => SwitchListTile(
                  title: const Text('Markdown Support'),
                  subtitle: const Text('Render formatted text and code'),
                  value: _markdownEnabled.value,
                  activeThumbColor: Colors.amber,
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
            'STATISTICS',
            [
              ListTile(
                title: const Text('Total Conversations'),
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
                title: const Text('Total Messages'),
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
            'DATA MANAGEMENT',
            [
              ListTile(
                title: const Text('Clear All Conversations'),
                subtitle: const Text('Delete all chat history'),
                leading: const Icon(Icons.delete_forever, color: Colors.red),
                trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                onTap: _clearAllData,
              ),
            ],
          ),

          // About Section
          _buildSection(
            'ABOUT',
            [
              const ListTile(
                title: Text('Version'),
                trailing: Text('1.0.2'),
                leading: Icon(Icons.info),
              ),
              const Divider(height: 1),
              const ListTile(
                title: Text('Developer'),
                trailing: Text('Selcuk AI'),
                leading: Icon(Icons.person),
              ),
            ],
          ),

          const SizedBox(height: 32),
        ],
      ),
    );
  }
}
