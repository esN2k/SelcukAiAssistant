/// DOSYA ADI: appwrite_service.dart
/// AMAÇ: Appwrite üzerinden kullanıcı işlemlerini yönetmek.
/// NE YAPAR:
///   - Kayıt, oturum açma ve çıkış işlemlerini yürütür.
///   - Mevcut kullanıcı bilgisini döndürür.
/// BAĞIMLILIKLAR:
///   - appwrite
///   - flutter_dotenv
/// SON DEĞİŞİKLİK: 17.01.2026
library;
import 'dart:developer';

import 'package:appwrite/appwrite.dart';
import 'package:appwrite/models.dart' as models;
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:selcukaiassistant/core/errors/app_exception.dart';
import 'package:selcukaiassistant/core/errors/error_messages.dart';

class AppwriteService {
  AppwriteService() {
    final endpoint = dotenv.env['APPWRITE_ENDPOINT']?.trim();
    final projectId = dotenv.env['APPWRITE_PROJECT_ID']?.trim();

    if (endpoint == null ||
        endpoint.isEmpty ||
        projectId == null ||
        projectId.isEmpty) {
      log('Appwrite ortam değişkenleri bulunamadı!');
      // Anahtarlar yoksa istemciyi başlatma.
      return;
    }

    client = Client()
      ..setEndpoint(endpoint)
      ..setProject(projectId);

    account = Account(client!);
  }

  // İstemci ve account opsiyoneldir; başlatılmamış olabilir.
  Client? client;
  Account? account;

  /// Giriş: Kullanıcı bilgileri.
  /// Çıkış: Oluşturulan kullanıcı nesnesi.
  /// İşleyiş: Appwrite üzerinden kullanıcı kaydı oluşturur.
  Future<models.User?> register({
    required String email,
    required String password,
    String? name,
  }) async {
    if (account == null) {
      throw AppException(ErrorMessages.appwriteBaslatilmadi);
    }
    try {
      return await account!.create(
        userId: ID.unique(),
        email: email,
        password: password,
        name: name,
      );
    } on AppwriteException catch (error) {
      final message = error.message?.trim();
      throw AppException(
        (message == null || message.isEmpty)
            ? ErrorMessages.appwriteKayitBasarisiz
            : message,
      );
    }
  }

  /// Giriş: E-posta ve şifre.
  /// Çıkış: Oturum nesnesi.
  /// İşleyiş: Appwrite üzerinden oturum açar.
  Future<models.Session?> createSession(String email, String password) async {
    if (account == null) {
      throw AppException(ErrorMessages.appwriteBaslatilmadi);
    }
    try {
      return await account!.createEmailPasswordSession(
        email: email,
        password: password,
      );
    } on AppwriteException catch (error) {
      final message = error.message?.trim();
      throw AppException(
        (message == null || message.isEmpty)
            ? ErrorMessages.appwriteOturumAcilamadi
            : message,
      );
    }
  }

  /// Giriş: yok.
  /// Çıkış: yok.
  /// İşleyiş: Mevcut oturumu kapatır.
  Future<void> deleteCurrentSession() async {
    if (account == null) {
      throw AppException(ErrorMessages.appwriteBaslatilmadi);
    }
    try {
      await account!.deleteSession(sessionId: 'current');
    } on AppwriteException catch (error) {
      final message = error.message?.trim();
      throw AppException(
        (message == null || message.isEmpty)
            ? ErrorMessages.appwriteOturumKapatilamadi
            : message,
      );
    }
  }

  /// Giriş: yok.
  /// Çıkış: Kullanıcı nesnesi veya null.
  /// İşleyiş: Oturum varsa kullanıcıyı döndürür.
  Future<models.User?> getCurrentUser() async {
    if (account == null) {
      log('Appwrite istemcisi başlatılmadı, kullanıcı boş döndürülüyor');
      return null;
    }
    try {
      return await account!.get();
    } on AppwriteException {
      return null; // Oturum yoksa null döndür.
    }
  }
}
