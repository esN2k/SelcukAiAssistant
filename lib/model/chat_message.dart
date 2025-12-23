import 'package:hive/hive.dart';

class ChatMessage extends HiveObject {
  ChatMessage({
    required this.id,
    required this.content,
    required this.isUser,
    required this.createdAt,
    this.imageUrl,
    this.role,
    this.provider,
    this.modelId,
    this.error,
    this.errorCode,
    this.parentMessageId,
    List<String>? citations,
  }) : citations = citations ?? <String>[];

  factory ChatMessage.fromJson(Map<String, dynamic> json) {
    final roleValue = json['role'] as String?;
    final createdAtValue = json['createdAt'] ?? json['timestamp'];
    final createdAt = createdAtValue is String
        ? DateTime.parse(createdAtValue)
        : DateTime.now();
    return ChatMessage(
      id: json['id'] as String,
      content: json['content'] as String,
      isUser: roleValue == null
          ? (json['isUser'] as bool? ?? false)
          : roleValue == 'user',
      createdAt: createdAt,
      imageUrl: json['imageUrl'] as String?,
      role: roleValue,
      provider: json['provider'] as String?,
      modelId: json['modelId'] as String?,
      error: json['error'] as String?,
      errorCode: json['errorCode'] as String?,
      parentMessageId: json['parentMessageId'] as String?,
      citations: (json['citations'] as List<dynamic>?)
          ?.map((item) => item.toString())
          .toList(),
    );
  }

  String id;
  String content;
  bool isUser;
  DateTime createdAt;
  String? imageUrl;
  String? role;
  String? provider;
  String? modelId;
  String? error;
  String? errorCode;
  String? parentMessageId;
  List<String> citations;

  String get effectiveRole => role ?? (isUser ? 'user' : 'assistant');
  bool get hasError => error != null && error!.isNotEmpty;

  Map<String, dynamic> toJson() => {
        'id': id,
        'role': effectiveRole,
        'content': content,
        'createdAt': createdAt.toIso8601String(),
        'imageUrl': imageUrl,
        'provider': provider,
        'modelId': modelId,
        'error': error,
        'errorCode': errorCode,
        'parentMessageId': parentMessageId,
        'citations': citations,
      };
}

class ChatMessageAdapter extends TypeAdapter<ChatMessage> {
  @override
  final int typeId = 1;

  @override
  ChatMessage read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };

    final isUser = fields[2] as bool? ?? false;
    final role = fields[5] as String?;
    final createdAt = fields[3] is DateTime
        ? fields[3] as DateTime
        : DateTime.now();

    return ChatMessage(
      id: fields[0] as String,
      content: fields[1] as String,
      isUser: isUser,
      createdAt: createdAt,
      imageUrl: fields[4] as String?,
      role: role,
      provider: fields[6] as String?,
      modelId: fields[7] as String?,
      error: fields[8] as String?,
      errorCode: fields[9] as String?,
      parentMessageId: fields[10] as String?,
      citations: (fields[11] as List?)?.cast<String>(),
    );
  }

  @override
  void write(BinaryWriter writer, ChatMessage obj) {
    writer
      ..writeByte(12)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.content)
      ..writeByte(2)
      ..write(obj.isUser)
      ..writeByte(3)
      ..write(obj.createdAt)
      ..writeByte(4)
      ..write(obj.imageUrl)
      ..writeByte(5)
      ..write(obj.role)
      ..writeByte(6)
      ..write(obj.provider)
      ..writeByte(7)
      ..write(obj.modelId)
      ..writeByte(8)
      ..write(obj.error)
      ..writeByte(9)
      ..write(obj.errorCode)
      ..writeByte(10)
      ..write(obj.parentMessageId)
      ..writeByte(11)
      ..write(obj.citations);
  }
}
