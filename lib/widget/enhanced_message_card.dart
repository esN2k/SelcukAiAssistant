import 'dart:async';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:intl/intl.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';

class EnhancedMessageCard extends StatelessWidget {
  const EnhancedMessageCard({
    required this.message,
    super.key,
  });

  final ChatMessage message;

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
                      SelectableText(
                        message.content,
                        style: const TextStyle(fontSize: 15, height: 1.5),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 4),

                // Timestamp and actions
                Row(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    Text(
                      _formatTime(context, message.timestamp),
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
                    GestureDetector(
                      onTap: () => _copyToClipboard(context),
                      child: Icon(
                        Icons.copy,
                        size: 14,
                        color: Theme.of(context)
                            .textTheme
                            .bodySmall
                            ?.color
                            ?.withValues(alpha: 0.5),
                      ),
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
