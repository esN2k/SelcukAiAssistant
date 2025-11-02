import 'package:flutter/material.dart';

import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/main.dart';

class CustomBtn extends StatelessWidget {
  const CustomBtn({required this.onTap, required this.text, super.key});
  final String text;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    return Align(
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          shape: const StadiumBorder(),
          elevation: 0,
          backgroundColor: Colors.amber, // Burayı değiştirdik
          textStyle: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500),
          minimumSize: Size(mq.width * .4, 50),
        ),
        onPressed: onTap,
        child: Text(text),
      ),
    );
  }
}
