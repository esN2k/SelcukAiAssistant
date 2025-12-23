class ChatApiResponse {
  ChatApiResponse({
    required this.answer,
    List<String>? citations,
    Map<String, dynamic>? usage,
  })  : citations = citations ?? <String>[],
        usage = usage ?? <String, dynamic>{};

  final String answer;
  final List<String> citations;
  final Map<String, dynamic> usage;
}
