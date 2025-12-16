import 'dart:developer';

import 'package:appwrite/appwrite.dart';
import 'package:appwrite/models.dart' as models;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppwriteService {
  AppwriteService() {
    final endpoint = dotenv.env['APPWRITE_ENDPOINT'];
    final projectId = dotenv.env['APPWRITE_PROJECT_ID'];

    if (endpoint == null || projectId == null) {
      log('Appwrite environment variables not found!');
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
      throw Exception('Appwrite Service not initialized');
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
      throw Exception('Appwrite Service not initialized');
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
      throw Exception('Appwrite Service not initialized');
    }
    try {
      await account!.deleteSession(sessionId: 'current');
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Oturum kapatılamadı');
    }
  }

  Future<models.User?> getCurrentUser() async {
    if (account == null) {
      log('Appwrite client not initialized, returning null user');
      return null;
    }
    try {
      return await account!.get();
    } on AppwriteException {
      return null; // Oturum yoksa null dön
    }
  }
}
