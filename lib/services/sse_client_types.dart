class ChatStreamEvent {
  ChatStreamEvent({
    required this.type,
    required this.requestId,
    this.token,
    this.message,
    this.usage,
  });

  factory ChatStreamEvent.fromJson(Map<String, dynamic> json) {
    return ChatStreamEvent(
      type: json['type'] as String? ?? '',
      requestId: json['request_id'] as String? ?? '',
      token: json['token'] as String?,
      message: json['message'] as String?,
      usage: json['usage'] as Map<String, dynamic>?,
    );
  }

  final String type;
  final String requestId;
  final String? token;
  final String? message;
  final Map<String, dynamic>? usage;
}

class ChatStreamSession {
  ChatStreamSession({
    required this.stream,
    required this.close,
  });

  final Stream<ChatStreamEvent> stream;
  final void Function() close;
}
