import 'package:appwrite/appwrite.dart';
import 'package:appwrite/models.dart' as models;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class AppwriteService {
  AppwriteService() {
    client = Client()
      ..setEndpoint(dotenv.env['APPWRITE_ENDPOINT']!)
      ..setProject(dotenv.env['APPWRITE_PROJECT_ID']!);
    account = Account(client);
  }

  late final Client client;
  late final Account account;

  Future<models.User> register({
    required String email,
    required String password,
    String? name,
  }) async {
    try {
      return await account.create(
        userId: ID.unique(),
        email: email,
        password: password,
        name: name,
      );
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Kayıt oluşturulamadı');
    }
  }

  Future<models.Session> createSession(String email, String password) async {
    try {
      return await account.createEmailPasswordSession(
        email: email,
        password: password,
      );
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Oturum açılamadı');
    }
  }

  Future<void> deleteCurrentSession() async {
    try {
      await account.deleteSession(sessionId: 'current');
    } on AppwriteException catch (error) {
      throw Exception(error.message ?? 'Oturum kapatılamadı');
    }
  }

  Future<models.User?> getCurrentUser() async {
    try {
      return await account.get();
    } on AppwriteException {
      return null; // Oturum yoksa null dön
    }
  }
}
