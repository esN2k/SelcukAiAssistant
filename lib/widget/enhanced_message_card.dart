import 'dart:async';
import 'dart:collection';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/widget/markdown_message_view.dart';
import 'package:selcukaiassistant/widget/typing_indicator.dart';

class EnhancedMessageCard extends StatelessWidget {
  const EnhancedMessageCard({
    required this.message,
    this.onEdit,
    this.onRegenerate,
    this.onRetry,
    this.showTypingIndicator = false,
    super.key,
  });

  final ChatMessage message;
  final VoidCallback? onEdit;
  final VoidCallback? onRegenerate;
  final VoidCallback? onRetry;
  final bool showTypingIndicator;

  void _copyToClipboard(BuildContext context) {
    unawaited(Clipboard.setData(ClipboardData(text: message.content)));
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(context.l10n.copiedToClipboard),
        duration: const Duration(seconds: 2),
        behavior: SnackBarBehavior.floating,
      ),
    );
  }

  Widget _buildActionIcon({
    required BuildContext context,
    required IconData icon,
    required String tooltip,
    required VoidCallback onPressed,
  }) {
    final color = Theme.of(context)
        .textTheme
        .bodySmall
        ?.color
        ?.withValues(alpha: 0.6);
    return IconButton(
      tooltip: tooltip,
      onPressed: onPressed,
      iconSize: 16,
      padding: EdgeInsets.zero,
      constraints: const BoxConstraints(
        minWidth: 24,
        minHeight: 24,
      ),
      icon: Icon(icon, color: color),
    );
  }

  Widget _buildSources(BuildContext context) {
    final theme = Theme.of(context);
    final l10n = context.l10n;
    final citations =
        LinkedHashSet<String>.from(message.citations).toList();

    if (citations.isEmpty) {
      return const SizedBox.shrink();
    }

    return Container(
      margin: const EdgeInsets.only(top: 8),
      padding: const EdgeInsets.all(10),
      decoration: BoxDecoration(
        color: theme.colorScheme.surfaceContainerHighest
            .withValues(alpha: 0.5),
        borderRadius: BorderRadius.circular(12),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            l10n.sourcesTitle,
            style: theme.textTheme.labelLarge?.copyWith(
              fontWeight: FontWeight.w600,
            ),
          ),
          const SizedBox(height: 6),
          ...citations.map(
            (item) => Padding(
              padding: const EdgeInsets.only(bottom: 4),
              child: Text(
                '• $item',
                style: theme.textTheme.bodySmall,
              ),
            ),
          ),
        ],
      ),
    );
  }

  String _formatTime(BuildContext context, DateTime timestamp) {
    final l10n = context.l10n;
    final locale = Localizations.localeOf(context).languageCode;
    final now = DateTime.now();
    final difference = now.difference(timestamp);

    if (difference.inDays == 0) {
      return DateFormat('HH:mm', locale).format(timestamp);
    } else if (difference.inDays == 1) {
      return l10n.yesterdayAt(DateFormat('HH:mm', locale).format(timestamp));
    } else if (difference.inDays < 7) {
      return DateFormat('EEEE HH:mm', locale).format(timestamp);
    } else {
      return DateFormat('MMM d, HH:mm', locale).format(timestamp);
    }
  }

  @override
  Widget build(BuildContext context) {
    final isUser = message.isUser;
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final markdownEnabled = Pref.markdownEnabled;

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (!isUser) ...[
            CircleAvatar(
              radius: 16,
              backgroundColor: Colors.amber.withValues(alpha: 0.2),
              child: const Icon(
                Icons.smart_toy_outlined,
                size: 18,
                color: Colors.amber,
              ),
            ),
            const SizedBox(width: 12),
          ],
          Expanded(
            child: Column(
              crossAxisAlignment:
                  isUser ? CrossAxisAlignment.end : CrossAxisAlignment.start,
              children: [
                // Message bubble
                Container(
                  padding: const EdgeInsets.all(12),
                  decoration: BoxDecoration(
                    color: isUser
                        ? Colors.amber.withValues(alpha: isDark ? 0.2 : 0.15)
                        : (isDark ? Colors.grey[800] : Colors.grey[100]),
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      if (message.imageUrl != null) ...[
                        ClipRRect(
                          borderRadius: BorderRadius.circular(8),
                          child: Image.network(
                            message.imageUrl!,
                            fit: BoxFit.cover,
                            errorBuilder: (context, error, stackTrace) =>
                                const Icon(Icons.broken_image, size: 50),
                          ),
                        ),
                        const SizedBox(height: 8),
                      ],
                      if (message.isUser)
                        SelectableText(
                          message.content,
                          style: const TextStyle(fontSize: 15, height: 1.5),
                        )
                      else if (message.content.trim().isEmpty &&
                          showTypingIndicator)
                        Row(
                          children: [
                            const TypingIndicator(),
                            const SizedBox(width: 12),
                            Text(
                              context.l10n.aiThinking,
                              style: const TextStyle(
                                fontSize: 14,
                                fontStyle: FontStyle.italic,
                              ),
                            ),
                          ],
                        )
                      else if (markdownEnabled)
                        MarkdownMessageView(data: message.content)
                      else
                        SelectableText(
                          message.content,
                          style: const TextStyle(fontSize: 15, height: 1.5),
                        ),
                      if (!message.isUser && message.hasError)
                        Padding(
                          padding: const EdgeInsets.only(top: 8),
                          child: Text(
                            message.error ?? '',
                            style: const TextStyle(
                              color: Colors.redAccent,
                              fontSize: 12,
                            ),
                          ),
                        ),
                    ],
                  ),
                ),
                if (!message.isUser && message.citations.isNotEmpty)
                  _buildSources(context),
                const SizedBox(height: 4),

                // Timestamp and actions
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      _formatTime(context, message.createdAt),
                      style: TextStyle(
                        fontSize: 11,
                        color: Theme.of(context)
                            .textTheme
                            .bodySmall
                            ?.color
                            ?.withValues(alpha: 0.6),
                      ),
                    ),
                    const SizedBox(width: 8),
                    Wrap(
                      spacing: 4,
                      children: [
                        if (onEdit != null)
                          _buildActionIcon(
                            context: context,
                            icon: Icons.edit,
                            tooltip: context.l10n.editMessageTitle,
                            onPressed: onEdit!,
                          ),
                        if (onRegenerate != null)
                          _buildActionIcon(
                            context: context,
                            icon: Icons.refresh,
                            tooltip: context.l10n.regenerateAction,
                            onPressed: onRegenerate!,
                          ),
                        if (onRetry != null)
                          _buildActionIcon(
                            context: context,
                            icon: Icons.replay,
                            tooltip: context.l10n.retryAction,
                            onPressed: onRetry!,
                          ),
                        _buildActionIcon(
                          context: context,
                          icon: Icons.copy,
                          tooltip: context.l10n.copyAction,
                          onPressed: () => _copyToClipboard(context),
                        ),
                      ],
                    ),
                  ],
                ),
              ],
            ),
          ),
          if (isUser) ...[
            const SizedBox(width: 12),
            CircleAvatar(
              radius: 16,
              backgroundColor: Colors.amber.withValues(alpha: 0.2),
              child: const Icon(
                Icons.person_outline,
                size: 18,
                color: Colors.amber,
              ),
            ),
          ],
        ],
      ),
    );
  }
}
