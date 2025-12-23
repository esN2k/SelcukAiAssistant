// ignore: unused_import
import 'package:intl/intl.dart' as intl;
import 'app_localizations.dart';

// ignore_for_file: type=lint

/// The translations for English (`en`).
class AppLocalizationsEn extends AppLocalizations {
  AppLocalizationsEn([String locale = 'en']) : super(locale);

  @override
  String get appTitle => 'Selcuk AI Assistant';

  @override
  String get appSubtitle => 'Selcuk AI Assistant';

  @override
  String get splashSubtitle => 'Selcuk AI Assistant';

  @override
  String get ok => 'OK';

  @override
  String get cancel => 'Cancel';

  @override
  String get delete => 'Delete';

  @override
  String get clear => 'Clear';

  @override
  String get rename => 'Rename';

  @override
  String get newChat => 'New chat';

  @override
  String get loginTitle => 'Welcome back';

  @override
  String get loginSubtitle => 'Sign in to continue';

  @override
  String get loginButton => 'Sign in';

  @override
  String get loginNoAccount => 'Don\'t have an account?';

  @override
  String get loginCreateAccount => 'Create account';

  @override
  String get loginSuccessTitle => 'Success';

  @override
  String get loginSuccessMessage => 'Signed in successfully!';

  @override
  String get loginErrorTitle => 'Error';

  @override
  String get registerTitle => 'Create account';

  @override
  String get registerSubtitle => 'Start using the assistant';

  @override
  String get registerButton => 'Create account';

  @override
  String get registerHaveAccount => 'Already have an account?';

  @override
  String get registerSignIn => 'Sign in';

  @override
  String get registerSuccessTitle => 'Success';

  @override
  String get registerSuccessMessage => 'Registration complete. Welcome!';

  @override
  String get registerErrorTitle => 'Error';

  @override
  String get nameLabel => 'Full name';

  @override
  String get emailLabel => 'Email';

  @override
  String get passwordLabel => 'Password';

  @override
  String get confirmPasswordLabel => 'Confirm password';

  @override
  String get nameRequired => 'Full name is required';

  @override
  String get emailRequired => 'Email is required';

  @override
  String get invalidEmail => 'Enter a valid email';

  @override
  String get passwordRequired => 'Password is required';

  @override
  String get passwordMinLength => 'Password must be at least 8 characters';

  @override
  String get confirmPasswordRequired => 'Please confirm your password';

  @override
  String get passwordsDoNotMatch => 'Passwords do not match';

  @override
  String get onboardingTitle1 => 'Ask me anything';

  @override
  String get onboardingSubtitle1 =>
      'I can be your best companion. Ask me anything and I will help!';

  @override
  String get onboardingTitle2 => 'From imagination to reality';

  @override
  String get onboardingSubtitle2 =>
      'Just imagine and tell me. I will create something great for you!';

  @override
  String get onboardingNext => 'Next';

  @override
  String get onboardingDone => 'Done';

  @override
  String get settingsTitle => 'Settings';

  @override
  String get sectionAppearance => 'APPEARANCE';

  @override
  String get sectionLanguage => 'LANGUAGE';

  @override
  String get sectionAiModel => 'AI MODEL';

  @override
  String get sectionChatSettings => 'CHAT SETTINGS';

  @override
  String get sectionServer => 'SERVER';

  @override
  String get sectionDiagnostics => 'DIAGNOSTICS';

  @override
  String get sectionStatistics => 'STATISTICS';

  @override
  String get sectionDataManagement => 'DATA MANAGEMENT';

  @override
  String get sectionAbout => 'ABOUT';

  @override
  String get darkModeTitle => 'Dark mode';

  @override
  String get darkModeSubtitle => 'Toggle between light and dark theme';

  @override
  String get languageTitle => 'App language';

  @override
  String get languageSubtitle => 'Choose your preferred language';

  @override
  String get languageTurkish => 'Turkish';

  @override
  String get languageEnglish => 'English';

  @override
  String get modelLabel => 'Model';

  @override
  String get modelNotSelected => 'Not selected';

  @override
  String get modelAvailable => 'Available';

  @override
  String get modelUnavailable => 'Unavailable';

  @override
  String get modelLocalSection => 'Local models';

  @override
  String get modelRemoteSection => 'Remote / API models';

  @override
  String modelInstallCommand(String command) {
    return 'Install: $command';
  }

  @override
  String modelUnavailableReason(String reason) {
    return 'Reason: $reason';
  }

  @override
  String get modelSearchHint => 'Search models...';

  @override
  String get modelNoResults => 'No models found';

  @override
  String get modelApiKeyRequired => 'API key required';

  @override
  String get modelNotInstalled => 'Not installed';

  @override
  String modelContextLength(int count) {
    return 'Context: $count tokens';
  }

  @override
  String get backendUrlTitle => 'Backend URL';

  @override
  String backendUrlSubtitle(String current) {
    return 'Current: $current';
  }

  @override
  String get backendUrlHint => 'https://example.com:8000 or /api';

  @override
  String get backendUrlSave => 'Save';

  @override
  String get backendUrlClear => 'Clear override';

  @override
  String get backendUrlSaved => 'Backend URL saved';

  @override
  String get backendUrlCleared => 'Backend URL override cleared';

  @override
  String get diagnosticsTitle => 'Diagnostics';

  @override
  String get diagnosticsSubtitle => 'Test backend connectivity and streaming';

  @override
  String get selectModelTitle => 'Select model';

  @override
  String get voiceInputTitle => 'Voice input';

  @override
  String get voiceInputSubtitle => 'Enable microphone for voice messages';

  @override
  String get markdownSupportTitle => 'Markdown support';

  @override
  String get markdownSupportSubtitle => 'Render formatted text and code';

  @override
  String get totalConversations => 'Total conversations';

  @override
  String get totalMessages => 'Total messages';

  @override
  String get clearAllConversationsTitle => 'Clear all conversations';

  @override
  String get clearAllConversationsSubtitle => 'Delete all chat history';

  @override
  String get clearAllDataTitle => 'Clear all data';

  @override
  String get clearAllDataMessage =>
      'Are you sure you want to delete all conversations? This action cannot be undone.';

  @override
  String get deleteAll => 'Delete all';

  @override
  String get clearAllSuccessTitle => 'Success';

  @override
  String get clearAllSuccessMessage => 'All conversations deleted';

  @override
  String get versionLabel => 'Version';

  @override
  String get developerLabel => 'Developer';

  @override
  String get developerValue => 'Selçuk AI';

  @override
  String get deleteConversationTitle => 'Delete conversation';

  @override
  String get deleteConversationMessage =>
      'Are you sure you want to delete this conversation? This action cannot be undone.';

  @override
  String get renameConversationTitle => 'Rename conversation';

  @override
  String get renameConversationHint => 'Enter new title';

  @override
  String get searchConversationsHint => 'Search conversations...';

  @override
  String get noConversationsFound => 'No conversations found';

  @override
  String get noConversationsYet => 'No conversations yet';

  @override
  String conversationsCount(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count conversations',
      one: '1 conversation',
      zero: '0 conversations',
    );
    return '$_temp0';
  }

  @override
  String get pinnedLabel => 'Pinned';

  @override
  String get archivedLabel => 'Archived';

  @override
  String get last7DaysLabel => 'Last 7 days';

  @override
  String get olderLabel => 'Older';

  @override
  String get pinConversation => 'Pin';

  @override
  String get unpinConversation => 'Unpin';

  @override
  String get archiveConversation => 'Archive';

  @override
  String get unarchiveConversation => 'Unarchive';

  @override
  String get todayLabel => 'Today';

  @override
  String get yesterdayLabel => 'Yesterday';

  @override
  String daysAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count days ago',
      one: '1 day ago',
    );
    return '$_temp0';
  }

  @override
  String weeksAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count weeks ago',
      one: '1 week ago',
    );
    return '$_temp0';
  }

  @override
  String monthsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count months ago',
      one: '1 month ago',
    );
    return '$_temp0';
  }

  @override
  String yearsAgo(int count) {
    String _temp0 = intl.Intl.pluralLogic(
      count,
      locale: localeName,
      other: '$count years ago',
      one: '1 year ago',
    );
    return '$_temp0';
  }

  @override
  String get clearConversationTitle => 'Clear conversation';

  @override
  String get clearConversationMessage =>
      'Are you sure you want to clear this conversation? This action cannot be undone.';

  @override
  String get listeningIndicator => 'Listening... (release to stop)';

  @override
  String get messageHint => 'Message Selcuk AI Assistant...';

  @override
  String get imageSelectedTitle => 'Image selected';

  @override
  String imageSelectedMessage(String fileName) {
    return 'Image: $fileName';
  }

  @override
  String get startConversationTitle => 'Start a conversation';

  @override
  String get startConversationSubtitle => 'Ask me anything!';

  @override
  String get suggestedPrompt1 => 'Explain quantum computing';

  @override
  String get suggestedPrompt2 => 'Write a poem';

  @override
  String get suggestedPrompt3 => 'Help with code';

  @override
  String get streamErrorTitle => 'Stream error';

  @override
  String streamErrorMessage(String error) {
    return '$error';
  }

  @override
  String get streamInterruptedTag => '[Stream interrupted]';

  @override
  String get copyAction => 'Copy';

  @override
  String get editMessageTitle => 'Edit message';

  @override
  String get editMessageHint => 'Update your message';

  @override
  String get editMessageAction => 'Resend';

  @override
  String get regenerateAction => 'Regenerate';

  @override
  String get retryAction => 'Retry';

  @override
  String get diagnosticsConnectionSection => 'CONNECTION';

  @override
  String get diagnosticsBaseUrlLabel => 'Base URL';

  @override
  String diagnosticsBaseUrlSource(String source) {
    return 'Source: $source';
  }

  @override
  String get diagnosticsPlatformLabel => 'Platform';

  @override
  String get diagnosticsLatencyLabel => 'Latency';

  @override
  String get diagnosticsLatencyUnavailable => 'No latency recorded yet.';

  @override
  String get diagnosticsModelLabel => 'Selected model';

  @override
  String get diagnosticsModelAvailable => 'Available';

  @override
  String get diagnosticsModelUnavailable => 'Unavailable';

  @override
  String get diagnosticsOllamaLabel => 'Ollama health';

  @override
  String get diagnosticsOllamaReady => 'Ready';

  @override
  String get diagnosticsOllamaUnavailable => 'Unavailable';

  @override
  String get diagnosticsOllamaButton => 'Test /health/ollama';

  @override
  String diagnosticsOllamaDetail(
      String status, String model, String availability, String count) {
    return 'Status: $status | Model: $model | $availability | Models: $count';
  }

  @override
  String get diagnosticsHfLabel => 'HF GPU Ready';

  @override
  String get diagnosticsHfReady => 'Ready';

  @override
  String get diagnosticsHfUnavailable => 'Unavailable';

  @override
  String get diagnosticsHfButton => 'Test /health/hf';

  @override
  String diagnosticsHfDetail(
      String gpu, String torch, String cuda, String transformers, String bnb) {
    return 'GPU: $gpu | Torch: $torch | CUDA: $cuda | Transformers: $transformers | bitsandbytes: $bnb';
  }

  @override
  String get diagnosticsHealthButton => 'Test /health';

  @override
  String get diagnosticsModelsButton => 'Test /models';

  @override
  String get diagnosticsSourceOverride => 'User override';

  @override
  String get diagnosticsSourceDartDefine => 'Dart define';

  @override
  String get diagnosticsSourceDotenv => 'Dotenv';

  @override
  String get diagnosticsSourceWebRelease => 'Web release (/api)';

  @override
  String get diagnosticsSourceWebDev => 'Web dev (localhost)';

  @override
  String get diagnosticsSourceAndroidEmulator => 'Android emulator (10.0.2.2)';

  @override
  String get diagnosticsSourceDesktop => 'Desktop (localhost)';

  @override
  String get diagnosticsChatButton => 'Test /chat';

  @override
  String get diagnosticsStreamButton => 'Test /chat/stream';

  @override
  String get diagnosticsStreamRunning => 'Streaming...';

  @override
  String get diagnosticsLastErrorTitle => 'Last error';

  @override
  String get diagnosticsErrorStatusLabel => 'Status';

  @override
  String get diagnosticsErrorBodyLabel => 'Body';

  @override
  String get diagnosticsErrorHeadersLabel => 'Headers';

  @override
  String get diagnosticsNoErrors => 'No errors recorded yet.';

  @override
  String get diagnosticsStreamSampleTitle => 'SSE sample';

  @override
  String get diagnosticsNoStreamSample => 'No stream events captured.';

  @override
  String get diagnosticsLogsTitle => 'Diagnostics log';

  @override
  String get diagnosticsCopyLog => 'Copy log';

  @override
  String get diagnosticsNoLogs => 'No diagnostics run yet.';

  @override
  String get diagnosticsTestMessage => 'Hello';

  @override
  String get microphonePermissionRequired =>
      'Microphone permission is required for voice input';

  @override
  String get speechNotAvailable => 'Speech recognition is not available';

  @override
  String get enterMessagePrompt => 'Please enter a message or use voice input!';

  @override
  String get exportFailedTitle => 'Export failed';

  @override
  String get noMessagesToExport => 'No messages to export';

  @override
  String get exportSuccessTitle => 'Export successful';

  @override
  String exportSuccessMessage(String path) {
    return 'Saved to $path\\nAlso copied to clipboard';
  }

  @override
  String get exportSuccessWebMessage =>
      'Downloaded file and copied to clipboard';

  @override
  String get logout => 'Logout';

  @override
  String get clearChat => 'Clear chat';

  @override
  String get exportChat => 'Export chat';

  @override
  String get logoutSuccessTitle => 'Success';

  @override
  String get logoutSuccessMessage => 'Logged out successfully';

  @override
  String get logoutErrorTitle => 'Error';

  @override
  String get copiedToClipboard => 'Copied to clipboard';

  @override
  String yesterdayAt(String time) {
    return 'Yesterday $time';
  }

  @override
  String get aiThinking => 'AI is thinking...';

  @override
  String get infoTitle => 'Info';

  @override
  String get successTitle => 'Success';

  @override
  String get errorTitle => 'Error';

  @override
  String get imagePickerErrorTitle => 'Error';

  @override
  String imagePickerErrorMessage(String error) {
    return 'Failed to pick image: $error';
  }

  @override
  String get chooseImageSourceTitle => 'Choose image source';

  @override
  String get cameraLabel => 'Camera';

  @override
  String get galleryLabel => 'Gallery';

  @override
  String get appwritePingSuccess => 'Appwrite connection is successful!';

  @override
  String get appwritePingNoSession =>
      'Appwrite connection is OK but no session is active.';

  @override
  String appwritePingError(String error) {
    return 'Appwrite ping error: $error';
  }

  @override
  String get sendPingTooltip => 'Send a ping';

  @override
  String get logoutTooltip => 'Logout';

  @override
  String get assistantTitle => 'AI assistant';

  @override
  String get assistantHint => 'Type a message or hold for voice input...';

  @override
  String get listeningStatus => 'Listening to voice input...';

  @override
  String get startChatHint => 'Start chatting with the AI assistant!';

  @override
  String get errorInvalidRequest => 'Error: Invalid request';

  @override
  String get errorInvalidRequestFormat => 'Error: Invalid request format.';

  @override
  String get errorServiceUnavailable => 'Error: AI service is unavailable.';

  @override
  String get errorTimeout => 'Error: AI response timeout.';

  @override
  String get errorBackendUnavailable => 'Error: Backend service unavailable.';

  @override
  String get errorNoInternet => 'Error: No internet connection.';

  @override
  String get errorInvalidServerResponse => 'Error: Invalid server response.';

  @override
  String get errorUnexpected => 'Error: Unexpected error.';

  @override
  String get noResponseGenerated => 'Sorry, no response generated.';

  @override
  String get requestTimeoutMessage => 'Request timed out. Please try again.';

  @override
  String get speechRecognitionFailed =>
      'Speech recognition failed. Please try again.';

  @override
  String get speechRecognitionError =>
      'Speech recognition error. Please check your network.';

  @override
  String get serverConnectionFailed => 'Server connection failed.';
}
