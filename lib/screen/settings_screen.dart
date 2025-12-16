import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final RxBool _isDarkMode = Get.isDarkMode.obs;
  final RxString _selectedModel = 'deepseek-r1-distill-qwen-7b'.obs;
  final RxBool _speechEnabled = true.obs;
  final RxBool _markdownEnabled = true.obs;

  @override
  void initState() {
    super.initState();
    _isDarkMode.value = Get.isDarkMode;
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
                  subtitle: Text(_selectedModel.value),
                  leading: const Icon(Icons.psychology),
                  trailing: const Icon(Icons.arrow_forward_ios, size: 16),
                  onTap: () {
                    unawaited(
                      Get.dialog<void>(
                        AlertDialog(
                          title: const Text('Select Model'),
                          content: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              RadioListTile<String>(
                                title: const Text('DeepSeek R1 Distill'),
                                subtitle: const Text('Fast and efficient'),
                                value: 'deepseek-r1-distill-qwen-7b',
                                // Deprecated API - waiting for RadioGroup
                                // ignore: deprecated_member_use
                                groupValue: _selectedModel.value,
                                // Deprecated API - waiting for RadioGroup
                                // ignore: deprecated_member_use
                                onChanged: (value) {
                                  if (value != null) {
                                    _selectedModel.value = value;
                                    Get.back<void>();
                                  }
                                },
                              ),
                              RadioListTile<String>(
                                title: const Text('DeepSeek R1'),
                                subtitle: const Text('More capable'),
                                value: 'deepseek-r1',
                                // Deprecated API - waiting for RadioGroup
                                // ignore: deprecated_member_use
                                groupValue: _selectedModel.value,
                                // Deprecated API - waiting for RadioGroup
                                // ignore: deprecated_member_use
                                onChanged: (value) {
                                  if (value != null) {
                                    _selectedModel.value = value;
                                    Get.back<void>();
                                  }
                                },
                              ),
                            ],
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
