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
      final query = _searchController.text.trim();
      if (query.isNotEmpty) {
        _filteredConversations =
            ConversationService.searchConversations(query);
        _isSearching = true;
      } else {
        _filteredConversations = ConversationService.getAllConversations();
        _isSearching = false;
      }
    });
  }

  void _searchConversations(String query) {
    setState(() {
      if (query.isEmpty) {
        _filteredConversations = ConversationService.getAllConversations();
        _isSearching = false;
      } else {
        _filteredConversations =
            ConversationService.searchConversations(query);
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

  Future<void> _setPinned(Conversation conversation, bool pinned) async {
    await ConversationService.setPinned(
      conversation.id,
      pinned: pinned,
    );
    _loadConversations();
  }

  Future<void> _setArchived(Conversation conversation, bool archived) async {
    await ConversationService.setArchived(
      conversation.id,
      archived: archived,
    );
    _loadConversations();

    if (archived && conversation.id == widget.currentConversationId) {
      final newConversation = await ConversationService.createConversation();
      widget.onConversationSelected(newConversation.id);
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

  Widget _buildSectionHeader(AppLocalizations l10n, String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 12, 16, 6),
      child: Text(
        title,
        style: TextStyle(
          fontSize: 12,
          fontWeight: FontWeight.w600,
          color: Theme.of(context)
              .textTheme
              .bodySmall
              ?.color
              ?.withValues(alpha: 0.6),
        ),
      ),
    );
  }

  Widget _buildConversationTile(
    AppLocalizations l10n,
    Conversation conversation,
  ) {
    final isSelected = conversation.id == widget.currentConversationId;
    final accentColor = Theme.of(context).primaryColor;

    return Container(
      margin: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: isSelected ? accentColor.withValues(alpha: 0.05) : null,
        borderRadius: BorderRadius.circular(8),
      ),
      child: ListTile(
        selected: isSelected,
        leading: Icon(
          conversation.archived
              ? Icons.archive_outlined
              : Icons.chat_bubble_outline,
          color: isSelected ? accentColor : null,
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
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (conversation.pinned)
              Icon(
                Icons.push_pin,
                size: 16,
                color: accentColor,
              ),
            if (conversation.archived)
              Padding(
                padding: const EdgeInsets.only(left: 6),
                child: Icon(
                  Icons.archive_outlined,
                  size: 16,
                  color: Theme.of(context)
                      .textTheme
                      .bodySmall
                      ?.color
                      ?.withValues(alpha: 0.6),
                ),
              ),
            PopupMenuButton<String>(
              icon: const Icon(Icons.more_vert),
              onSelected: (value) {
                if (value == 'pin') {
                  unawaited(_setPinned(conversation, true));
                } else if (value == 'unpin') {
                  unawaited(_setPinned(conversation, false));
                } else if (value == 'archive') {
                  unawaited(_setArchived(conversation, true));
                } else if (value == 'unarchive') {
                  unawaited(_setArchived(conversation, false));
                } else if (value == 'rename') {
                  unawaited(_renameConversation(conversation));
                } else if (value == 'delete') {
                  unawaited(_deleteConversation(conversation.id));
                }
              },
              itemBuilder: (context) {
                final items = <PopupMenuEntry<String>>[];
                if (!conversation.archived) {
                  items.add(
                    PopupMenuItem(
                      value: conversation.pinned ? 'unpin' : 'pin',
                      child: Row(
                        children: [
                          Icon(
                            Icons.push_pin,
                            size: 20,
                            color: accentColor,
                          ),
                          const SizedBox(width: 12),
                          Text(
                            conversation.pinned
                                ? l10n.unpinConversation
                                : l10n.pinConversation,
                          ),
                        ],
                      ),
                    ),
                  );
                }
                items
                  ..add(
                    PopupMenuItem(
                      value: conversation.archived ? 'unarchive' : 'archive',
                      child: Row(
                        children: [
                          const Icon(Icons.archive_outlined, size: 20),
                          const SizedBox(width: 12),
                          Text(
                            conversation.archived
                                ? l10n.unarchiveConversation
                                : l10n.archiveConversation,
                          ),
                        ],
                      ),
                    ),
                  )
                  ..add(const PopupMenuDivider())
                  ..add(
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
                  )
                  ..add(
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
                            style: const TextStyle(color: Colors.red),
                          ),
                        ],
                      ),
                    ),
                  );
                return items;
              },
            ),
          ],
        ),
        onTap: () {
          widget.onConversationSelected(conversation.id);
          Navigator.pop(context);
        },
      ),
    );
  }

  List<Widget> _buildGroupedChildren(AppLocalizations l10n) {
    final pinned = <Conversation>[];
    final today = <Conversation>[];
    final yesterday = <Conversation>[];
    final last7Days = <Conversation>[];
    final older = <Conversation>[];
    final archived = <Conversation>[];
    final now = DateTime.now();

    for (final conversation in _filteredConversations) {
      if (conversation.archived) {
        archived.add(conversation);
        continue;
      }
      if (conversation.pinned) {
        pinned.add(conversation);
        continue;
      }

      final days = now.difference(conversation.updatedAt).inDays;
      if (days == 0) {
        today.add(conversation);
      } else if (days == 1) {
        yesterday.add(conversation);
      } else if (days < 7) {
        last7Days.add(conversation);
      } else {
        older.add(conversation);
      }
    }

    void sortByUpdated(List<Conversation> items) {
      items.sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    }

    sortByUpdated(pinned);
    sortByUpdated(today);
    sortByUpdated(yesterday);
    sortByUpdated(last7Days);
    sortByUpdated(older);
    sortByUpdated(archived);

    final children = <Widget>[];

    void addSection(String title, List<Conversation> items) {
      if (items.isEmpty) {
        return;
      }
      children
        ..add(_buildSectionHeader(l10n, title))
        ..addAll(items.map((c) => _buildConversationTile(l10n, c)))
        ..add(const SizedBox(height: 4));
    }

    addSection(l10n.pinnedLabel, pinned);
    addSection(l10n.todayLabel, today);
    addSection(l10n.yesterdayLabel, yesterday);
    addSection(l10n.last7DaysLabel, last7Days);
    addSection(l10n.olderLabel, older);

    if (archived.isNotEmpty) {
      children.add(
        Theme(
          data: Theme.of(context).copyWith(
            dividerColor: Colors.transparent,
          ),
          child: ExpansionTile(
            tilePadding: const EdgeInsets.symmetric(horizontal: 16),
            childrenPadding: const EdgeInsets.only(bottom: 8),
            title: Text(
              '${l10n.archivedLabel} (${archived.length})',
              style: TextStyle(
                fontSize: 12,
                fontWeight: FontWeight.w600,
                color: Theme.of(context)
                    .textTheme
                    .bodySmall
                    ?.color
                    ?.withValues(alpha: 0.6),
              ),
            ),
            children: archived
                .map(
                  (conversation) =>
                      _buildConversationTile(l10n, conversation),
                )
                .toList(),
          ),
        ),
      );
    }

    return children;
  }

  Widget _buildSearchResults(AppLocalizations l10n) {
    return ListView.builder(
      itemCount: _filteredConversations.length,
      itemBuilder: (context, index) {
        final conversation = _filteredConversations[index];
        return _buildConversationTile(l10n, conversation);
      },
    );
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
                  : _isSearching
                      ? _buildSearchResults(l10n)
                      : ListView(
                          children: _buildGroupedChildren(l10n),
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
