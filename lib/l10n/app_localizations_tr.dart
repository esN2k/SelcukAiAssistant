// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Turkish (`tr`).
class AppLocalizationsTr extends AppLocalizations {
  AppLocalizationsTr([String locale = 'tr']) : super(locale);

  @override
  String get appTitle => 'Selçuk AI Asistanı';

  @override
  String get appSubtitle => 'Gizliliğe odaklı akademik asistan';

  @override
  String get splashSubtitle => 'Selçuk AI Asistanı';

  @override
  String get ok => 'Tamam';

  @override
  String get cancel => 'İptal';

  @override
  String get delete => 'Sil';

  @override
  String get clear => 'Temizle';

  @override
  String get rename => 'Yeniden adlandır';

  @override
  String get newChat => 'Yeni sohbet';

  @override
  String get loginTitle => 'Hoş geldiniz';

  @override
  String get loginSubtitle => 'Devam etmek için giriş yapın';

  @override
  String get loginButton => 'Giriş yap';

  @override
  String get loginNoAccount => 'Hesabınız yok mu?';

  @override
  String get loginCreateAccount => 'Kayıt olun';

  @override
  String get loginSuccessTitle => 'Başarılı';

  @override
  String get loginSuccessMessage => 'Giriş yapıldı!';

  @override
  String get loginErrorTitle => 'Hata';

  @override
  String get registerTitle => 'Hesap oluştur';

  @override
  String get registerSubtitle => 'Asistanı kullanmaya başlayın';

  @override
  String get registerButton => 'Kayıt ol';

  @override
  String get registerHaveAccount => 'Zaten hesabınız var mı?';

  @override
  String get registerSignIn => 'Giriş yap';

  @override
  String get registerSuccessTitle => 'Başarılı';

  @override
  String get registerSuccessMessage => 'Kayıt tamamlandı. Hoş geldiniz!';

  @override
  String get registerErrorTitle => 'Hata';

  @override
  String get nameLabel => 'Ad soyad';

  @override
  String get emailLabel => 'E-posta';

  @override
  String get passwordLabel => 'Şifre';

  @override
  String get confirmPasswordLabel => 'Şifre tekrar';

  @override
  String get nameRequired => 'Ad soyad gerekli';

  @override
  String get emailRequired => 'E-posta gerekli';

  @override
  String get invalidEmail => 'Geçerli bir e-posta girin';

  @override
  String get passwordRequired => 'Şifre gerekli';

  @override
  String get passwordMinLength => 'Şifre en az 8 karakter olmalı';

  @override
  String get confirmPasswordRequired => 'Şifre tekrarını girin';

  @override
  String get passwordsDoNotMatch => 'Şifreler eşleşmiyor';

  @override
  String get onboardingTitle1 => 'Bana bir şey sor';

  @override
  String get onboardingSubtitle1 =>
      'En iyi yol arkadaşın olabilirim. Bana her şeyi sor, yardımcı olayım!';

  @override
  String get onboardingTitle2 => 'Hayalden gerçeğe';

  @override
  String get onboardingSubtitle2 =>
      'Sadece hayal et ve söyle. Senin için harika bir şey yaratayım!';

  @override
  String get onboardingNext => 'Sıradaki';

  @override
  String get onboardingDone => 'Bitti';

  @override
  String get settingsTitle => 'Ayarlar';

  @override
  String get sectionAppearance => 'GÖRÜNÜM';

  @override
  String get sectionLanguage => 'DİL';

  @override
  String get sectionAiModel => 'YAPAY ZEKA MODELİ';

  @override
  String get sectionChatSettings => 'SOHBET AYARLARI';

  @override
  String get sectionServer => 'SUNUCU';

  @override
  String get sectionDiagnostics => 'TANILAMA';

  @override
  String get sectionStatistics => 'İSTATİSTİKLER';

  @override
  String get sectionDataManagement => 'VERİ YÖNETİMİ';

  @override
  String get sectionAbout => 'HAKKINDA';

  @override
  String get darkModeTitle => 'Karanlık mod';

  @override
  String get darkModeSubtitle =>
      'Aydınlık ve karanlık tema arasında geçiş yapın';

  @override
  String get languageTitle => 'Uygulama dili';

  @override
  String get languageSubtitle => 'Tercih ettiğiniz dili seçin';

  @override
  String get languageTurkish => 'Türkçe';

  @override
  String get languageEnglish => 'İngilizce';

  @override
  String get modelLabel => 'Model';

  @override
  String get modelNotSelected => 'Seçilmedi';

  @override
  String get modelAvailable => 'Uygun';

  @override
  String get modelUnavailable => 'Kullanılamaz';

  @override
  String get modelLocalSection => 'Yerel modeller';

  @override
  String get modelRemoteSection => 'Uzak / API modelleri';

  @override
  String modelInstallCommand(String command) {
    return 'Kurulum: $command';
  }

  @override
  String modelUnavailableReason(String reason) {
    return 'Neden: $reason';
  }

  @override
  String get modelSearchHint => 'Model ara...';

  @override
  String get modelNoResults => 'Model bulunamadı';

  @override
  String get modelApiKeyRequired => 'API anahtarı gerekli';

  @override
  String get modelNotInstalled => 'Yüklü değil';

  @override
  String modelContextLength(int count) {
    return 'Bağlam: $count belirteç';
  }

  @override
  String get backendUrlTitle => 'Sunucu URL\'si';

  @override
  String backendUrlSubtitle(String current) {
    return 'Geçerli: $current';
  }

  @override
  String get backendUrlHint => 'https://example.com:8000 veya /api';

  @override
  String get backendUrlSave => 'Kaydet';

  @override
  String get backendUrlClear => 'Özel ayarı temizle';

  @override
  String get backendUrlSaved => 'Sunucu URL\'si kaydedildi';

  @override
  String get backendUrlCleared => 'Sunucu URL\'si özelleştirmesi temizlendi';

  @override
  String get diagnosticsTitle => 'Tanılama';

  @override
  String get diagnosticsSubtitle => 'Backend bağlantısı ve streaming testi';

  @override
  String get selectModelTitle => 'Model seç';

  @override
  String get voiceInputTitle => 'Sesli giriş';

  @override
  String get voiceInputSubtitle =>
      'Sesli mesajlar için mikrofonu etkinleştirin';

  @override
  String get markdownSupportTitle => 'Markdown desteği';

  @override
  String get markdownSupportSubtitle => 'Biçimlendirilmiş metin ve kodu göster';

  @override
  String get ragEnabledTitle => 'Kaynaklı yanıtlar (RAG)';

  @override
  String get ragEnabledSubtitle =>
      'Uygunsa dizinlenen belgelerden yanıt üretir';

  @override
  String get ragStrictTitle => 'Sıkı kaynak modu';

  @override
  String get ragStrictSubtitle => 'Kaynak yoksa sabit uyarı verir';

  @override
  String get totalConversations => 'Toplam konuşma';

  @override
  String get totalMessages => 'Toplam mesaj';

  @override
  String get clearAllConversationsTitle => 'Tüm konuşmaları temizle';

  @override
  String get clearAllConversationsSubtitle => 'Tüm sohbet geçmişini silin';

  @override
  String get clearAllDataTitle => 'Tüm verileri temizle';

  @override
  String get clearAllDataMessage =>
      'Tüm konuşmaları silmek istediğinize emin misiniz? Bu işlem geri alınamaz.';

  @override
  String get deleteAll => 'Tümünü sil';

  @override
  String get clearAllSuccessTitle => 'Başarılı';

  @override
  String get clearAllSuccessMessage => 'Tüm konuşmalar silindi';

  @override
  String get versionLabel => 'Sürüm';

  @override
  String get developerLabel => 'Geliştirici';

  @override
  String get developerValue => 'Selçuk AI';

  @override
  String get deleteConversationTitle => 'Konuşmayı sil';

  @override
  String get deleteConversationMessage =>
      'Bu konuşmayı silmek istediğinize emin misiniz? Bu işlem geri alınamaz.';

  @override
  String get renameConversationTitle => 'Konuşmayı yeniden adlandır';

  @override
  String get renameConversationHint => 'Yeni başlık girin';

  @override
  String get searchConversationsHint => 'Konuşmaları ara...';

  @override
  String get noConversationsFound => 'Konuşma bulunamadı';

  @override
  String get noConversationsYet => 'Henüz konuşma yok';

  @override
  String conversationsCount(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count konuşma',
      one: '1 konuşma',
      zero: '0 konuşma',
    );
    return '$_temp0';
  }

  @override
  String get pinnedLabel => 'Sabitlenenler';

  @override
  String get archivedLabel => 'Arşivlenenler';

  @override
  String get last7DaysLabel => 'Son 7 gün';

  @override
  String get olderLabel => 'Daha eski';

  @override
  String get pinConversation => 'Sabitle';

  @override
  String get unpinConversation => 'Sabitlemeyi kaldır';

  @override
  String get archiveConversation => 'Arşivle';

  @override
  String get unarchiveConversation => 'Arşivden çıkar';

  @override
  String get todayLabel => 'Bugün';

  @override
  String get yesterdayLabel => 'Dün';

  @override
  String daysAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count gün önce',
      one: '1 gün önce',
    );
    return '$_temp0';
  }

  @override
  String weeksAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count hafta önce',
      one: '1 hafta önce',
    );
    return '$_temp0';
  }

  @override
  String monthsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count ay önce',
      one: '1 ay önce',
    );
    return '$_temp0';
  }

  @override
  String yearsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count yıl önce',
      one: '1 yıl önce',
    );
    return '$_temp0';
  }

  @override
  String get clearConversationTitle => 'Konuşmayı temizle';

  @override
  String get clearConversationMessage =>
      'Bu konuşmayı temizlemek istediğinize emin misiniz? Bu işlem geri alınamaz.';

  @override
  String get listeningIndicator => 'Dinleniyor... (bırakınca durur)';

  @override
  String get messageHint => 'Selçuk AI Asistanı\'na yazın...';

  @override
  String get imageSelectedTitle => 'Görsel seçildi';

  @override
  String imageSelectedMessage(String fileName) {
    return 'Görsel: $fileName';
  }

  @override
  String get startConversationTitle => 'Bir sohbet başlatın';

  @override
  String get startConversationSubtitle => 'Bana istediğinizi sorun!';

  @override
  String get suggestedPrompt1 => 'Kuantum hesaplamayı açıkla';

  @override
  String get suggestedPrompt2 => 'Bir şiir yaz';

  @override
  String get suggestedPrompt3 => 'Kod konusunda yardım';

  @override
  String get streamErrorTitle => 'Akış hatası';

  @override
  String streamErrorMessage(String error) {
    return '$error';
  }

  @override
  String get streamInterruptedTag => '[Akış kesildi]';

  @override
  String get copyAction => 'Kopyala';

  @override
  String get editMessageTitle => 'Mesajı düzenle';

  @override
  String get editMessageHint => 'Mesajınızı güncelleyin';

  @override
  String get editMessageAction => 'Yeniden gönder';

  @override
  String get regenerateAction => 'Yeniden üret';

  @override
  String get retryAction => 'Tekrar dene';

  @override
  String get sourcesTitle => 'Kaynaklar';

  @override
  String get diagnosticsConnectionSection => 'BAĞLANTI';

  @override
  String get diagnosticsBaseUrlLabel => 'Temel URL';

  @override
  String diagnosticsBaseUrlSource(String source) {
    return 'Kaynak: $source';
  }

  @override
  String get diagnosticsPlatformLabel => 'Platform';

  @override
  String get diagnosticsLatencyLabel => 'Gecikme';

  @override
  String get diagnosticsLatencyUnavailable => 'Henüz gecikme ölçülmedi.';

  @override
  String get diagnosticsModelLabel => 'Seçili model';

  @override
  String get diagnosticsModelAvailable => 'Uygun';

  @override
  String get diagnosticsModelUnavailable => 'Kullanılamıyor';

  @override
  String get diagnosticsOllamaLabel => 'Ollama sağlığı';

  @override
  String get diagnosticsOllamaReady => 'Hazır';

  @override
  String get diagnosticsOllamaUnavailable => 'Uygun değil';

  @override
  String get diagnosticsOllamaButton => '/health/ollama test et';

  @override
  String diagnosticsOllamaDetail(
      String status, String model, String availability, String count) {
    return 'Durum: $status | Model: $model | $availability | Modeller: $count';
  }

  @override
  String get diagnosticsHfLabel => 'HF GPU Hazır';

  @override
  String get diagnosticsHfReady => 'Hazır';

  @override
  String get diagnosticsHfUnavailable => 'Uygun değil';

  @override
  String get diagnosticsHfButton => '/health/hf test et';

  @override
  String diagnosticsHfDetail(
      String gpu, String torch, String cuda, String transformers, String bnb) {
    return 'GPU: $gpu | Torch: $torch | CUDA: $cuda | Transformers: $transformers | bitsandbytes: $bnb';
  }

  @override
  String get diagnosticsHealthButton => '/health test et';

  @override
  String get diagnosticsModelsButton => '/models test et';

  @override
  String get diagnosticsSourceOverride => 'Kullanıcı özelleştirmesi';

  @override
  String get diagnosticsSourceDartDefine => 'Dart tanımı';

  @override
  String get diagnosticsSourceDotenv => 'Dotenv';

  @override
  String get diagnosticsSourceWebRelease => 'Web sürümü (/api)';

  @override
  String get diagnosticsSourceWebDev => 'Web geliştirme (localhost)';

  @override
  String get diagnosticsSourceAndroidEmulator => 'Android emülatörü (10.0.2.2)';

  @override
  String get diagnosticsSourceDesktop => 'Masaüstü (localhost)';

  @override
  String get diagnosticsChatButton => '/chat test et';

  @override
  String get diagnosticsStreamButton => '/chat/stream test et';

  @override
  String get diagnosticsStreamRunning => 'Akış sürüyor...';

  @override
  String get diagnosticsLastErrorTitle => 'Son hata';

  @override
  String get diagnosticsErrorStatusLabel => 'Durum';

  @override
  String get diagnosticsErrorBodyLabel => 'İçerik';

  @override
  String get diagnosticsErrorHeadersLabel => 'Üstbilgiler';

  @override
  String get diagnosticsNoErrors => 'Henüz hata yok.';

  @override
  String get diagnosticsStreamSampleTitle => 'SSE örneği';

  @override
  String get diagnosticsNoStreamSample => 'Akış olayı yakalanmadı.';

  @override
  String get diagnosticsLogsTitle => 'Tanılama günlüğü';

  @override
  String get diagnosticsCopyLog => 'Günlüğü kopyala';

  @override
  String get diagnosticsNoLogs => 'Henüz tanılama yapılmadı.';

  @override
  String get diagnosticsTestMessage => 'Merhaba';

  @override
  String get microphonePermissionRequired =>
      'Sesli giriş için mikrofon izni gerekli';

  @override
  String get speechNotAvailable => 'Ses tanıma kullanılamıyor';

  @override
  String get enterMessagePrompt =>
      'Lütfen bir mesaj yazın veya sesli giriş kullanın!';

  @override
  String get exportFailedTitle => 'Dışa aktarma başarısız';

  @override
  String get noMessagesToExport => 'Dışa aktarılacak mesaj yok';

  @override
  String get exportSuccessTitle => 'Dışa aktarma başarılı';

  @override
  String exportSuccessMessage(String path) {
    return 'Şuraya kaydedildi: $path\\nAyrıca panoya kopyalandı';
  }

  @override
  String get exportSuccessWebMessage => 'Dosya indirildi ve panoya kopyalandı';

  @override
  String get logout => 'Çıkış';

  @override
  String get clearChat => 'Sohbeti temizle';

  @override
  String get exportChat => 'Sohbeti dışa aktar';

  @override
  String get logoutSuccessTitle => 'Başarılı';

  @override
  String get logoutSuccessMessage => 'Çıkış yapıldı';

  @override
  String get logoutErrorTitle => 'Hata';

  @override
  String get copiedToClipboard => 'Panoya kopyalandı';

  @override
  String yesterdayAt(String time) {
    return 'Dün $time';
  }

  @override
  String get aiThinking => 'Yapay zeka düşünüyor...';

  @override
  String get infoTitle => 'Bilgi';

  @override
  String get successTitle => 'Başarılı';

  @override
  String get errorTitle => 'Hata';

  @override
  String get imagePickerErrorTitle => 'Hata';

  @override
  String imagePickerErrorMessage(String error) {
    return 'Görsel seçilemedi: $error';
  }

  @override
  String get chooseImageSourceTitle => 'Görsel kaynağını seçin';

  @override
  String get cameraLabel => 'Kamera';

  @override
  String get galleryLabel => 'Galeri';

  @override
  String get appwritePingSuccess => 'Appwrite bağlantısı başarılı!';

  @override
  String get appwritePingNoSession =>
      'Appwrite bağlantısı var ama oturum açık değil.';

  @override
  String appwritePingError(String error) {
    return 'Appwrite ping hatası: $error';
  }

  @override
  String get sendPingTooltip => 'Ping gönder';

  @override
  String get logoutTooltip => 'Çıkış';

  @override
  String get assistantTitle => 'Yapay Zeka Asistanı';

  @override
  String get assistantHint =>
      'Bir mesaj yazın veya sesli giriş için basılı tutun...';

  @override
  String get listeningStatus => 'Ses girişi dinleniyor...';

  @override
  String get startChatHint => 'Yapay Zeka Asistanı ile konuşmaya başlayın!';

  @override
  String get errorInvalidRequest => 'Hata: Geçersiz istek';

  @override
  String get errorInvalidRequestFormat => 'Hata: Geçersiz istek formatı.';

  @override
  String get errorServiceUnavailable =>
      'Hata: Yapay zeka hizmeti kullanılamıyor.';

  @override
  String get errorTimeout => 'Hata: Yanıt zaman aşımına uğradı.';

  @override
  String get errorBackendUnavailable => 'Hata: Sunucu hizmeti kullanılamıyor.';

  @override
  String get errorNoInternet => 'Hata: İnternet bağlantısı yok.';

  @override
  String get errorInvalidServerResponse => 'Hata: Geçersiz sunucu yanıtı.';

  @override
  String get errorUnexpected => 'Hata: Beklenmeyen hata.';

  @override
  String get noResponseGenerated => 'Üzgünüm, yanıt üretilemedi.';

  @override
  String get requestTimeoutMessage =>
      'İstek zaman aşımına uğradı. Lütfen tekrar deneyin.';

  @override
  String get speechRecognitionFailed =>
      'Ses tanıma başarısız oldu. Lütfen tekrar deneyin.';

  @override
  String get speechRecognitionError =>
      'Ses tanıma hatası. Lütfen ağ bağlantınızı kontrol edin.';

  @override
  String get serverConnectionFailed => 'Sunucu bağlantısı başarısız.';
}
