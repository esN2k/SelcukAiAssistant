// Geçici olarak Material 2 API'lerindeki withOpacity kullanımını sürdürüyoruz.
// ignore_for_file: deprecated_member_use

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/controller/enhanced_chat_controller.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
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
    _controller = Get.put<EnhancedChatController>(
      EnhancedChatController(),
    );
    _isDarkMode.value = Get.isDarkMode;

    // Sohbet verilerini hazırlamak için servis başlatılır.
    unawaited(ConversationService.init());
  }

  String _displayTitle(BuildContext context, String? title) {
    final l10n = context.l10n;
    if (title == null || title.trim().isEmpty) {
      return l10n.newChat;
    }
    const defaults = {'New Chat', 'Yeni sohbet'};
    if (defaults.contains(title)) {
      return l10n.newChat;
    }
    return title;
  }

  Future<void> _logout() async {
    final l10n = L10n.current();
    try {
      await _appwriteService.deleteCurrentSession();
      if (mounted) {
        unawaited(Get.offAll<void>(() => const LoginScreen()));
        Get.snackbar(
          l10n?.logoutSuccessTitle ?? 'Başarılı',
          l10n?.logoutSuccessMessage ?? 'Oturum başarıyla kapatıldı',
          backgroundColor: Colors.green,
          colorText: Colors.white,
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } on Exception catch (e) {
      if (mounted) {
        Get.snackbar(
          l10n?.logoutErrorTitle ?? 'Hata',
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
    final l10n = context.l10n;
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
          () {
            final title = _displayTitle(
              context,
              _controller.currentConversation.value?.title,
            );
            return Text(
              title,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
            );
          },
        ),
        centerTitle: true,
        elevation: 1,
        actions: [
          // Koyu/açık tema geçişi
          IconButton(
            padding: const EdgeInsets.only(right: 10),
            onPressed: () {
              final newMode =
                  _isDarkMode.value ? ThemeMode.light : ThemeMode.dark;
              Get.changeThemeMode(newMode);
              _isDarkMode.value = !_isDarkMode.value;
              Pref.isDarkMode = _isDarkMode.value;
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
          // Ek seçenekler
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
              PopupMenuItem(
                value: 'clear',
                child: Row(
                  children: [
                    const Icon(Icons.delete_sweep, size: 20),
                    const SizedBox(width: 12),
                    Text(l10n.clearChat),
                  ],
                ),
              ),
              PopupMenuItem(
                value: 'export',
                child: Row(
                  children: [
                    const Icon(Icons.download, size: 20),
                    const SizedBox(width: 12),
                    Text(l10n.exportChat),
                  ],
                ),
              ),
              PopupMenuItem(
                value: 'logout',
                child: Row(
                  children: [
                    const Icon(Icons.logout, size: 20, color: Colors.red),
                    const SizedBox(width: 12),
                    Text(
                      l10n.logout,
                      style: const TextStyle(color: Colors.red),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ],
      ),
      // Alt giriş alanı: sesli giriş, metin alanı ve gönder/durdur kontrolü.
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
              // Dinleme durum göstergesi
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
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            const Icon(Icons.mic, color: Colors.red, size: 16),
                            const SizedBox(width: 8),
                            Text(
                              l10n.listeningIndicator,
                              style: const TextStyle(
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

              // Mesaj giriş satırı
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
                              : Theme.of(context)
                                  .colorScheme
                                  .primary
                                  .withValues(alpha: 0.1),
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: _controller.isListening.value
                                ? Colors.red
                                : Theme.of(context).colorScheme.primary,
                            width: 2,
                          ),
                        ),
                        child: Icon(
                          _controller.isListening.value
                              ? Icons.mic
                              : Icons.mic_none,
                          color: _controller.isListening.value
                              ? Colors.red
                              : Theme.of(context).colorScheme.primary,
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
                          // Görsel ekleme düğmesi
                          IconButton(
                            icon: const Icon(Icons.image, size: 20),
                            onPressed: () async {
                              final image = await ImagePickerService
                                  .showImageSourceDialog();
                              if (image != null && mounted) {
                                final fileName = image.name.isNotEmpty
                                    ? image.name
                                    : image.path.split('/').last;
                                Get.snackbar(
                                  l10n.imageSelectedTitle,
                                  l10n.imageSelectedMessage(
                                    fileName,
                                  ),
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
                              onFieldSubmitted: (_) {
                                unawaited(_controller.sendMessage());
                              },
                              decoration: InputDecoration(
                                hintText: l10n.messageHint,
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
                              : Theme.of(context).colorScheme.primary,
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
                            l10n.startConversationTitle,
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
                            l10n.startConversationSubtitle,
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
                          // Önerilen başlangıç soruları
                          //(kullanıcıyı yönlendirmek için).
                          Wrap(
                            spacing: 8,
                            runSpacing: 8,
                            alignment: WrapAlignment.center,
                            children: [
                              _SuggestedPrompt(
                                text: l10n.suggestedPrompt1,
                                icon: Icons.science,
                                onTap: () {
                                  _controller.textC.text =
                                      l10n.suggestedPrompt1;
                                  unawaited(_controller.sendMessage());
                                },
                              ),
                              _SuggestedPrompt(
                                text: l10n.suggestedPrompt2,
                                icon: Icons.edit,
                                onTap: () {
                                  _controller.textC.text =
                                      l10n.suggestedPrompt2;
                                  unawaited(_controller.sendMessage());
                                },
                              ),
                              _SuggestedPrompt(
                                text: l10n.suggestedPrompt3,
                                icon: Icons.code,
                                onTap: () {
                                  _controller.textC.text =
                                      l10n.suggestedPrompt3;
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
                        final lastUserIndex = _controller.messages
                            .lastIndexWhere((m) => m.isUser);
                        final lastAssistantIndex = _controller.messages
                            .lastIndexWhere((m) => !m.isUser);
                        final message = _controller.messages[index];
                        final actionsEnabled = !_controller.isGenerating.value;
                        final canEdit = actionsEnabled &&
                            message.isUser &&
                            index == lastUserIndex;
                        final canRetry = actionsEnabled &&
                            !message.isUser &&
                            message.hasError;
                        final canRegenerate = actionsEnabled &&
                            !message.isUser &&
                            index == lastAssistantIndex &&
                            !message.hasError;
                        final showTypingIndicator =
                            _controller.isGenerating.value &&
                                !message.isUser &&
                                index == lastAssistantIndex &&
                                message.content.trim().isEmpty;
                        return EnhancedMessageCard(
                          message: message,
                          onEdit: canEdit
                              ? () => _controller.editLastUserMessage(message)
                              : null,
                          onRetry: canRetry
                              ? () => _controller.retryResponse(message)
                              : null,
                          onRegenerate: canRegenerate
                              ? () => _controller.regenerateResponse(message)
                              : null,
                          showTypingIndicator: showTypingIndicator,
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
