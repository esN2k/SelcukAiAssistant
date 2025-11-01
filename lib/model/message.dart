class Message {
  Message({required this.msg, required this.msgType});
  String msg;
  final MessageType msgType;
}

enum MessageType { user, bot }
