// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for Turkish (`tr`).
class AppLocalizationsTr extends AppLocalizations {
  AppLocalizationsTr([String locale = 'tr']) : super(locale);

  @override
  String get appTitle => 'SelÃ§uk AI AsistanÄ±';

  @override
  String get appSubtitle => 'SelÃ§uk Ãœniversitesi Yapay Zeka AsistanÄ±';

  @override
  String get splashSubtitle => 'SelÃ§uk Ãœniversitesi Yapay Zeka AsistanÄ±';

  @override
  String get ok => 'Tamam';

  @override
  String get cancel => 'Ä°ptal';

  @override
  String get delete => 'Sil';

  @override
  String get clear => 'Temizle';

  @override
  String get rename => 'Yeniden adlandÄ±r';

  @override
  String get newChat => 'Yeni sohbet';

  @override
  String get loginTitle => 'HoÅŸ geldiniz';

  @override
  String get loginSubtitle => 'Devam etmek iÃ§in giriÅŸ yapÄ±n';

  @override
  String get loginButton => 'GiriÅŸ yap';

  @override
  String get loginNoAccount => 'HesabÄ±nÄ±z yok mu?';

  @override
  String get loginCreateAccount => 'KayÄ±t olun';

  @override
  String get loginSuccessTitle => 'BaÅŸarÄ±lÄ±';

  @override
  String get loginSuccessMessage => 'GiriÅŸ yapÄ±ldÄ±!';

  @override
  String get loginErrorTitle => 'Hata';

  @override
  String get registerTitle => 'Hesap oluÅŸtur';

  @override
  String get registerSubtitle => 'AsistanÄ± kullanmaya baÅŸlayÄ±n';

  @override
  String get registerButton => 'KayÄ±t ol';

  @override
  String get registerHaveAccount => 'Zaten hesabÄ±nÄ±z var mÄ±?';

  @override
  String get registerSignIn => 'GiriÅŸ yap';

  @override
  String get registerSuccessTitle => 'BaÅŸarÄ±lÄ±';

  @override
  String get registerSuccessMessage => 'KayÄ±t tamamlandÄ±. HoÅŸ geldiniz!';

  @override
  String get registerErrorTitle => 'Hata';

  @override
  String get nameLabel => 'Ad soyad';

  @override
  String get emailLabel => 'E-posta';

  @override
  String get passwordLabel => 'Åifre';

  @override
  String get confirmPasswordLabel => 'Åifre tekrar';

  @override
  String get nameRequired => 'Ad soyad gerekli';

  @override
  String get emailRequired => 'E-posta gerekli';

  @override
  String get invalidEmail => 'GeÃ§erli bir e-posta girin';

  @override
  String get passwordRequired => 'Åifre gerekli';

  @override
  String get passwordMinLength => 'Åifre en az 8 karakter olmalÄ±';

  @override
  String get confirmPasswordRequired => 'Åifre tekrarÄ±nÄ± girin';

  @override
  String get passwordsDoNotMatch => 'Åifreler eÅŸleÅŸmiyor';

  @override
  String get onboardingTitle1 => 'Bana bir ÅŸey sor';

  @override
  String get onboardingSubtitle1 =>
      'En iyi yol arkadaÅŸÄ±n olabilirim. Bana her ÅŸeyi sor, yardÄ±mcÄ± olayÄ±m!';

  @override
  String get onboardingTitle2 => 'Hayalden gerÃ§eÄŸe';

  @override
  String get onboardingSubtitle2 =>
      'Sadece hayal et ve sÃ¶yle. Senin iÃ§in harika bir ÅŸey yaratayÄ±m!';

  @override
  String get onboardingNext => 'SÄ±radaki';

  @override
  String get onboardingDone => 'Bitti';

  @override
  String get settingsTitle => 'Ayarlar';

  @override
  String get sectionAppearance => 'GÃ–RÃœNÃœM';

  @override
  String get sectionLanguage => 'DÄ°L';

  @override
  String get sectionAiModel => 'YAPAY ZEKA MODELÄ°';

  @override
  String get sectionChatSettings => 'SOHBET AYARLARI';

  @override
  String get sectionServer => 'SUNUCU';

  @override
  String get sectionDiagnostics => 'TANILAMA';

  @override
  String get sectionStatistics => 'Ä°STATÄ°STÄ°KLER';

  @override
  String get sectionDataManagement => 'VERÄ° YÃ–NETÄ°MÄ°';

  @override
  String get sectionAbout => 'HAKKINDA';

  @override
  String get darkModeTitle => 'KaranlÄ±k mod';

  @override
  String get darkModeSubtitle =>
      'AydÄ±nlÄ±k ve karanlÄ±k tema arasÄ±nda geÃ§iÅŸ yapÄ±n';

  @override
  String get languageTitle => 'Uygulama dili';

  @override
  String get languageSubtitle => 'Tercih ettiÄŸiniz dili seÃ§in';

  @override
  String get languageTurkish => 'TÃ¼rkÃ§e';

  @override
  String get languageEnglish => 'Ä°ngilizce';

  @override
  String get modelLabel => 'Model';

  @override
  String get modelNotSelected => 'SeÃ§ilmedi';

  @override
  String get modelAvailable => 'Uygun';

  @override
  String get modelUnavailable => 'Kullanilamaz';

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
  String get diagnosticsSubtitle => 'Sunucu bağlantısını ve akışı test edin';

  @override
  String get selectModelTitle => 'Model seÃ§in';

  @override
  String get voiceInputTitle => 'Sesli giriÅŸ';

  @override
  String get voiceInputSubtitle =>
      'Sesli mesajlar iÃ§in mikrofonu etkinleÅŸtirin';

  @override
  String get markdownSupportTitle => 'Markdown desteÄŸi';

  @override
  String get markdownSupportSubtitle =>
      'BiÃ§imlendirilmiÅŸ metin ve kodu gÃ¶ster';

  @override
  String get totalConversations => 'Toplam konuÅŸma';

  @override
  String get totalMessages => 'Toplam mesaj';

  @override
  String get clearAllConversationsTitle => 'TÃ¼m konuÅŸmalarÄ± temizle';

  @override
  String get clearAllConversationsSubtitle => 'TÃ¼m sohbet geÃ§miÅŸini silin';

  @override
  String get clearAllDataTitle => 'TÃ¼m verileri temizle';

  @override
  String get clearAllDataMessage =>
      'TÃ¼m konuÅŸmalarÄ± silmek istediÄŸinize emin misiniz? Bu iÅŸlem geri alÄ±namaz.';

  @override
  String get deleteAll => 'TÃ¼mÃ¼nÃ¼ sil';

  @override
  String get clearAllSuccessTitle => 'BaÅŸarÄ±lÄ±';

  @override
  String get clearAllSuccessMessage => 'TÃ¼m konuÅŸmalar silindi';

  @override
  String get versionLabel => 'SÃ¼rÃ¼m';

  @override
  String get developerLabel => 'GeliÅŸtirici';

  @override
  String get developerValue => 'SelÃ§uk AI';

  @override
  String get deleteConversationTitle => 'KonuÅŸmayÄ± sil';

  @override
  String get deleteConversationMessage =>
      'Bu konuÅŸmayÄ± silmek istediÄŸinize emin misiniz? Bu iÅŸlem geri alÄ±namaz.';

  @override
  String get renameConversationTitle => 'KonuÅŸmayÄ± yeniden adlandÄ±r';

  @override
  String get renameConversationHint => 'Yeni baÅŸlÄ±k girin';

  @override
  String get searchConversationsHint => 'KonuÅŸmalarÄ± ara...';

  @override
  String get noConversationsFound => 'KonuÅŸma bulunamadÄ±';

  @override
  String get noConversationsYet => 'HenÃ¼z konuÅŸma yok';

  @override
  String conversationsCount(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count konuÅŸma',
      one: '1 konuÅŸma',
      zero: '0 konuÅŸma',
    );
    return '$_temp0';
  }

  @override
  String get todayLabel => 'BugÃ¼n';

  @override
  String get yesterdayLabel => 'DÃ¼n';

  @override
  String daysAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count gÃ¼n Ã¶nce',
      one: '1 gÃ¼n Ã¶nce',
    );
    return '$_temp0';
  }

  @override
  String weeksAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count hafta Ã¶nce',
      one: '1 hafta Ã¶nce',
    );
    return '$_temp0';
  }

  @override
  String monthsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count ay Ã¶nce',
      one: '1 ay Ã¶nce',
    );
    return '$_temp0';
  }

  @override
  String yearsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count yÄ±l Ã¶nce',
      one: '1 yÄ±l Ã¶nce',
    );
    return '$_temp0';
  }

  @override
  String get clearConversationTitle => 'KonuÅŸmayÄ± temizle';

  @override
  String get clearConversationMessage =>
      'Bu konuÅŸmayÄ± temizlemek istediÄŸinize emin misiniz? Bu iÅŸlem geri alÄ±namaz.';

  @override
  String get listeningIndicator => 'Dinleniyor... (bÄ±rakÄ±nca durur)';

  @override
  String get messageHint => 'SelÃ§uk AI AsistanÄ±\'na yazÄ±n...';

  @override
  String get imageSelectedTitle => 'GÃ¶rsel seÃ§ildi';

  @override
  String imageSelectedMessage(String fileName) {
    return 'GÃ¶rsel: $fileName';
  }

  @override
  String get startConversationTitle => 'Bir sohbet baÅŸlatÄ±n';

  @override
  String get startConversationSubtitle => 'Bana istediÄŸinizi sorun!';

  @override
  String get suggestedPrompt1 => 'Kuantum hesaplamayÄ± aÃ§Ä±kla';

  @override
  String get suggestedPrompt2 => 'Bir ÅŸiir yaz';

  @override
  String get suggestedPrompt3 => 'Kod konusunda yardÄ±m';

  @override
  String get streamErrorTitle => 'AkÄ±ÅŸ hatasÄ±';

  @override
  String streamErrorMessage(String error) {
    return '$error';
  }

  @override
  String get streamInterruptedTag => '[AkÄ±ÅŸ kesildi]';

  @override
  String get diagnosticsConnectionSection => 'BAĞLANTI';

  @override
  String get diagnosticsBaseUrlLabel => 'Temel URL';

  @override
  String get diagnosticsModelLabel => 'Seçili model';

  @override
  String get diagnosticsModelAvailable => 'Uygun';

  @override
  String get diagnosticsModelUnavailable => 'Kullanılamıyor';

  @override
  String get diagnosticsHealthButton => '/health test et';

  @override
  String get diagnosticsModelsButton => '/models test et';

  @override
  String get diagnosticsChatButton => '/chat test et';

  @override
  String get diagnosticsStreamButton => '/chat/stream test et';

  @override
  String get diagnosticsStreamRunning => 'Akış sürüyor...';

  @override
  String get diagnosticsLastErrorTitle => 'Son hata';

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
      'Sesli giriÅŸ iÃ§in mikrofon izni gerekli';

  @override
  String get speechNotAvailable => 'Ses tanÄ±ma kullanÄ±lamÄ±yor';

  @override
  String get enterMessagePrompt =>
      'LÃ¼tfen bir mesaj yazÄ±n veya sesli giriÅŸ kullanÄ±n!';

  @override
  String get exportFailedTitle => 'DÄ±ÅŸa aktarma baÅŸarÄ±sÄ±z';

  @override
  String get noMessagesToExport => 'DÄ±ÅŸa aktarÄ±lacak mesaj yok';

  @override
  String get exportSuccessTitle => 'DÄ±ÅŸa aktarma baÅŸarÄ±lÄ±';

  @override
  String exportSuccessMessage(String path) {
    return 'Åuraya kaydedildi: $path\\nAyrÄ±ca panoya kopyalandÄ±';
  }

  @override
  String get exportSuccessWebMessage =>
      'Dosya indirildi ve panoya kopyalandÅ½Ã±';

  @override
  String get logout => 'Ã‡Ä±kÄ±ÅŸ';

  @override
  String get clearChat => 'Sohbeti temizle';

  @override
  String get exportChat => 'Sohbeti dÄ±ÅŸa aktar';

  @override
  String get logoutSuccessTitle => 'BaÅŸarÄ±lÄ±';

  @override
  String get logoutSuccessMessage => 'Ã‡Ä±kÄ±ÅŸ yapÄ±ldÄ±';

  @override
  String get logoutErrorTitle => 'Hata';

  @override
  String get copiedToClipboard => 'Panoya kopyalandÄ±';

  @override
  String yesterdayAt(String time) {
    return 'DÃ¼n $time';
  }

  @override
  String get aiThinking => 'Yapay zeka dÃ¼ÅŸÃ¼nÃ¼yor...';

  @override
  String get infoTitle => 'Bilgi';

  @override
  String get successTitle => 'BaÅŸarÄ±lÄ±';

  @override
  String get errorTitle => 'Hata';

  @override
  String get imagePickerErrorTitle => 'Hata';

  @override
  String imagePickerErrorMessage(String error) {
    return 'GÃ¶rsel seÃ§ilemedi: $error';
  }

  @override
  String get chooseImageSourceTitle => 'GÃ¶rsel kaynaÄŸÄ±nÄ± seÃ§in';

  @override
  String get cameraLabel => 'Kamera';

  @override
  String get galleryLabel => 'Galeri';

  @override
  String get appwritePingSuccess => 'Appwrite baÄŸlantÄ±sÄ± baÅŸarÄ±lÄ±!';

  @override
  String get appwritePingNoSession =>
      'Appwrite baÄŸlantÄ±sÄ± var ama oturum aÃ§Ä±k deÄŸil.';

  @override
  String appwritePingError(String error) {
    return 'Appwrite ping hatasÄ±: $error';
  }

  @override
  String get sendPingTooltip => 'Ping gÃ¶nder';

  @override
  String get logoutTooltip => 'Ã‡Ä±kÄ±ÅŸ';

  @override
  String get assistantTitle => 'Yapay zeka asistanÄ±';

  @override
  String get assistantHint =>
      'Bir mesaj yazÄ±n veya sesli giriÅŸ iÃ§in basÄ±lÄ± tutun...';

  @override
  String get listeningStatus => 'Ses giriÅŸi dinleniyor...';

  @override
  String get startChatHint => 'Yapay zeka asistanÄ±yla konuÅŸmaya baÅŸlayÄ±n!';

  @override
  String get errorInvalidRequest => 'Hata: GeÃ§ersiz istek';

  @override
  String get errorInvalidRequestFormat => 'Hata: GeÃ§ersiz istek formatÄ±.';

  @override
  String get errorServiceUnavailable =>
      'Hata: Yapay zeka hizmeti kullanÄ±lamÄ±yor.';

  @override
  String get errorTimeout => 'Hata: YanÄ±t zaman aÅŸÄ±mÄ±na uÄŸradÄ±.';

  @override
  String get errorBackendUnavailable =>
      'Hata: Sunucu hizmeti kullanÄ±lamÄ±yor.';

  @override
  String get errorNoInternet => 'Hata: Ä°nternet baÄŸlantÄ±sÄ± yok.';

  @override
  String get errorInvalidServerResponse => 'Hata: GeÃ§ersiz sunucu yanÄ±tÄ±.';

  @override
  String get errorUnexpected => 'Hata: Beklenmeyen hata.';

  @override
  String get noResponseGenerated => 'ÃœzgÃ¼nÃ¼m, yanÄ±t Ã¼retilemedi.';

  @override
  String get requestTimeoutMessage =>
      'Ä°stek zaman aÅŸÄ±mÄ±na uÄŸradÄ±. LÃ¼tfen tekrar deneyin.';

  @override
  String get speechRecognitionFailed =>
      'Ses tanÄ±ma baÅŸarÄ±sÄ±z oldu. LÃ¼tfen tekrar deneyin.';

  @override
  String get speechRecognitionError =>
      'Ses tanÄ±ma hatasÄ±. LÃ¼tfen aÄŸ baÄŸlantÄ±nÄ±zÄ± kontrol edin.';

  @override
  String get serverConnectionFailed => 'Sunucu baÄŸlantÄ±sÄ± baÅŸarÄ±sÄ±z.';
}
