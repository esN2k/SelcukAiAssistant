import 'dart:developer';

import 'package:appwrite/appwrite.dart';
import 'package:appwrite/models.dart' as models;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppwriteService {
  AppwriteService() {
    final endpoint = dotenv.env['APPWRITE_ENDPOINT']?.trim();
    final projectId = dotenv.env['APPWRITE_PROJECT_ID']?.trim();

    if (endpoint == null ||
        endpoint.isEmpty ||
        projectId == null ||
        projectId.isEmpty) {
      log('Appwrite ortam değişkenleri bulunamadı!');
      // Don't initialize client if keys are missing
      return;
    }

    client = Client()
      ..setEndpoint(endpoint)
      ..setProject(projectId);

    account = Account(client!);
  }

  // Make client and account nullable, as they might not be initialized
  Client? client;
  Account? account;

  Future<models.User?> register({
    required String email,
    required String password,
    String? name,
  }) async {
    if (account == null) {
      throw Exception('Appwrite servisi başlatılmadı');
    }
    try {
      return await account!.create(
        userId: ID.unique(),
        email: email,
        password: password,
        name: name,
      );
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Kayıt oluşturulamadı');
    }
  }

  Future<models.Session?> createSession(String email, String password) async {
    if (account == null) {
      throw Exception('Appwrite servisi başlatılmadı');
    }
    try {
      return await account!.createEmailPasswordSession(
        email: email,
        password: password,
      );
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Oturum açılamadı');
    }
  }

  Future<void> deleteCurrentSession() async {
    if (account == null) {
      throw Exception('Appwrite servisi başlatılmadı');
    }
    try {
      await account!.deleteSession(sessionId: 'current');
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Oturum kapatılamadı');
    }
  }

  Future<models.User?> getCurrentUser() async {
    if (account == null) {
      log('Appwrite istemcisi başlatılmadı, kullanıcı boş döndürülüyor');
      return null;
    }
    try {
      return await account!.get();
    } on AppwriteException {
      return null; // Oturum yoksa null dön
    }
  }
}
