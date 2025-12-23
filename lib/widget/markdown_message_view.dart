import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_highlight/flutter_highlight.dart';
import 'package:flutter_highlight/themes/atom-one-dark.dart';
import 'package:flutter_highlight/themes/atom-one-light.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import 'package:markdown/markdown.dart' as md;
import 'package:selcukaiassistant/l10n/l10n.dart';

class MarkdownMessageView extends StatelessWidget {
  const MarkdownMessageView({
    required this.data,
    super.key,
  });

  final String data;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    return MarkdownBody(
      data: data,
      selectable: true,
      styleSheet: MarkdownStyleSheet(
        p: TextStyle(
          fontSize: 15,
          height: 1.5,
          color: Theme.of(context).textTheme.bodyMedium?.color,
        ),
        code: TextStyle(
          fontFamily: 'monospace',
          fontSize: 13,
          color: Theme.of(context).textTheme.bodyMedium?.color,
          backgroundColor: isDark ? Colors.grey[800] : Colors.grey[200],
        ),
      ),
      builders: {
        'pre': CodeBlockBuilder(),
      },
    );
  }
}

class CodeBlockBuilder extends MarkdownElementBuilder {
  @override
  Widget? visitElementAfter(md.Element element, TextStyle? preferredStyle) {
    md.Element? codeElement;
    for (final child in element.children ?? <md.Node>[]) {
      if (child is md.Element && child.tag == 'code') {
        codeElement = child;
        break;
      }
    }

    final rawCode = (codeElement ?? element).textContent;
    final className = codeElement?.attributes['class'];
    final languageMatch =
        className == null ? null : RegExp(r'language-([\\w-]+)').firstMatch(className);
    final language = languageMatch?.group(1);

    return CodeBlockWidget(
      code: rawCode,
      language: language,
    );
  }
}

class CodeBlockWidget extends StatelessWidget {
  const CodeBlockWidget({
    required this.code,
    this.language,
    super.key,
  });

  final String code;
  final String? language;

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final background =
        isDark ? const Color(0xFF1E1E1E) : const Color(0xFFF6F6F6);
    final borderColor =
        isDark ? const Color(0xFF2B2B2B) : const Color(0xFFE0E0E0);
    final title = (language == null || language!.isEmpty) ? 'code' : language!;
    final codeText = code.trimRight();

    return Container(
      margin: const EdgeInsets.symmetric(vertical: 8),
      decoration: BoxDecoration(
        color: background,
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: borderColor),
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Container(
            padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
            decoration: BoxDecoration(
              color: isDark ? const Color(0xFF2B2B2B) : const Color(0xFFEAEAEA),
              borderRadius: const BorderRadius.vertical(
                top: Radius.circular(8),
              ),
            ),
            child: Row(
              children: [
                Text(
                  title,
                  style: TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: isDark ? Colors.white70 : Colors.black54,
                  ),
                ),
                const Spacer(),
                IconButton(
                  icon: const Icon(Icons.copy, size: 16),
                  tooltip: context.l10n.copyAction,
                  padding: EdgeInsets.zero,
                  constraints: const BoxConstraints(
                    minWidth: 24,
                    minHeight: 24,
                  ),
                  onPressed: () async {
                    await Clipboard.setData(ClipboardData(text: codeText));
                    if (!context.mounted) {
                      return;
                    }
                    ScaffoldMessenger.of(context).showSnackBar(
                      SnackBar(
                        content: Text(context.l10n.copiedToClipboard),
                        duration: const Duration(seconds: 2),
                        behavior: SnackBarBehavior.floating,
                      ),
                    );
                  },
                ),
              ],
            ),
          ),
          SingleChildScrollView(
            scrollDirection: Axis.horizontal,
            padding: const EdgeInsets.all(12),
            child: HighlightView(
              codeText,
              language: language ?? 'plaintext',
              theme: isDark ? atomOneDarkTheme : atomOneLightTheme,
              textStyle: const TextStyle(
                fontFamily: 'monospace',
                fontSize: 13,
                height: 1.4,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
