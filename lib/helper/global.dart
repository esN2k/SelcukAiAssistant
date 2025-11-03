import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

const appName = 'Yapay zeka akıllı asistanı';

late Size mq;

String apiKey = dotenv.env['API_KEY'] ?? '';
