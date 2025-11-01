import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

const appName = 'AI 智能助手';

late Size mq;

String apiKey = dotenv.env['API_KEY'] ?? '';
