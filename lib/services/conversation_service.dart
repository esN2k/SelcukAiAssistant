/// DOSYA ADI: conversation_service.dart
/// AMAÇ: Sohbet oturumlarını yerel depoda yönetmek.
/// NE YAPAR:
///   - Yeni sohbet oluşturur.
///   - Mesaj ekleme/güncelleme işlemlerini yapar.
///   - Arşivleme ve istatistik üretir.
/// BAĞIMLILIKLAR:
///   - hive: yerel depolama
///   - storage_service.dart: kutu yönetimi
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'package:hive/hive.dart';
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';
import 'package:uuid/uuid.dart';

class ConversationService {
  static Box<Conversation>? _box;
  static const _uuid = Uuid();
  static const Set<String> _defaultTitles = {'yeni sohbet', 'new chat'};

  /// Giriş: yok.
  /// Çıkış: yok.
  /// İşleyiş: Depolama kutularını başlatır.
  static Future<void> init() async {
    if (_box != null) {
      return;
    }
    await StorageService.initialize();
    _box = StorageService.conversationsBox;
  }

  /// Giriş: yok.
  /// Çıkış: Konuşma kutusu.
  /// İşleyiş: Başlatılmamışsa hata üretir.
  static Box<Conversation> get box {
    if (_box == null) {
      throw AppException(ErrorMessages.depolamaBaslatilmadi);
    }
    return _box!;
  }

  /// Giriş: Başlık metni.
  /// Çıkış: Varsayılan başlık mı?
  /// İşleyiş: Başlığı normalize ederek kontrol eder.
  static bool isDefaultTitle(String title) {
    return _defaultTitles.contains(title.trim().toLowerCase());
  }

  // Yeni bir konuşma oluşturur.
  static Future<Conversation> createConversation({String? title}) async {
    final defaultTitle = L10n.current()?.newChat ?? 'Yeni Sohbet';
    final conversation = Conversation(
      id: _uuid.v4(),
      title: title ?? defaultTitle,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
      messages: [],
    );

    await box.put(conversation.id, conversation);
    return conversation;
  }

  // Tüm konuşmaları güncellenme tarihine göre sıralar.
  static List<Conversation> getAllConversations({
    bool includeArchived = true,
  }) {
    final conversations = box.values.where((conversation) {
      if (includeArchived) {
        return true;
      }
      return !conversation.archived;
    }).toList()
      ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return conversations;
  }

  static List<Conversation> getActiveConversations() {
    return getAllConversations(includeArchived: false);
  }

  static List<Conversation> getArchivedConversations() {
    return box.values.where((conversation) => conversation.archived).toList()
      ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
  }

  // ID ile konuşma getirir.
  static Conversation? getConversation(String id) {
    return box.get(id);
  }

  // Konuşmaya mesaj ekler.
  static Future<void> addMessage(
    String conversationId,
    ChatMessage message,
  ) async {
    final conversation = box.get(conversationId);
    if (conversation != null) {
      conversation
        ..messages.add(message)
        ..updatedAt = DateTime.now();

      // Varsayılan başlıktaysa ilk kullanıcı mesajından otomatik başlık üretir.
      if (isDefaultTitle(conversation.title) &&
          message.isUser &&
          conversation.messages.where((m) => m.isUser).length == 1) {
        conversation
          ..title = generateTitle(message.content)
          ..updatedAt = DateTime.now();
      }

      await conversation.save();
    }
  }

  // Konuşmadaki bir mesajı günceller.
  static Future<void> updateMessage(
    String conversationId,
    String messageId, {
    String? newContent,
    String? error,
    String? errorCode,
    List<String>? citations,
  }) async {
    final conversation = box.get(conversationId);
    if (conversation != null) {
      final messageIndex =
          conversation.messages.indexWhere((m) => m.id == messageId);
      if (messageIndex != -1) {
        final message = conversation.messages[messageIndex];
        if (newContent != null) {
          message.content = newContent;
        }
        if (error != null) {
          message.error = error.isEmpty ? null : error;
        }
        if (errorCode != null) {
          message.errorCode = errorCode.isEmpty ? null : errorCode;
        }
        if (citations != null) {
          message.citations = citations;
        }
        conversation.updatedAt = DateTime.now();
        await conversation.save();
      }
    }
  }

  static Future<void> setMessages(
    String conversationId,
    List<ChatMessage> messages,
  ) async {
    final conversation = box.get(conversationId);
    if (conversation != null) {
      conversation
        ..messages = messages
        ..updatedAt = DateTime.now();
      await conversation.save();
    }
  }

  // Konuşmayı siler.
  static Future<void> deleteConversation(String id) async {
    await box.delete(id);
  }

  // Konuşmayı yeniden adlandırır.
  static Future<void> renameConversation(String id, String newTitle) async {
    final conversation = box.get(id);
    if (conversation != null) {
      conversation
        ..title = newTitle
        ..updatedAt = DateTime.now();
      await conversation.save();
    }
  }

  // Konuşmaları arar.
  static List<Conversation> searchConversations(
    String query, {
    bool includeArchived = true,
  }) {
    final lowerQuery = query.toLowerCase();
    final results = box.values.where((conversation) {
      if (!includeArchived && conversation.archived) {
        return false;
      }
      // Başlık içinde arama.
      if (conversation.title.toLowerCase().contains(lowerQuery)) {
        return true;
      }
      // Mesaj içeriğinde arama.
      return conversation.messages.any(
        (msg) => msg.content.toLowerCase().contains(lowerQuery),
      );
    }).toList()
      ..sort((a, b) => b.updatedAt.compareTo(a.updatedAt));
    return results;
  }

  static Future<void> setPinned(String id, {required bool pinned}) async {
    final conversation = box.get(id);
    if (conversation != null) {
      conversation.pinned = pinned;
      if (pinned) {
        conversation.archived = false;
      }
      await conversation.save();
    }
  }

  static Future<void> setArchived(String id, {required bool archived}) async {
    final conversation = box.get(id);
    if (conversation != null) {
      conversation.archived = archived;
      if (archived) {
        conversation.pinned = false;
      }
      await conversation.save();
    }
  }

  // Tüm konuşmaları temizler.
  static Future<void> clearAll() async {
    await box.clear();
  }

  // Konuşmayı JSON olarak dışa aktarır.
  static Map<String, dynamic> exportConversation(String id) {
    final conversation = box.get(id);
    if (conversation != null) {
      return conversation.toJson();
    }
    return {};
  }

  // İlk mesajdan akıllı başlık üretir.
  static String generateTitle(String content) {
    // İlk 50 karakteri veya ilk cümleyi alır.
    var title = content.trim();

    if (title.length > 50) {
      title = title.substring(0, 50);
      // Kelime sınırında bitirmeyi dener.
      final lastSpace = title.lastIndexOf(' ');
      if (lastSpace > 30) {
        title = title.substring(0, lastSpace);
      }
      title = '$title...';
    }

    return title;
  }

  // Konuşma istatistiklerini döndürür.
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
