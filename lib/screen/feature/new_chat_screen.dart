// Using deprecated withOpacity and other Material 2 APIs until migration
// ignore_for_file: deprecated_member_use

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/controller/enhanced_chat_controller.dart';
import 'package:selcukaiassistant/screen/auth/login_screen.dart';
import 'package:selcukaiassistant/services/appwrite_service.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';
import 'package:selcukaiassistant/services/image_picker_service.dart';
import 'package:selcukaiassistant/widget/conversation_list_drawer.dart';
import 'package:selcukaiassistant/widget/enhanced_message_card.dart';

class NewChatScreen extends StatefulWidget {
  const NewChatScreen({super.key});

  @override
  State<NewChatScreen> createState() => _NewChatScreenState();
}

class _NewChatScreenState extends State<NewChatScreen> {
  late EnhancedChatController _controller;
  final RxBool _isDarkMode = Get.isDarkMode.obs;
  final _appwriteService = AppwriteService();
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  @override
  void initState() {
    super.initState();
    _controller = Get.put(EnhancedChatController());
    _isDarkMode.value = Get.isDarkMode;

    // Initialize conversation service
    unawaited(ConversationService.init());
  }

  Future<void> _logout() async {
    try {
      await _appwriteService.deleteCurrentSession();
      if (mounted) {
        unawaited(Get.offAll<void>(() => const LoginScreen()));
        Get.snackbar(
          'Success',
          'Logged out successfully',
          backgroundColor: Colors.green,
          colorText: Colors.white,
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } on Exception catch (e) {
      if (mounted) {
        Get.snackbar(
          'Error',
          e.toString().replaceAll('Exception: ', ''),
          backgroundColor: Colors.red,
          colorText: Colors.white,
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      key: _scaffoldKey,
      drawer: Obx(
        () => ConversationListDrawer(
          currentConversationId: _controller.currentConversationId.value,
          onConversationSelected: (id) {
            unawaited(_controller.loadConversation(id));
          },
        ),
      ),
      appBar: AppBar(
        leading: IconButton(
          icon: const Icon(Icons.menu),
          onPressed: () {
            _scaffoldKey.currentState?.openDrawer();
          },
        ),
        title: Obx(
          () => Text(
            _controller.currentConversation.value?.title ?? 'New Chat',
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
          ),
        ),
        centerTitle: true,
        elevation: 1,
        actions: [
          // Dark mode toggle
          IconButton(
            padding: const EdgeInsets.only(right: 10),
            onPressed: () {
              final newMode =
                  _isDarkMode.value ? ThemeMode.light : ThemeMode.dark;
              Get.changeThemeMode(newMode);
              _isDarkMode.value = !_isDarkMode.value;
            },
            icon: Obx(
              () => Icon(
                _isDarkMode.value
                    ? Icons.brightness_2_rounded
                    : Icons.brightness_5_rounded,
                size: 24,
              ),
            ),
          ),
          // More options
          PopupMenuButton<String>(
            icon: const Icon(Icons.more_vert),
            onSelected: (value) {
              if (value == 'logout') {
                unawaited(_logout());
              } else if (value == 'clear') {
                unawaited(_controller.clearCurrentConversation());
              } else if (value == 'export') {
                unawaited(_controller.exportCurrentConversation());
              }
            },
            itemBuilder: (context) => [
              const PopupMenuItem(
                value: 'clear',
                child: Row(
                  children: [
                    Icon(Icons.delete_sweep, size: 20),
                    SizedBox(width: 12),
                    Text('Clear Chat'),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'export',
                child: Row(
                  children: [
                    Icon(Icons.download, size: 20),
                    SizedBox(width: 12),
                    Text('Export Chat'),
                  ],
                ),
              ),
              const PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    Icon(Icons.logout, size: 20, color: Colors.red),
                    SizedBox(width: 12),
                    Text('Logout', style: TextStyle(color: Colors.red)),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      bottomNavigationBar: Container(
        padding: EdgeInsets.only(
          left: 16,
          right: 16,
          bottom: MediaQuery.of(context).viewInsets.bottom + 16,
          top: 16,
        ),
        decoration: BoxDecoration(
          color: Theme.of(context).scaffoldBackgroundColor,
          border: Border(
            top: BorderSide(
              color: Theme.of(context).dividerColor,
              width: 0.5,
            ),
          ),
        ),
        child: SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              // Listening indicator
              Obx(
                () => _controller.isListening.value
                    ? Container(
                        width: double.infinity,
                        padding: const EdgeInsets.all(12),
                        margin: const EdgeInsets.only(bottom: 12),
                        decoration: BoxDecoration(
                          color: Colors.red.withValues(alpha: 0.1),
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(
                            color: Colors.red.withValues(alpha: 0.3),
                          ),
                        ),
                        child: const Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(Icons.mic, color: Colors.red, size: 16),
                            SizedBox(width: 8),
                            Text(
                              'Listening... (Release to stop)',
                              style: TextStyle(
                                color: Colors.red,
                                fontSize: 14,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ],
                        ),
                      )
                    : const SizedBox.shrink(),
              ),

              // Input row
              Row(
                children: [
                  Obx(
                    () => GestureDetector(
                      onTapDown: (_) => _controller.startListening(),
                      onTapUp: (_) => _controller.stopListening(),
                      onTapCancel: _controller.stopListening,
                      child: Container(
                        width: 48,
                        height: 48,
                        decoration: BoxDecoration(
                          color: _controller.isListening.value
                              ? Colors.red.withValues(alpha: 0.1)
                              : Colors.amber.withValues(alpha: 0.1),
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: _controller.isListening.value
                                ? Colors.red
                                : Colors.amber,
                            width: 2,
                          ),
                        ),
                        child: Icon(
                          _controller.isListening.value
                              ? Icons.mic
                              : Icons.mic_none,
                          color: _controller.isListening.value
                              ? Colors.red
                              : Colors.amber,
                          size: 24,
                        ),
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Expanded(
                    child: Container(
                      decoration: BoxDecoration(
                        color: Theme.of(context).brightness == Brightness.dark
                            ? Colors.grey[800]
                            : Colors.grey[100],
                        borderRadius: BorderRadius.circular(24),
                      ),
                      child: Row(
                        children: [
                          // Image attachment button
                          IconButton(
                            icon: const Icon(Icons.image, size: 20),
                            onPressed: () async {
                              final image = await ImagePickerService
                                  .showImageSourceDialog();
                              if (image != null && mounted) {
                                Get.snackbar(
                                  'Image Selected',
                                  'Image: ${image.path.split('/').last}',
                                  snackPosition: SnackPosition.BOTTOM,
                                );
                              }
                            },
                            color: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.color
                                ?.withOpacity(0.6),
                          ),
                          Expanded(
                            child: TextFormField(
                              controller: _controller.textC,
                              maxLines: null,
                              textInputAction: TextInputAction.send,
                              onFieldSubmitted: (_) =>
                                  _controller.sendMessage(),
                              decoration: InputDecoration(
                                hintText: 'Message AI Assistant...',
                                hintStyle: TextStyle(
                                  fontSize: 14,
                                  color: Theme.of(context)
                                      .textTheme
                                      .bodyMedium
                                      ?.color
                                      ?.withOpacity(0.6),
                                ),
                                border: InputBorder.none,
                                contentPadding: const EdgeInsets.symmetric(
                                  horizontal: 16,
                                  vertical: 12,
                                ),
                              ),
                            ),
                          ),
                        ],
                      ),
                    ),
                  ),
                  const SizedBox(width: 12),
                  Obx(
                    () => GestureDetector(
                      onTap: _controller.isGenerating.value
                          ? _controller.stopGeneration
                          : _controller.sendMessage,
                      child: Container(
                        width: 48,
                        height: 48,
                        decoration: BoxDecoration(
                          color: _controller.isGenerating.value
                              ? Colors.red
                              : Colors.amber,
                          shape: BoxShape.circle,
                        ),
                        child: Icon(
                          _controller.isGenerating.value
                              ? Icons.stop
                              : Icons.send_rounded,
                          color: Colors.white,
                          size: 20,
                        ),
                      ),
                    ),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
      body: Obx(
        () => Column(
          children: [
            Expanded(
              child: _controller.messages.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.chat_bubble_outline,
                            size: 80,
                            color: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.color
                                ?.withOpacity(0.2),
                          ),
                          const SizedBox(height: 24),
                          Text(
                            'Start a conversation',
                            style: TextStyle(
                              fontSize: 20,
                              fontWeight: FontWeight.w600,
                              color: Theme.of(context)
                                  .textTheme
                                  .bodyMedium
                                  ?.color
                                  ?.withOpacity(0.7),
                            ),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            'Ask me anything!',
                            style: TextStyle(
                              fontSize: 14,
                              color: Theme.of(context)
                                  .textTheme
                                  .bodySmall
                                  ?.color
                                  ?.withOpacity(0.5),
                            ),
                          ),
                          const SizedBox(height: 32),
                          // Suggested prompts
                          Wrap(
                            spacing: 8,
                            runSpacing: 8,
                            alignment: WrapAlignment.center,
                            children: [
                              _SuggestedPrompt(
                                text: 'Explain quantum computing',
                                icon: Icons.science,
                                onTap: () {
                                  _controller.textC.text =
                                      'Explain quantum computing';
                                  unawaited(_controller.sendMessage());
                                },
                              ),
                              _SuggestedPrompt(
                                text: 'Write a poem',
                                icon: Icons.edit,
                                onTap: () {
                                  _controller.textC.text =
                                      'Write a short poem about nature';
                                  unawaited(_controller.sendMessage());
                                },
                              ),
                              _SuggestedPrompt(
                                text: 'Help with code',
                                icon: Icons.code,
                                onTap: () {
                                  _controller.textC.text =
                                      'Help me write a Flutter widget';
                                  unawaited(_controller.sendMessage());
                                },
                              ),
                            ],
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      physics: const BouncingScrollPhysics(),
                      controller: _controller.scrollC,
                      padding: const EdgeInsets.only(
                        top: 16,
                        bottom: 16,
                      ),
                      itemCount: _controller.messages.length,
                      itemBuilder: (context, index) {
                        return EnhancedMessageCard(
                          message: _controller.messages[index],
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}

class _SuggestedPrompt extends StatelessWidget {
  const _SuggestedPrompt({
    required this.text,
    required this.icon,
    required this.onTap,
  });

  final String text;
  final IconData icon;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 10),
        decoration: BoxDecoration(
          color: Theme.of(context).brightness == Brightness.dark
              ? Colors.grey[800]
              : Colors.grey[100],
          borderRadius: BorderRadius.circular(20),
          border: Border.all(
            color: Theme.of(context).dividerColor,
          ),
        ),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 16),
            const SizedBox(width: 8),
            Text(
              text,
              style: const TextStyle(fontSize: 13),
            ),
          ],
        ),
      ),
    );
  }
}
