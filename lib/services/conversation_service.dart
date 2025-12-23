import 'package:hive/hive.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';
import 'package:uuid/uuid.dart';

class ConversationService {
  static Box<Conversation>? _box;
  static const _uuid = Uuid();

  static Future<void> init() async {
    if (_box != null) {
      return;
    }
    await StorageService.initialize();
    _box = StorageService.conversationsBox;
  }

  static Box<Conversation> get box {
    if (_box == null) {
      throw Exception('ConversationService not initialized');
    }
    return _box!;
  }

  // Create a new conversation
  static Future<Conversation> createConversation({String? title}) async {
    final conversation = Conversation(
      id: _uuid.v4(),
      title: title ?? 'New Chat',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
      messages: [],
    );

    await box.put(conversation.id, conversation);
    return conversation;
  }

  // Get all conversations sorted by updated time
  static List<Conversation> getAllConversations() {
    return box.values.toList()
      ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
  }

  // Get a specific conversation by ID
  static Conversation? getConversation(String id) {
    return box.get(id);
  }

  // Add a message to a conversation
  static Future<void> addMessage(
    String conversationId,
    ChatMessage message,
  ) async {
    final conversation = box.get(conversationId);
    if (conversation != null) {
      conversation
        ..messages.add(message)
        ..updatedAt = DateTime.now();

      // Auto-generate title from first user message if still default
      if (conversation.title == 'New Chat' &&
          message.isUser &&
          conversation.messages.where((m) => m.isUser).length == 1) {
        conversation
          ..title = _generateTitle(message.content)
          ..updatedAt = DateTime.now();
      }

      await conversation.save();
    }
  }

  // Update a message in a conversation
  static Future<void> updateMessage(
    String conversationId,
    String messageId,
    String newContent,
  ) async {
    final conversation = box.get(conversationId);
    if (conversation != null) {
      final messageIndex =
          conversation.messages.indexWhere((m) => m.id == messageId);
      if (messageIndex != -1) {
        conversation.messages[messageIndex].content = newContent;
        conversation.updatedAt = DateTime.now();
        await conversation.save();
      }
    }
  }

  // Delete a conversation
  static Future<void> deleteConversation(String id) async {
    await box.delete(id);
  }

  // Rename a conversation
  static Future<void> renameConversation(String id, String newTitle) async {
    final conversation = box.get(id);
    if (conversation != null) {
      conversation
        ..title = newTitle
        ..updatedAt = DateTime.now();
      await conversation.save();
    }
  }

  // Search conversations
  static List<Conversation> searchConversations(String query) {
    final lowerQuery = query.toLowerCase();
    return box.values.where((conversation) {
      // Search in title
      if (conversation.title.toLowerCase().contains(lowerQuery)) {
        return true;
      }
      // Search in messages
      return conversation.messages.any(
        (msg) => msg.content.toLowerCase().contains(lowerQuery),
      );
    }).toList();
  }

  // Clear all conversations
  static Future<void> clearAll() async {
    await box.clear();
  }

  // Export conversation as JSON
  static Map<String, dynamic> exportConversation(String id) {
    final conversation = box.get(id);
    if (conversation != null) {
      return conversation.toJson();
    }
    return {};
  }

  // Generate a smart title from the first message
  static String _generateTitle(String content) {
    // Take first 50 characters or first sentence
    var title = content.trim();

    if (title.length > 50) {
      title = title.substring(0, 50);
      // Try to end at a word boundary
      final lastSpace = title.lastIndexOf(' ');
      if (lastSpace > 30) {
        title = title.substring(0, lastSpace);
      }
      title = '$title...';
    }

    return title;
  }

  // Get statistics
  static Map<String, dynamic> getStatistics() {
    final conversations = box.values.toList();
    final totalMessages = conversations.fold<int>(
      0,
      (sum, conv) => sum + conv.messages.length,
    );

    return {
      'totalConversations': conversations.length,
      'totalMessages': totalMessages,
      'oldestConversation': conversations.isNotEmpty
          ? conversations
              .reduce((a, b) => a.createdAt.isBefore(b.createdAt) ? a : b)
              .createdAt
          : null,
      'newestConversation': conversations.isNotEmpty
          ? conversations
              .reduce((a, b) => a.createdAt.isAfter(b.createdAt) ? a : b)
              .createdAt
          : null,
    };
  }
}
