// Using deprecated withOpacity API until migrated to withValues
// ignore_for_file: deprecated_member_use

import 'package:animated_text_kit/animated_text_kit.dart';
import 'package:flutter/material.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/model/message.dart';

class MessageCard extends StatelessWidget {
  const MessageCard({required this.message, super.key});
  final Message message;

  @override
  Widget build(BuildContext context) {
    const r = Radius.circular(15);

    return message.msgType == MessageType.bot
        ? Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              const SizedBox(width: 6),
              CircleAvatar(
                radius: 18,
                backgroundColor: Colors.amber.withOpacity(0.1),
                child: const Icon(
                  Icons.smart_toy,
                  color: Colors.amber,
                  size: 20,
                ),
              ),
              Expanded(
                child: Container(
                  margin: EdgeInsets.only(
                    bottom: mq.height * .02,
                    left: mq.width * .02,
                    right: mq.width * .1,
                  ),
                  padding: EdgeInsets.symmetric(
                    vertical: mq.height * .015,
                    horizontal: mq.width * .03,
                  ),
                  decoration: BoxDecoration(
                    color: Theme.of(context).brightness == Brightness.dark
                        ? Colors.grey[800]
                        : Colors.grey[100],
                    borderRadius: const BorderRadius.only(
                      topLeft: r,
                      topRight: r,
                      bottomRight: r,
                    ),
                  ),
                  child: message.msg.isEmpty
                      ? AnimatedTextKit(
                          animatedTexts: [
                            TypewriterAnimatedText(
                              'Bir şey daha var...',
                              speed: const Duration(milliseconds: 100),
                            ),
                          ],
                          repeatForever: true,
                        )
                      : MarkdownBody(
                          data: message.msg,
                          selectable: true,
                          styleSheet: MarkdownStyleSheet(
                            p: TextStyle(
                              fontSize: 16,
                              color:
                                  Theme.of(context).textTheme.bodyLarge?.color,
                              height: 1.4,
                            ),
                            code: TextStyle(
                              backgroundColor: Theme.of(context).brightness ==
                                      Brightness.dark
                                  ? Colors.grey[700]
                                  : Colors.grey[200],
                              fontFamily: 'monospace',
                              fontSize: 14,
                            ),
                            codeblockDecoration: BoxDecoration(
                              color: Theme.of(context).brightness ==
                                      Brightness.dark
                                  ? Colors.grey[700]
                                  : Colors.grey[200],
                              borderRadius: BorderRadius.circular(8),
                            ),
                            blockquoteDecoration: BoxDecoration(
                              color: Theme.of(context).brightness ==
                                      Brightness.dark
                                  ? Colors.amber.withOpacity(0.1)
                                  : Colors.amber.withOpacity(0.05),
                              borderRadius: BorderRadius.circular(4),
                              border: const Border(
                                left: BorderSide(
                                  color: Colors.amber,
                                  width: 4,
                                ),
                              ),
                            ),
                          ),
                        ),
                ),
              ),
            ],
          )
        : Row(
            mainAxisAlignment: MainAxisAlignment.end,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Expanded(
                child: Container(
                  margin: EdgeInsets.only(
                    bottom: mq.height * .02,
                    right: mq.width * .02,
                    left: mq.width * .1,
                  ),
                  padding: EdgeInsets.symmetric(
                    vertical: mq.height * .015,
                    horizontal: mq.width * .03,
                  ),
                  decoration: const BoxDecoration(
                    color: Colors.amber,
                    borderRadius: BorderRadius.only(
                      topLeft: r,
                      topRight: r,
                      bottomLeft: r,
                    ),
                  ),
                  child: Text(
                    message.msg,
                    style: const TextStyle(
                      color: Colors.white,
                      fontSize: 16,
                      height: 1.4,
                    ),
                  ),
                ),
              ),
              const CircleAvatar(
                radius: 18,
                backgroundColor: Colors.amber,
                child: Icon(
                  Icons.person,
                  color: Colors.white,
                  size: 20,
                ),
              ),
              const SizedBox(width: 6),
            ],
          );
  }
}
