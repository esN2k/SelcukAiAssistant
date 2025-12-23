import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/widget/availability_badge.dart';

class ModelCard extends StatelessWidget {
  const ModelCard({
    required this.model,
    required this.selected,
    this.onSelect,
    super.key,
  });

  final ModelInfo model;
  final bool selected;
  final VoidCallback? onSelect;

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final theme = Theme.of(context);
    final canSelect = model.available && onSelect != null;
    final command = 'ollama pull ${model.modelId}';

    return Card(
      margin: const EdgeInsets.symmetric(vertical: 6),
      child: InkWell(
        onTap: canSelect ? onSelect : null,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(12),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Row(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Expanded(
                    child: Text(
                      model.displayName,
                      style: theme.textTheme.titleMedium?.copyWith(
                        fontWeight: FontWeight.w600,
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  AvailabilityBadge(model: model),
                  if (selected) ...[
                    const SizedBox(width: 6),
                    Icon(
                      Icons.check_circle,
                      color: theme.colorScheme.primary,
                      size: 18,
                    ),
                  ],
                ],
              ),
              const SizedBox(height: 6),
              Text(
                '${model.provider.toUpperCase()} \u2022 ${model.modelId}',
                style: theme.textTheme.bodySmall?.copyWith(
                  color: theme.textTheme.bodySmall?.color?.withValues(
                        alpha: 0.7,
                      ),
                ),
              ),
              if (model.contextLength != null) ...[
                const SizedBox(height: 4),
                Text(
                  l10n.modelContextLength(model.contextLength!),
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.textTheme.bodySmall?.color?.withValues(
                          alpha: 0.7,
                        ),
                  ),
                ),
              ],
              if (model.tags.isNotEmpty) ...[
                const SizedBox(height: 6),
                Wrap(
                  spacing: 6,
                  runSpacing: 4,
                  children: model.tags
                      .map(
                        (tag) => Chip(
                          label: Text(tag),
                          visualDensity: VisualDensity.compact,
                        ),
                      )
                      .toList(),
                ),
              ],
              if (model.notes.isNotEmpty) ...[
                const SizedBox(height: 6),
                Text(
                  model.notes,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.textTheme.bodySmall?.color?.withValues(
                          alpha: 0.7,
                        ),
                  ),
                ),
              ],
              if (!model.available && model.reasonUnavailable.isNotEmpty) ...[
                const SizedBox(height: 6),
                Text(
                  l10n.modelUnavailableReason(model.reasonUnavailable),
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.colorScheme.error,
                  ),
                ),
              ],
              if (!model.available && model.requiresApiKey) ...[
                const SizedBox(height: 6),
                Text(
                  l10n.modelApiKeyRequired,
                  style: theme.textTheme.bodySmall?.copyWith(
                    color: theme.textTheme.bodySmall?.color?.withValues(
                          alpha: 0.7,
                        ),
                  ),
                ),
              ],
              if (!model.available && model.provider == 'ollama') ...[
                const SizedBox(height: 6),
                Row(
                  children: [
                    Expanded(
                      child: Text(
                        l10n.modelInstallCommand(command),
                        style: theme.textTheme.bodySmall?.copyWith(
                          color: theme.textTheme.bodySmall?.color
                              ?.withValues(alpha: 0.7),
                        ),
                      ),
                    ),
                    IconButton(
                      icon: const Icon(Icons.copy, size: 16),
                      tooltip: l10n.copyAction,
                      onPressed: () async {
                        await Clipboard.setData(
                          ClipboardData(text: command),
                        );
                        if (!context.mounted) {
                          return;
                        }
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(l10n.copiedToClipboard),
                            duration: const Duration(seconds: 2),
                            behavior: SnackBarBehavior.floating,
                          ),
                        );
                      },
                    ),
                  ],
                ),
              ],
            ],
          ),
        ),
      ),
    );
  }
}
