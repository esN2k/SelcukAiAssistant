import 'dart:convert';
import 'dart:developer';

import 'package:http/http.dart' as http;

/// 语音服务类，用于处理语音转文字功能
class VoiceService {
  static const String _baseUrl =
      'http://your-server-url.com/api'; // 替换为实际的服务器地址

  /// 将音频文件发送到服务器进行语音识别
  /// [audioPath] 音频文件路径
  /// 返回识别出的文字内容
  static Future<String> speechToText(String audioPath) async {
    try {
      log('开始语音识别，音频文件路径: $audioPath');

      final request = http.MultipartRequest(
        'POST',
        Uri.parse('$_baseUrl/speech-to-text'),
      );

      // 添加音频文件
      request.files.add(
        await http.MultipartFile.fromPath('audio', audioPath),
      );

      // 添加其他参数
      request.fields['language'] = 'zh-CN'; // 中文识别

      final response = await request.send();
      final responseData = await response.stream.bytesToString();

      if (response.statusCode == 200) {
        final jsonData = json.decode(responseData);
        final recognizedText = (jsonData['text'] as String?) ?? '';
        log('语音识别成功: $recognizedText');
        return recognizedText;
      } else {
        log('语音识别失败，状态码: ${response.statusCode}');
        return '语音识别失败，请重试';
      }
    } catch (e) {
      log('语音识别异常: $e');
      return '语音识别出错，请检查网络连接';
    }
  }

  /// 检查服务器连接状态
  static Future<bool> checkServerConnection() async {
    try {
      final response = await http.get(
        Uri.parse('$_baseUrl/health'),
        headers: {'Content-Type': 'application/json'},
      ).timeout(const Duration(seconds: 5));

      return response.statusCode == 200;
    } catch (e) {
      log('服务器连接检查失败: $e');
      return false;
    }
  }
}
