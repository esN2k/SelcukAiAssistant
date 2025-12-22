// Using deprecated withOpacity and other Material 2 APIs until migration
// ignore_for_file: deprecated_member_use

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/controller/chat_controller.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/screen/auth/login_screen.dart';
import 'package:selcukaiassistant/services/appwrite_service.dart';
import 'package:selcukaiassistant/widget/message_card.dart';

class ChatBotFeature extends StatefulWidget {
  const ChatBotFeature({super.key});

  @override
  State<ChatBotFeature> createState() => _ChatBotFeatureState();
}

class _ChatBotFeatureState extends State<ChatBotFeature> {
  final _c = ChatController();
  final RxBool _isDarkMode = Get.isDarkMode.obs;
  final _appwriteService = AppwriteService();

  @override
  void initState() {
    super.initState();
    _isDarkMode.value = Get.isDarkMode;
  }

  Future<void> _sendPing() async {
    final l10n = context.l10n;
    try {
      final user = await _appwriteService.getCurrentUser();

      if (mounted) {
        if (user != null) {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(l10n.appwritePingSuccess),
              backgroundColor: Colors.green,
            ),
          );
        } else {
          ScaffoldMessenger.of(context).showSnackBar(
            SnackBar(
              content: Text(l10n.appwritePingNoSession),
              backgroundColor: Colors.orange,
            ),
          );
        }
      }
    } on Exception catch (e) {
      if (mounted) {
        final errorMessage = e.toString().replaceAll('Exception: ', '');
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text(l10n.appwritePingError(errorMessage)),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }

  Future<void> _logout() async {
    final l10n = context.l10n;
    try {
      await _appwriteService.deleteCurrentSession();
      if (mounted) {
        unawaited(Get.offAll<void>(() => const LoginScreen()));
        Get.snackbar(
          l10n.logoutSuccessTitle,
          l10n.logoutSuccessMessage,
          backgroundColor: Colors.green,
          colorText: Colors.white,
          snackPosition: SnackPosition.BOTTOM,
        );
      }
    } on Exception catch (e) {
      if (mounted) {
        Get.snackbar(
          l10n.errorTitle,
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
      appBar: AppBar(
        title: Text(l10n.assistantTitle),
        centerTitle: true,
        elevation: 1,
        actions: [
          // Appwrite ping button
          IconButton(
            padding: const EdgeInsets.only(right: 10),
            onPressed: _sendPing,
            icon: const Icon(Icons.wifi_rounded, size: 24),
            tooltip: l10n.sendPingTooltip,
          ),
          // Dark mode toggle
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
          // Logout button
          IconButton(
            padding: const EdgeInsets.only(right: 10),
            onPressed: _logout,
            icon: const Icon(Icons.logout_rounded, size: 24),
            tooltip: l10n.logoutTooltip,
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
          child: Row(
            children: [
              Obx(
                () => GestureDetector(
                  onTapDown: (_) => _c.startListening(),
                  onTapUp: (_) => _c.stopListening(),
                  onTapCancel: _c.stopListening,
                  child: Container(
                    width: 48,
                    height: 48,
                    decoration: BoxDecoration(
                      color: _c.isListening.value
                          ? Colors.red.withOpacity(0.1)
                          : Colors.amber.withOpacity(0.1),
                      shape: BoxShape.circle,
                      border: Border.all(
                        color: _c.isListening.value ? Colors.red : Colors.amber,
                        width: 2,
                      ),
                    ),
                    child: Icon(
                      _c.isListening.value ? Icons.mic : Icons.mic_none,
                      color: _c.isListening.value ? Colors.red : Colors.amber,
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
                  child: TextFormField(
                    controller: _c.textC,
                    maxLines: null,
                    textInputAction: TextInputAction.send,
                    onFieldSubmitted: (_) => _c.askQuestion(),
                    decoration: InputDecoration(
                      hintText: l10n.assistantHint,
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
              ),
              const SizedBox(width: 12),
              GestureDetector(
                onTap: _c.askQuestion,
                child: Container(
                  width: 48,
                  height: 48,
                  decoration: const BoxDecoration(
                    color: Colors.amber,
                    shape: BoxShape.circle,
                  ),
                  child: const Icon(
                    Icons.send_rounded,
                    color: Colors.white,
                    size: 20,
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
      body: Obx(
        () => Column(
          children: [
            if (_c.isListening.value)
              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(12),
                color: Colors.red.withOpacity(0.1),
                child: Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Icon(Icons.mic, color: Colors.red, size: 16),
                    const SizedBox(width: 8),
                    Text(
                      l10n.listeningStatus,
                      style: const TextStyle(
                        color: Colors.red,
                        fontSize: 14,
                        fontWeight: FontWeight.w500,
                      ),
                    ),
                  ],
                ),
              ),
            Expanded(
              child: _c.list.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            Icons.chat_bubble_outline,
                            size: 64,
                            color: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.color
                                ?.withOpacity(0.3),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            l10n.startChatHint,
                            style: TextStyle(
                              fontSize: 16,
                              color: Theme.of(context)
                                  .textTheme
                                  .bodyMedium
                                  ?.color
                                  ?.withOpacity(0.6),
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      physics: const BouncingScrollPhysics(),
                      controller: _c.scrollC,
                      padding: EdgeInsets.only(
                        top: Global.mq.height * .02,
                        bottom: 16,
                        left: 8,
                        right: 8,
                      ),
                      itemCount: _c.list.length,
                      itemBuilder: (context, index) {
                        return MessageCard(message: _c.list[index]);
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}
