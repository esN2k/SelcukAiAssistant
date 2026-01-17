/// DOSYA ADI: response_cleaner.dart
/// AMAÇ: Model yanıtlarındaki düşünce ve meta bloklarını temizlemek.
/// NE YAPAR:
///   - `<think>` bloklarını çıkarır.
///   - Kod bloklarını koruyarak metni sadeleştirir.
/// BAĞIMLILIKLAR:
///   - yok
/// SON DEĞİŞİKLİK: 17.01.2026
class ResponseCleaner {
  final StringBuffer _raw = StringBuffer();

  String push(String chunk) {
    _raw.write(chunk);
    return clean(_raw.toString());
  }

  String finalize() => clean(_raw.toString());

  static String clean(String text) {
    // 1) Kod bloklarını ayır, böylece kod içeriği bozulmasın.
    final parts = _splitByFences(text);

    for (var i = 0; i < parts.length; i++) {
      final segment = parts[i].$1;
      final isCode = parts[i].$2;
      if (isCode) continue;

      var cleaned = segment;

      // 2) <think> bloklarını temizle (tamamlanmış + yarım kalan akış).
      cleaned = cleaned.replaceAll(
        RegExp(r'<think>[\s\S]*?</think>', caseSensitive: false),
        '',
      );
      cleaned = cleaned.replaceAll(
        RegExp(r'<think>[\s\S]*$', caseSensitive: false),
        '',
      );

      // 3) Sadece baştaki meta başlık satırlarını kaldır.
      cleaned = _stripLeadingMetaLines(cleaned);

      parts[i] = (cleaned, isCode);
    }

    final rebuilt = parts.map((p) => p.$1).join();

    // Akışta titreme olmaması için yalnızca baştaki boşluğu temizle.
    return rebuilt.replaceFirst(RegExp(r'^\s+'), '');
  }

  static String _stripLeadingMetaLines(String s) {
    final lines = s.replaceAll('\r\n', '\n').split('\n');

    var idx = 0;
    // Başlangıçtaki boş satırları geç.
    while (idx < lines.length && lines[idx].trim().isEmpty) {
      idx++;
    }

    final metaLine = RegExp(
      r'^\s*(?:'
      // İngilizce meta başlıklar
      r'(?:reasoning|analysis|thoughts?|chain of thought|let me think)\s*:?\s*$|'
      // Türkçe meta başlıklar.
      // Not:
      // - Sık görülen meta başlıklar eşleşir.
      // - Yanlış pozitifleri azaltmak için "mantık" hariç tutulur.
      r'(?:düşünce|akıl yürütme|gerekçe)\s*:?\s*$|'
      // "Final" sarmalayıcıları
      r'(?:final answer|final|answer)\s*:?\s*$|'
      // Yaygın ön bilgi satırları
      r'(?:final answer|final|answer)\s*:?\s*$|'
      // Yaygın ön bilgi satırları
      r'okay[, ]+i need to respond.*$'
      ')',
      caseSensitive: false,
    );

    // En fazla ilk 6 meta satırı kaldır.
    var removed = 0;
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
    var i = 0;
    var inCode = false;

    while (i < s.length) {
      final j = s.indexOf(fence, i);
      if (j == -1) {
        out.add((s.substring(i), inCode));
        break;
      }
      out.add((s.substring(i, j), inCode));

      // Kod durumunu değiştir ve fence işaretini koru.
      inCode = !inCode;
      out.add((fence, inCode));

      i = j + fence.length;
    }
    return out;
  }
}
