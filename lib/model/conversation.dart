import 'package:hive/hive.dart';
import 'package:selcukaiassistant/model/chat_message.dart';

export 'package:selcukaiassistant/model/chat_message.dart';

class Conversation extends HiveObject {
  Conversation({
    required this.id,
    required this.title,
    required this.createdAt,
    required this.updatedAt,
    this.pinned = false,
    this.archived = false,
    this.selectedModelId,
    List<ChatMessage>? messages,
  }) : messages = messages ?? <ChatMessage>[];

  factory Conversation.fromJson(Map<String, dynamic> json) {
    return Conversation(
      id: json['id'] as String,
      title: json['title'] as String,
      createdAt: DateTime.parse(json['createdAt'] as String),
      updatedAt: DateTime.parse(json['updatedAt'] as String),
      pinned: json['pinned'] as bool? ?? false,
      archived: json['archived'] as bool? ?? false,
      selectedModelId: json['selectedModelId'] as String?,
      messages: (json['messages'] as List<dynamic>? ?? const [])
          .map((item) => ChatMessage.fromJson(item as Map<String, dynamic>))
          .toList(),
    );
  }

  String id;
  String title;
  DateTime createdAt;
  DateTime updatedAt;
  bool pinned;
  bool archived;
  String? selectedModelId;
  List<ChatMessage> messages;

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'createdAt': createdAt.toIso8601String(),
        'updatedAt': updatedAt.toIso8601String(),
        'pinned': pinned,
        'archived': archived,
        'selectedModelId': selectedModelId,
        'messages': messages.map((m) => m.toJson()).toList(),
      };
}

class ConversationAdapter extends TypeAdapter<Conversation> {
  @override
  final int typeId = 0;

  @override
  Conversation read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };

    return Conversation(
      id: fields[0] as String,
      title: fields[1] as String,
      createdAt: fields[2] as DateTime,
      updatedAt: fields[3] as DateTime,
      messages: (fields[4] as List?)?.cast<ChatMessage>(),
      pinned: fields[5] as bool? ?? false,
      archived: fields[6] as bool? ?? false,
      selectedModelId: fields[7] as String?,
    );
  }

  @override
  void write(BinaryWriter writer, Conversation obj) {
    writer
      ..writeByte(8)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.title)
      ..writeByte(2)
      ..write(obj.createdAt)
      ..writeByte(3)
      ..write(obj.updatedAt)
      ..writeByte(4)
      ..write(obj.messages)
      ..writeByte(5)
      ..write(obj.pinned)
      ..writeByte(6)
      ..write(obj.archived)
      ..writeByte(7)
      ..write(obj.selectedModelId);
  }
}
