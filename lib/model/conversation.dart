import 'package:hive/hive.dart';

part 'conversation.g.dart';

@HiveType(typeId: 0)
class Conversation extends HiveObject {
  Conversation({
    required this.id,
    required this.title,
    required this.createdAt,
    required this.updatedAt,
    this.messages = const [],
  });

  Conversation.fromJson(Map<String, dynamic> json)
      : id = json['id'] as String,
        title = json['title'] as String,
        createdAt = DateTime.parse(json['createdAt'] as String),
        updatedAt = DateTime.parse(json['updatedAt'] as String),
        messages = (json['messages'] as List<dynamic>)
            .map((m) => ChatMessage.fromJson(m as Map<String, dynamic>))
            .toList();

  @HiveField(0)
  String id;

  @HiveField(1)
  String title;

  @HiveField(2)
  DateTime createdAt;

  @HiveField(3)
  DateTime updatedAt;

  @HiveField(4)
  List<ChatMessage> messages;

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'createdAt': createdAt.toIso8601String(),
        'updatedAt': updatedAt.toIso8601String(),
        'messages': messages.map((m) => m.toJson()).toList(),
      };
}

@HiveType(typeId: 1)
class ChatMessage extends HiveObject {
  ChatMessage({
    required this.id,
    required this.content,
    required this.isUser,
    required this.timestamp,
    this.imageUrl,
  });

  ChatMessage.fromJson(Map<String, dynamic> json)
      : id = json['id'] as String,
        content = json['content'] as String,
        isUser = json['isUser'] as bool,
        timestamp = DateTime.parse(json['timestamp'] as String),
        imageUrl = json['imageUrl'] as String?;

  @HiveField(0)
  String id;

  @HiveField(1)
  String content;

  @HiveField(2)
  bool isUser;

  @HiveField(3)
  DateTime timestamp;

  @HiveField(4)
  String? imageUrl;

  Map<String, dynamic> toJson() => {
        'id': id,
        'content': content,
        'isUser': isUser,
        'timestamp': timestamp.toIso8601String(),
        'imageUrl': imageUrl,
      };
}
