class ResponseCleaner {
  final StringBuffer _raw = StringBuffer();

  String push(String chunk) {
    _raw.write(chunk);
    return clean(_raw.toString());
  }

  String finalize() => clean(_raw.toString());

  static String clean(String text) {
    // 1) Split by fenced code blocks so we never alter code.
    final parts = _splitByFences(text);

    for (var i = 0; i < parts.length; i++) {
      final segment = parts[i].$1;
      final isCode = parts[i].$2;
      if (isCode) continue;

      var cleaned = segment;

      // 2) Remove <think> blocks (complete + incomplete streaming tail).
      cleaned = cleaned.replaceAll(
        RegExp(r'<think>[\s\S]*?</think>', caseSensitive: false),
        '',
      );
      cleaned = cleaned.replaceAll(
        RegExp(r'<think>[\s\S]*$', caseSensitive: false),
        '',
      );

      // 3) Strip only LEADING meta header lines, not mid-response content.
      cleaned = _stripLeadingMetaLines(cleaned);

      parts[i] = (cleaned, isCode);
    }

    final rebuilt = parts.map((p) => p.$1).join();

    // Avoid aggressive trim that can cause streaming jitter; only trim leading whitespace.
    return rebuilt.replaceFirst(RegExp(r'^\s+'), '');
  }

  static String _stripLeadingMetaLines(String s) {
    final lines = s.replaceAll('\r\n', '\n').split('\n');

    int idx = 0;
    // Skip initial empty lines
    while (idx < lines.length && lines[idx].trim().isEmpty) idx++;

    final metaLine = RegExp(
      r'^\s*(?:'
      // English meta headers
      r'(?:reasoning|analysis|thoughts?|chain of thought|let me think)\s*:?\s*$|'
      // Turkish meta headers (NOTE: intentionally excludes "mantık" to avoid false positives)
      r'(?:düşünce|akıl yürütme|gerekçe)\s*:?\s*$|'
      // "Final" wrappers
      r'(?:final answer|final|answer)\s*:?\s*$|'
      // Common preamble
      r'okay[, ]+i need to respond.*$'
      r')',
      caseSensitive: false,
    );

    // Remove up to first ~6 meta lines
    int removed = 0;
    while (idx < lines.length && removed < 6) {
      final line = lines[idx].trim();
      if (line.isEmpty) {
        idx++;
        continue;
      }
      if (!metaLine.hasMatch(line)) break;
      lines[idx] = '';
      idx++;
      removed++;
    }

    return lines.join('\n');
  }

  static List<(String, bool)> _splitByFences(String s) {
    final out = <(String, bool)>[];
    const fence = '```';
    int i = 0;
    bool inCode = false;

    while (i < s.length) {
      final j = s.indexOf(fence, i);
      if (j == -1) {
        out.add((s.substring(i), inCode));
        break;
      }
      out.add((s.substring(i, j), inCode));

      // Toggle code state and keep the fence token itself.
      inCode = !inCode;
      out.add((fence, inCode));

      i = j + fence.length;
    }
    return out;
  }
}
