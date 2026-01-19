/// DOSYA ADI: appwrite_service.dart
/// AMAÇ: Appwrite üzerinden kullanıcı işlemlerini yönetmek.
/// NE YAPAR:
///   - Kayıt, oturum açma ve çıkış işlemlerini yürütür.
///   - Mevcut kullanıcı bilgisini döndürür.
///   - Heartbeat ile bağlantıyı canlı tutar.
/// BAĞIMLILIKLAR:
///   - appwrite
///   - flutter_dotenv
/// SON DEĞİŞİKLİK: 18.01.2026
library;

import 'dart:async';
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

    // Heartbeat başlat - her 5 dakikada bir bağlantıyı kontrol et
    _startHeartbeat();
  }

  // İstemci ve account opsiyoneldir; başlatılmamış olabilir.
  Client? client;
  Account? account;
  Timer? _heartbeatTimer;

  /// Giriş: yok.
  /// Çıkış: yok.
  /// İşleyiş: Periyodik heartbeat başlatır, bağlantıyı canlı tutar.
  void _startHeartbeat() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = Timer.periodic(const Duration(minutes: 5), (_) async {
      await _performHeartbeat();
    });
  }

  /// Giriş: yok.
  /// Çıkış: yok.
  /// İşleyiş: Appwrite bağlantısını test eder, hata varsa loglar.
  Future<void> _performHeartbeat() async {
    if (account == null) return;

    try {
      await account!.get();
      log('✓ Appwrite heartbeat OK');
    } on AppwriteException catch (e) {
      log('✗ Appwrite heartbeat failed: ${e.message}');
      // Bağlantı kopmuşsa yeniden bağlanmayı dene
      if (e.code == 401 || e.code == 403) {
        log('Appwrite session expired, reconnection may be needed');
      }
    } on Exception catch (e) {
      log('✗ Appwrite heartbeat error: $e');
    }
  }

  /// Giriş: yok.
  /// Çıkış: yok.
  /// İşleyiş: Heartbeat timer'ı durdurur.
  void dispose() {
    _heartbeatTimer?.cancel();
    _heartbeatTimer = null;
  }

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
