import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStore {
  SecureStore._();

  static const FlutterSecureStorage _storage = FlutterSecureStorage();

  static String _key(String provider) => 'api_key_$provider';

  static Future<void> writeApiKey(String provider, String apiKey) {
    return _storage.write(key: _key(provider), value: apiKey);
  }

  static Future<String?> readApiKey(String provider) {
    return _storage.read(key: _key(provider));
  }

  static Future<void> deleteApiKey(String provider) {
    return _storage.delete(key: _key(provider));
  }

  static Future<void> clearAll() => _storage.deleteAll();
}
