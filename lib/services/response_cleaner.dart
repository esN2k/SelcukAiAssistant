class ResponseCleaner {
  final StringBuffer _raw = StringBuffer();

  String push(String chunk) {
    _raw.write(chunk);
    return clean(_raw.toString());
  }

  String finalize() => clean(_raw.toString());

  static String clean(String text) {
    var cleaned = text;
    cleaned = cleaned.replaceAll(
      RegExp(r'<think>[\s\S]*?</think>', caseSensitive: false),
      '',
    );
    cleaned = cleaned.replaceAll(
      RegExp(r'<think>[\s\S]*$', caseSensitive: false),
      '',
    );
    cleaned = cleaned.replaceAll(
      RegExp(
        r'^\s*(reasoning|analysis|thoughts?|chain of thought|let me think).*?$',
        caseSensitive: false,
        multiLine: true,
      ),
      '',
    );
    cleaned = cleaned.replaceAll(
      RegExp(
        r'^\s*(düşünce|akıl yürütme|gerekçe|mantık).*?$',
        caseSensitive: false,
        multiLine: true,
      ),
      '',
    );
    cleaned = cleaned.replaceAll(
      RegExp(r'^\s*(final answer|final|answer)\s*:\s*', caseSensitive: false),
      '',
    );
    cleaned = cleaned.replaceAll(
      RegExp(r'^\s*okay[, ]+i need to respond.*$', caseSensitive: false),
      '',
    );
    return cleaned.trim();
  }
}
