/// ══════════════════════════════════════════════════════════════════════════════
/// DOSYA ADI: message.dart
/// AMAÇ: Sohbet mesajı veri modeli
/// KULLANIM: ChatController ve MessageCard tarafından kullanılır
/// YAZAN: esN2k - Selçuk Üniversitesi
/// ══════════════════════════════════════════════════════════════════════════════
///
/// DETAYLI AÇIKLAMA:
/// ────────────────
/// Bu dosya, sohbet mesajlarını temsil eden basit veri modelini tanımlar.
///
/// ALANLAR:
/// • msg: Mesaj içeriği (String)
/// • msgType: Mesaj türü (user veya bot)
///
/// KULLANIM:
/// ```dart
/// final userMessage = Message(msg: "Merhaba", msgType: MessageType.user);
/// final botMessage = Message(msg: "Size nasıl yardımcı...", msgType: MessageType.bot);
/// ```

class Message {
  Message({required this.msg, required this.msgType});
  String msg;
  final MessageType msgType;
}

enum MessageType { user, bot }
