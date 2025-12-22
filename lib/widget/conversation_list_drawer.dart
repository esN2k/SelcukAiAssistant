import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/screen/settings_screen.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';

class ConversationListDrawer extends StatefulWidget {
  const ConversationListDrawer({
    required this.currentConversationId,
    required this.onConversationSelected,
    super.key,
  });

  final String? currentConversationId;
  final void Function(String conversationId) onConversationSelected;

  @override
  State<ConversationListDrawer> createState() => _ConversationListDrawerState();
}

class _ConversationListDrawerState extends State<ConversationListDrawer> {
  final TextEditingController _searchController = TextEditingController();
  List<Conversation> _filteredConversations = [];
  bool _isSearching = false;

  @override
  void initState() {
    super.initState();
    _loadConversations();
  }

  void _loadConversations() {
    setState(() {
      _filteredConversations = ConversationService.getAllConversations();
    });
  }

  void _searchConversations(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredConversations = ConversationService.getAllConversations();
        _isSearching = false;
      } else {
        _filteredConversations = ConversationService.searchConversations(query);
        _isSearching = true;
      }
    });
  }

  Future<void> _deleteConversation(String id) async {
    final l10n = context.l10n;
    final confirmed = await Get.dialog<bool>(
      AlertDialog(
        title: Text(l10n.deleteConversationTitle),
        content: Text(l10n.deleteConversationMessage),
        actions: [
          TextButton(
            onPressed: () => Get.back<bool>(result: false),
            child: Text(l10n.cancel),
          ),
          TextButton(
            onPressed: () => Get.back<bool>(result: true),
            child: Text(
              l10n.delete,
              style: const TextStyle(color: Colors.red),
            ),
          ),
        ],
      ),
    );

    if (confirmed ?? false) {
      await ConversationService.deleteConversation(id);
      _loadConversations();

      // If deleted conversation was current, start a new chat
      if (id == widget.currentConversationId) {
        final newConversation = await ConversationService.createConversation();
        widget.onConversationSelected(newConversation.id);
      }
    }
  }

  Future<void> _renameConversation(Conversation conversation) async {
    final l10n = context.l10n;
    final controller = TextEditingController(text: conversation.title);

    final newTitle = await Get.dialog<String>(
      AlertDialog(
        title: Text(l10n.renameConversationTitle),
        content: TextField(
          controller: controller,
          autofocus: true,
          decoration: InputDecoration(
            hintText: l10n.renameConversationHint,
            border: const OutlineInputBorder(),
          ),
          onSubmitted: (value) => Get.back(result: value),
        ),
        actions: [
          TextButton(
            onPressed: () => Get.back<String>(),
            child: Text(l10n.cancel),
          ),
          TextButton(
            onPressed: () => Get.back<String>(result: controller.text),
            child: Text(l10n.rename),
          ),
        ],
      ),
    );

    if (newTitle != null && newTitle.trim().isNotEmpty) {
      await ConversationService.renameConversation(
        conversation.id,
        newTitle.trim(),
      );
      _loadConversations();
    }
  }

  String _formatDate(DateTime date, AppLocalizations l10n) {
    final now = DateTime.now();
    final difference = now.difference(date);

    if (difference.inDays == 0) {
      return l10n.todayLabel;
    } else if (difference.inDays == 1) {
      return l10n.yesterdayLabel;
    } else if (difference.inDays < 7) {
      return l10n.daysAgo(difference.inDays);
    } else if (difference.inDays < 30) {
      final weeks = (difference.inDays / 7).floor();
      return l10n.weeksAgo(weeks);
    } else if (difference.inDays < 365) {
      final months = (difference.inDays / 30).floor();
      return l10n.monthsAgo(months);
    } else {
      final years = (difference.inDays / 365).floor();
      return l10n.yearsAgo(years);
    }
  }

  String _displayTitle(AppLocalizations l10n, String title) {
    const defaults = {'New Chat', 'Yeni sohbet'};
    if (defaults.contains(title)) {
      return l10n.newChat;
    }
    return title;
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    return Drawer(
      child: SafeArea(
        child: Column(
          children: [
            // Header with New Chat button
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                color: Theme.of(context).primaryColor.withValues(alpha: 0.1),
                border: Border(
                  bottom: BorderSide(
                    color: Theme.of(context).dividerColor,
                    width: 0.5,
                  ),
                ),
              ),
              child: Row(
                children: [
                  Expanded(
                    child: ElevatedButton.icon(
                      onPressed: () async {
                        final newConversation =
                            await ConversationService.createConversation();
                        widget.onConversationSelected(newConversation.id);
                        _loadConversations();
                        if (context.mounted) {
                          Navigator.pop(context);
                        }
                      },
                      icon: const Icon(Icons.add),
                      label: Text(l10n.newChat),
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Theme.of(context).colorScheme.primary,
                        foregroundColor: Colors.white,
                        padding: const EdgeInsets.symmetric(vertical: 12),
                      ),
                    ),
                  ),
                ],
              ),
            ),

            // Search bar
            Padding(
              padding: const EdgeInsets.all(12),
              child: TextField(
                controller: _searchController,
                onChanged: _searchConversations,
                decoration: InputDecoration(
                  hintText: l10n.searchConversationsHint,
                  prefixIcon: const Icon(Icons.search),
                  suffixIcon: _isSearching
                      ? IconButton(
                          icon: const Icon(Icons.clear),
                          onPressed: () {
                            _searchController.clear();
                            _searchConversations('');
                          },
                        )
                      : null,
                  border: OutlineInputBorder(
                    borderRadius: BorderRadius.circular(12),
                  ),
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 16,
                    vertical: 12,
                  ),
                ),
              ),
            ),

            // Conversations list
            Expanded(
              child: _filteredConversations.isEmpty
                  ? Center(
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Icon(
                            _isSearching
                                ? Icons.search_off
                                : Icons.chat_bubble_outline,
                            size: 64,
                            color: Theme.of(context)
                                .textTheme
                                .bodyMedium
                                ?.color
                                ?.withValues(alpha: 0.3),
                          ),
                          const SizedBox(height: 16),
                          Text(
                            _isSearching
                                ? l10n.noConversationsFound
                                : l10n.noConversationsYet,
                            style: TextStyle(
                              fontSize: 16,
                              color: Theme.of(context)
                                  .textTheme
                                  .bodyMedium
                                  ?.color
                                  ?.withValues(alpha: 0.6),
                            ),
                          ),
                        ],
                      ),
                    )
                  : ListView.builder(
                      itemCount: _filteredConversations.length,
                      itemBuilder: (context, index) {
                        final conversation = _filteredConversations[index];
                        final isSelected =
                            conversation.id == widget.currentConversationId;

                        return Container(
                          margin: const EdgeInsets.symmetric(
                            horizontal: 8,
                            vertical: 4,
                          ),
                          decoration: BoxDecoration(
                            color: isSelected
                                ? Theme.of(context)
                                    .primaryColor
                                    .withValues(alpha: 0.05)
                                : null,
                            borderRadius: BorderRadius.circular(8),
                          ),
                          child: ListTile(
                            selected: isSelected,
                            leading: Icon(
                              Icons.chat_bubble_outline,
                              color: isSelected
                                  ? Theme.of(context).primaryColor
                                  : null,
                            ),
                            title: Text(
                              _displayTitle(l10n, conversation.title),
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontWeight: isSelected ? FontWeight.w600 : null,
                              ),
                            ),
                            subtitle: Text(
                              _formatDate(conversation.updatedAt, l10n),
                              style: TextStyle(
                                fontSize: 12,
                                color: Theme.of(context)
                                    .textTheme
                                    .bodySmall
                                    ?.color
                                    ?.withValues(alpha: 0.7),
                              ),
                            ),
                            trailing: PopupMenuButton<String>(
                              icon: const Icon(Icons.more_vert),
                              onSelected: (value) {
                                if (value == 'rename') {
                                  unawaited(_renameConversation(conversation));
                                } else if (value == 'delete') {
                                  unawaited(
                                    _deleteConversation(conversation.id),
                                  );
                                }
                              },
                              itemBuilder: (context) => [
                                PopupMenuItem(
                                  value: 'rename',
                                  child: Row(
                                    children: [
                                      const Icon(Icons.edit, size: 20),
                                      const SizedBox(width: 12),
                                      Text(l10n.rename),
                                    ],
                                  ),
                                ),
                                PopupMenuItem(
                                  value: 'delete',
                                  child: Row(
                                    children: [
                                      const Icon(
                                        Icons.delete,
                                        size: 20,
                                        color: Colors.red,
                                      ),
                                      const SizedBox(width: 12),
                                      Text(
                                        l10n.delete,
                                        style: const TextStyle(
                                          color: Colors.red,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),
                              ],
                            ),
                            onTap: () {
                              widget.onConversationSelected(conversation.id);
                              Navigator.pop(context);
                            },
                          ),
                        );
                      },
                    ),
            ),

            // Footer with stats or settings
            Container(
              padding: const EdgeInsets.all(16),
              decoration: BoxDecoration(
                border: Border(
                  top: BorderSide(
                    color: Theme.of(context).dividerColor,
                    width: 0.5,
                  ),
                ),
              ),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    l10n.conversationsCount(_filteredConversations.length),
                    style: TextStyle(
                      fontSize: 12,
                      color: Theme.of(context)
                          .textTheme
                          .bodySmall
                          ?.color
                          ?.withValues(alpha: 0.6),
                    ),
                  ),
                  IconButton(
                    icon: const Icon(Icons.settings),
                    onPressed: () {
                      Navigator.pop(context);
                      unawaited(Get.to<void>(() => const SettingsScreen()));
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }
}
