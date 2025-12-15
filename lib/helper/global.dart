import 'package:appwrite/appwrite.dart';
import 'package:flutter/material.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

const appName = 'Yapay zeka akıllı asistanı';

late Size mq;

String apiKey = dotenv.env['API_KEY'] ?? '';

// Backend API URL - configurable via environment variable
String backendUrl = dotenv.env['BACKEND_URL'] ?? 'http://localhost:8000';

// Appwrite global client
final Client appwriteClient = Client()
    .setProject('69407f8200300e7093d8')
    .setEndpoint('https://fra.cloud.appwrite.io/v1');
