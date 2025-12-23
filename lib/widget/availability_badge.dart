import 'package:flutter/material.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';

class AvailabilityBadge extends StatelessWidget {
  const AvailabilityBadge({
    required this.model,
    super.key,
  });

  final ModelInfo model;

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final scheme = Theme.of(context).colorScheme;
    final label = _label(l10n);
    final background = _background(scheme);
    final foreground = _foreground(scheme);

    return Chip(
      label: Text(label),
      labelStyle: TextStyle(color: foreground, fontSize: 12),
      backgroundColor: background,
      visualDensity: VisualDensity.compact,
    );
  }

  String _label(AppLocalizations l10n) {
    if (model.available) {
      return l10n.modelAvailable;
    }
    if (model.requiresApiKey) {
      return l10n.modelApiKeyRequired;
    }
    if (model.provider == 'ollama') {
      return l10n.modelNotInstalled;
    }
    return l10n.modelUnavailable;
  }

  Color _background(ColorScheme scheme) {
    if (model.available) {
      return scheme.secondaryContainer;
    }
    if (model.requiresApiKey) {
      return scheme.tertiaryContainer;
    }
    return scheme.surfaceContainerHighest;
  }

  Color _foreground(ColorScheme scheme) {
    if (model.available) {
      return scheme.onSecondaryContainer;
    }
    if (model.requiresApiKey) {
      return scheme.onTertiaryContainer;
    }
    return scheme.onSurfaceVariant;
  }
}
