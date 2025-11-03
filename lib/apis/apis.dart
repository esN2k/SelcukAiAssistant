import 'dart:developer';

import 'package:google_generative_ai/google_generative_ai.dart';

import 'package:selcukaiassistant/helper/global.dart';

class APIs {
  static Future<String> getAnswer(String question) async {
    try {
      log('AI arayüzü çağrılıyor, API Key: ${apiKey.substring(0, 10)}...');

      final model = GenerativeModel(
        model: 'gemini-2.0-flashfl',
        apiKey: apiKey,
      );

      // ... (prompt kısmı aynı kalabilir) ...
      final prompt = '''
Siz dost canlısı ve profesyonel bir yapay zeka asistanısınız. Lütfen kullanıcı sorularını Türkçe yanıtlayın

Sen, Selçuk Üniversitesi (SÜ) öğrencileri ve akademik/idari personeli için çalışan, resmi bilgilere dayalı cevaplar veren bir AI asistansın.
Tüm soruları, Selçuk Üniversitesi'nin güncel yönetmeliklerine, akademik takvimine, duyurularına ve iç prosedürlerine göre yanıtlamalısın.
Yanıtlarında profesyonel, resmi ve kurallara uygun bir dil kullan.
Bilmediğin veya emin olmadığın SÜ ile ilgili konularda, tahminde bulunmak yerine dürüstçe 'Bu konuda güncel Selçuk Üniversitesi bilgisine sahip değilim' veya 'Lütfen ilgili birime danışınız' şeklinde yanıt ver.
Kesinlikle Selçuk Üniversitesi ile ilgisi olmayan veya genel kültür bilgisi gerektiren sorulara da SÜ bağlamını gözeterek cevap vermekten kaçın.

Yanıt verirken, içeriğinizi daha anlaşılır ve okunması kolay hale getirmek için Markdown biçimlendirmesini kullanabilirsiniz. Örneğin:
- Önemli noktaları vurgulamak için **kalın** kullanın
- Teknik terimleri belirtmek için **kod** kullanın
- Kodu görüntülemek için **kod blokları** kullanın
- İçeriği düzenlemek için liste ve başlıklar kullanın
- Önemli bilgilere atıfta bulunmak için > kullanın

Kullanıcı sorusu:$question
''';

      final content = [Content.text(prompt)];
      final res = await model.generateContent(
        content,
        safetySettings: [
          SafetySetting(HarmCategory.dangerousContent, HarmBlockThreshold.none),
          SafetySetting(HarmCategory.sexuallyExplicit, HarmBlockThreshold.none),
          SafetySetting(HarmCategory.harassment, HarmBlockThreshold.none),
          SafetySetting(HarmCategory.hateSpeech, HarmBlockThreshold.none),
        ],
      );

      // 2. ADIM: Varsayılan yanıtı Türkçeleştirin
      final answer = res.text ?? 'Üzgünüm, bir yanıt oluşturulamadı.';
      log('AI Yanıtı: ${answer.substring(0, answer.length > 100 ? 100 : answer.length)}...');

      return answer;
    } catch (e) {
      // 3. ADIM: Hata mesajını Türkçeleştirin ve detayı log'layın
      log('AI ARAYÜZÜ ÇAĞRISI HATASI: $e'); // Gerçek hatayı terminalde görün
      return 'Hata: Servis geçici olarak kullanılamıyor. Lütfen daha sonra tekrar deneyin. Sorun devam ederse ağ bağlantınızı veya API anahtarı yapılandırmanızı kontrol edin. Hata Detayı: $e';
    }
  }
}
