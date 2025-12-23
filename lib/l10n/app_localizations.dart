import 'dart:async';

import 'package:flutter/foundation.dart';
import 'package:flutter/widgets.dart';
import 'package:flutter_localizations/flutter_localizations.dart';
import 'package:intl/intl.dart' as intl;

import 'app_localizations_en.dart';
import 'app_localizations_tr.dart';

// ignore_for_file: type=lint

/// Callers can lookup localized strings with an instance of AppLocalizations
/// returned by `AppLocalizations.of(context)`.
///
/// Applications need to include `AppLocalizations.delegate()` in their app's
/// `localizationDelegates` list, and the locales they support in the app's
/// `supportedLocales` list. For example:
///
/// ```dart
/// import 'l10n/app_localizations.dart';
///
/// return MaterialApp(
///   localizationsDelegates: AppLocalizations.localizationsDelegates,
///   supportedLocales: AppLocalizations.supportedLocales,
///   home: MyApplicationHome(),
/// );
/// ```
///
/// ## Update pubspec.yaml
///
/// Please make sure to update your pubspec.yaml to include the following
/// packages:
///
/// ```yaml
/// dependencies:
///   # Internationalization support.
///   flutter_localizations:
///     sdk: flutter
///   intl: any # Use the pinned version from flutter_localizations
///
///   # Rest of dependencies
/// ```
///
/// ## iOS Applications
///
/// iOS applications define key application metadata, including supported
/// locales, in an Info.plist file that is built into the application bundle.
/// To configure the locales supported by your app, you’ll need to edit this
/// file.
///
/// First, open your project’s ios/Runner.xcworkspace Xcode workspace file.
/// Then, in the Project Navigator, open the Info.plist file under the Runner
/// project’s Runner folder.
///
/// Next, select the Information Property List item, select Add Item from the
/// Editor menu, then select Localizations from the pop-up menu.
///
/// Select and expand the newly-created Localizations item then, for each
/// locale your application supports, add a new item and select the locale
/// you wish to add from the pop-up menu in the Value field. This list should
/// be consistent with the languages listed in the AppLocalizations.supportedLocales
/// property.
abstract class AppLocalizations {
  AppLocalizations(String locale)
      : localeName = intl.Intl.canonicalizedLocale(locale.toString());

  final String localeName;

  static AppLocalizations of(BuildContext context) {
    return Localizations.of<AppLocalizations>(context, AppLocalizations)!;
  }

  static const LocalizationsDelegate<AppLocalizations> delegate =
      _AppLocalizationsDelegate();

  /// A list of this localizations delegate along with the default localizations
  /// delegates.
  ///
  /// Returns a list of localizations delegates containing this delegate along with
  /// GlobalMaterialLocalizations.delegate, GlobalCupertinoLocalizations.delegate,
  /// and GlobalWidgetsLocalizations.delegate.
  ///
  /// Additional delegates can be added by appending to this list in
  /// MaterialApp. This list does not have to be used at all if a custom list
  /// of delegates is preferred or required.
  static const List<LocalizationsDelegate<dynamic>> localizationsDelegates =
      <LocalizationsDelegate<dynamic>>[
    delegate,
    GlobalMaterialLocalizations.delegate,
    GlobalCupertinoLocalizations.delegate,
    GlobalWidgetsLocalizations.delegate,
  ];

  /// A list of this localizations delegate's supported locales.
  static const List<Locale> supportedLocales = <Locale>[
    Locale('en'),
    Locale('tr')
  ];

  /// No description provided for @appTitle.
  ///
  /// In en, this message translates to:
  /// **'Selcuk AI Assistant'**
  String get appTitle;

  /// No description provided for @appSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Selcuk AI Assistant'**
  String get appSubtitle;

  /// No description provided for @splashSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Selcuk AI Assistant'**
  String get splashSubtitle;

  /// No description provided for @ok.
  ///
  /// In en, this message translates to:
  /// **'OK'**
  String get ok;

  /// No description provided for @cancel.
  ///
  /// In en, this message translates to:
  /// **'Cancel'**
  String get cancel;

  /// No description provided for @delete.
  ///
  /// In en, this message translates to:
  /// **'Delete'**
  String get delete;

  /// No description provided for @clear.
  ///
  /// In en, this message translates to:
  /// **'Clear'**
  String get clear;

  /// No description provided for @rename.
  ///
  /// In en, this message translates to:
  /// **'Rename'**
  String get rename;

  /// No description provided for @newChat.
  ///
  /// In en, this message translates to:
  /// **'New chat'**
  String get newChat;

  /// No description provided for @loginTitle.
  ///
  /// In en, this message translates to:
  /// **'Welcome back'**
  String get loginTitle;

  /// No description provided for @loginSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Sign in to continue'**
  String get loginSubtitle;

  /// No description provided for @loginButton.
  ///
  /// In en, this message translates to:
  /// **'Sign in'**
  String get loginButton;

  /// No description provided for @loginNoAccount.
  ///
  /// In en, this message translates to:
  /// **'Don\'t have an account?'**
  String get loginNoAccount;

  /// No description provided for @loginCreateAccount.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get loginCreateAccount;

  /// No description provided for @loginSuccessTitle.
  ///
  /// In en, this message translates to:
  /// **'Success'**
  String get loginSuccessTitle;

  /// No description provided for @loginSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'Signed in successfully!'**
  String get loginSuccessMessage;

  /// No description provided for @loginErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get loginErrorTitle;

  /// No description provided for @registerTitle.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get registerTitle;

  /// No description provided for @registerSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Start using the assistant'**
  String get registerSubtitle;

  /// No description provided for @registerButton.
  ///
  /// In en, this message translates to:
  /// **'Create account'**
  String get registerButton;

  /// No description provided for @registerHaveAccount.
  ///
  /// In en, this message translates to:
  /// **'Already have an account?'**
  String get registerHaveAccount;

  /// No description provided for @registerSignIn.
  ///
  /// In en, this message translates to:
  /// **'Sign in'**
  String get registerSignIn;

  /// No description provided for @registerSuccessTitle.
  ///
  /// In en, this message translates to:
  /// **'Success'**
  String get registerSuccessTitle;

  /// No description provided for @registerSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'Registration complete. Welcome!'**
  String get registerSuccessMessage;

  /// No description provided for @registerErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get registerErrorTitle;

  /// No description provided for @nameLabel.
  ///
  /// In en, this message translates to:
  /// **'Full name'**
  String get nameLabel;

  /// No description provided for @emailLabel.
  ///
  /// In en, this message translates to:
  /// **'Email'**
  String get emailLabel;

  /// No description provided for @passwordLabel.
  ///
  /// In en, this message translates to:
  /// **'Password'**
  String get passwordLabel;

  /// No description provided for @confirmPasswordLabel.
  ///
  /// In en, this message translates to:
  /// **'Confirm password'**
  String get confirmPasswordLabel;

  /// No description provided for @nameRequired.
  ///
  /// In en, this message translates to:
  /// **'Full name is required'**
  String get nameRequired;

  /// No description provided for @emailRequired.
  ///
  /// In en, this message translates to:
  /// **'Email is required'**
  String get emailRequired;

  /// No description provided for @invalidEmail.
  ///
  /// In en, this message translates to:
  /// **'Enter a valid email'**
  String get invalidEmail;

  /// No description provided for @passwordRequired.
  ///
  /// In en, this message translates to:
  /// **'Password is required'**
  String get passwordRequired;

  /// No description provided for @passwordMinLength.
  ///
  /// In en, this message translates to:
  /// **'Password must be at least 8 characters'**
  String get passwordMinLength;

  /// No description provided for @confirmPasswordRequired.
  ///
  /// In en, this message translates to:
  /// **'Please confirm your password'**
  String get confirmPasswordRequired;

  /// No description provided for @passwordsDoNotMatch.
  ///
  /// In en, this message translates to:
  /// **'Passwords do not match'**
  String get passwordsDoNotMatch;

  /// No description provided for @onboardingTitle1.
  ///
  /// In en, this message translates to:
  /// **'Ask me anything'**
  String get onboardingTitle1;

  /// No description provided for @onboardingSubtitle1.
  ///
  /// In en, this message translates to:
  /// **'I can be your best companion. Ask me anything and I will help!'**
  String get onboardingSubtitle1;

  /// No description provided for @onboardingTitle2.
  ///
  /// In en, this message translates to:
  /// **'From imagination to reality'**
  String get onboardingTitle2;

  /// No description provided for @onboardingSubtitle2.
  ///
  /// In en, this message translates to:
  /// **'Just imagine and tell me. I will create something great for you!'**
  String get onboardingSubtitle2;

  /// No description provided for @onboardingNext.
  ///
  /// In en, this message translates to:
  /// **'Next'**
  String get onboardingNext;

  /// No description provided for @onboardingDone.
  ///
  /// In en, this message translates to:
  /// **'Done'**
  String get onboardingDone;

  /// No description provided for @settingsTitle.
  ///
  /// In en, this message translates to:
  /// **'Settings'**
  String get settingsTitle;

  /// No description provided for @sectionAppearance.
  ///
  /// In en, this message translates to:
  /// **'APPEARANCE'**
  String get sectionAppearance;

  /// No description provided for @sectionLanguage.
  ///
  /// In en, this message translates to:
  /// **'LANGUAGE'**
  String get sectionLanguage;

  /// No description provided for @sectionAiModel.
  ///
  /// In en, this message translates to:
  /// **'AI MODEL'**
  String get sectionAiModel;

  /// No description provided for @sectionChatSettings.
  ///
  /// In en, this message translates to:
  /// **'CHAT SETTINGS'**
  String get sectionChatSettings;

  /// No description provided for @sectionServer.
  ///
  /// In en, this message translates to:
  /// **'SERVER'**
  String get sectionServer;

  /// No description provided for @sectionDiagnostics.
  ///
  /// In en, this message translates to:
  /// **'DIAGNOSTICS'**
  String get sectionDiagnostics;

  /// No description provided for @sectionStatistics.
  ///
  /// In en, this message translates to:
  /// **'STATISTICS'**
  String get sectionStatistics;

  /// No description provided for @sectionDataManagement.
  ///
  /// In en, this message translates to:
  /// **'DATA MANAGEMENT'**
  String get sectionDataManagement;

  /// No description provided for @sectionAbout.
  ///
  /// In en, this message translates to:
  /// **'ABOUT'**
  String get sectionAbout;

  /// No description provided for @darkModeTitle.
  ///
  /// In en, this message translates to:
  /// **'Dark mode'**
  String get darkModeTitle;

  /// No description provided for @darkModeSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Toggle between light and dark theme'**
  String get darkModeSubtitle;

  /// No description provided for @languageTitle.
  ///
  /// In en, this message translates to:
  /// **'App language'**
  String get languageTitle;

  /// No description provided for @languageSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Choose your preferred language'**
  String get languageSubtitle;

  /// No description provided for @languageTurkish.
  ///
  /// In en, this message translates to:
  /// **'Turkish'**
  String get languageTurkish;

  /// No description provided for @languageEnglish.
  ///
  /// In en, this message translates to:
  /// **'English'**
  String get languageEnglish;

  /// No description provided for @modelLabel.
  ///
  /// In en, this message translates to:
  /// **'Model'**
  String get modelLabel;

  /// No description provided for @modelNotSelected.
  ///
  /// In en, this message translates to:
  /// **'Not selected'**
  String get modelNotSelected;

  /// No description provided for @modelAvailable.
  ///
  /// In en, this message translates to:
  /// **'Available'**
  String get modelAvailable;

  /// No description provided for @modelUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Unavailable'**
  String get modelUnavailable;

  /// No description provided for @modelLocalSection.
  ///
  /// In en, this message translates to:
  /// **'Local models'**
  String get modelLocalSection;

  /// No description provided for @modelRemoteSection.
  ///
  /// In en, this message translates to:
  /// **'Remote / API models'**
  String get modelRemoteSection;

  /// No description provided for @modelInstallCommand.
  ///
  /// In en, this message translates to:
  /// **'Install: {command}'**
  String modelInstallCommand(String command);

  /// No description provided for @modelUnavailableReason.
  ///
  /// In en, this message translates to:
  /// **'Reason: {reason}'**
  String modelUnavailableReason(String reason);

  /// No description provided for @backendUrlTitle.
  ///
  /// In en, this message translates to:
  /// **'Backend URL'**
  String get backendUrlTitle;

  /// No description provided for @backendUrlSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Current: {current}'**
  String backendUrlSubtitle(String current);

  /// No description provided for @backendUrlHint.
  ///
  /// In en, this message translates to:
  /// **'https://example.com:8000 or /api'**
  String get backendUrlHint;

  /// No description provided for @backendUrlSave.
  ///
  /// In en, this message translates to:
  /// **'Save'**
  String get backendUrlSave;

  /// No description provided for @backendUrlClear.
  ///
  /// In en, this message translates to:
  /// **'Clear override'**
  String get backendUrlClear;

  /// No description provided for @backendUrlSaved.
  ///
  /// In en, this message translates to:
  /// **'Backend URL saved'**
  String get backendUrlSaved;

  /// No description provided for @backendUrlCleared.
  ///
  /// In en, this message translates to:
  /// **'Backend URL override cleared'**
  String get backendUrlCleared;

  /// No description provided for @diagnosticsTitle.
  ///
  /// In en, this message translates to:
  /// **'Diagnostics'**
  String get diagnosticsTitle;

  /// No description provided for @diagnosticsSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Test backend connectivity and streaming'**
  String get diagnosticsSubtitle;

  /// No description provided for @selectModelTitle.
  ///
  /// In en, this message translates to:
  /// **'Select model'**
  String get selectModelTitle;

  /// No description provided for @voiceInputTitle.
  ///
  /// In en, this message translates to:
  /// **'Voice input'**
  String get voiceInputTitle;

  /// No description provided for @voiceInputSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Enable microphone for voice messages'**
  String get voiceInputSubtitle;

  /// No description provided for @markdownSupportTitle.
  ///
  /// In en, this message translates to:
  /// **'Markdown support'**
  String get markdownSupportTitle;

  /// No description provided for @markdownSupportSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Render formatted text and code'**
  String get markdownSupportSubtitle;

  /// No description provided for @totalConversations.
  ///
  /// In en, this message translates to:
  /// **'Total conversations'**
  String get totalConversations;

  /// No description provided for @totalMessages.
  ///
  /// In en, this message translates to:
  /// **'Total messages'**
  String get totalMessages;

  /// No description provided for @clearAllConversationsTitle.
  ///
  /// In en, this message translates to:
  /// **'Clear all conversations'**
  String get clearAllConversationsTitle;

  /// No description provided for @clearAllConversationsSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Delete all chat history'**
  String get clearAllConversationsSubtitle;

  /// No description provided for @clearAllDataTitle.
  ///
  /// In en, this message translates to:
  /// **'Clear all data'**
  String get clearAllDataTitle;

  /// No description provided for @clearAllDataMessage.
  ///
  /// In en, this message translates to:
  /// **'Are you sure you want to delete all conversations? This action cannot be undone.'**
  String get clearAllDataMessage;

  /// No description provided for @deleteAll.
  ///
  /// In en, this message translates to:
  /// **'Delete all'**
  String get deleteAll;

  /// No description provided for @clearAllSuccessTitle.
  ///
  /// In en, this message translates to:
  /// **'Success'**
  String get clearAllSuccessTitle;

  /// No description provided for @clearAllSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'All conversations deleted'**
  String get clearAllSuccessMessage;

  /// No description provided for @versionLabel.
  ///
  /// In en, this message translates to:
  /// **'Version'**
  String get versionLabel;

  /// No description provided for @developerLabel.
  ///
  /// In en, this message translates to:
  /// **'Developer'**
  String get developerLabel;

  /// No description provided for @developerValue.
  ///
  /// In en, this message translates to:
  /// **'Selçuk AI'**
  String get developerValue;

  /// No description provided for @deleteConversationTitle.
  ///
  /// In en, this message translates to:
  /// **'Delete conversation'**
  String get deleteConversationTitle;

  /// No description provided for @deleteConversationMessage.
  ///
  /// In en, this message translates to:
  /// **'Are you sure you want to delete this conversation? This action cannot be undone.'**
  String get deleteConversationMessage;

  /// No description provided for @renameConversationTitle.
  ///
  /// In en, this message translates to:
  /// **'Rename conversation'**
  String get renameConversationTitle;

  /// No description provided for @renameConversationHint.
  ///
  /// In en, this message translates to:
  /// **'Enter new title'**
  String get renameConversationHint;

  /// No description provided for @searchConversationsHint.
  ///
  /// In en, this message translates to:
  /// **'Search conversations...'**
  String get searchConversationsHint;

  /// No description provided for @noConversationsFound.
  ///
  /// In en, this message translates to:
  /// **'No conversations found'**
  String get noConversationsFound;

  /// No description provided for @noConversationsYet.
  ///
  /// In en, this message translates to:
  /// **'No conversations yet'**
  String get noConversationsYet;

  /// No description provided for @conversationsCount.
  ///
  /// In en, this message translates to:
  /// **'{count, plural, =0{0 conversations} =1{1 conversation} other{{count} conversations}}'**
  String conversationsCount(int count);

  /// No description provided for @pinnedLabel.
  ///
  /// In en, this message translates to:
  /// **'Pinned'**
  String get pinnedLabel;

  /// No description provided for @archivedLabel.
  ///
  /// In en, this message translates to:
  /// **'Archived'**
  String get archivedLabel;

  /// No description provided for @last7DaysLabel.
  ///
  /// In en, this message translates to:
  /// **'Last 7 days'**
  String get last7DaysLabel;

  /// No description provided for @olderLabel.
  ///
  /// In en, this message translates to:
  /// **'Older'**
  String get olderLabel;

  /// No description provided for @pinConversation.
  ///
  /// In en, this message translates to:
  /// **'Pin'**
  String get pinConversation;

  /// No description provided for @unpinConversation.
  ///
  /// In en, this message translates to:
  /// **'Unpin'**
  String get unpinConversation;

  /// No description provided for @archiveConversation.
  ///
  /// In en, this message translates to:
  /// **'Archive'**
  String get archiveConversation;

  /// No description provided for @unarchiveConversation.
  ///
  /// In en, this message translates to:
  /// **'Unarchive'**
  String get unarchiveConversation;

  /// No description provided for @todayLabel.
  ///
  /// In en, this message translates to:
  /// **'Today'**
  String get todayLabel;

  /// No description provided for @yesterdayLabel.
  ///
  /// In en, this message translates to:
  /// **'Yesterday'**
  String get yesterdayLabel;

  /// No description provided for @daysAgo.
  ///
  /// In en, this message translates to:
  /// **'{count, plural, =1{1 day ago} other{{count} days ago}}'**
  String daysAgo(int count);

  /// No description provided for @weeksAgo.
  ///
  /// In en, this message translates to:
  /// **'{count, plural, =1{1 week ago} other{{count} weeks ago}}'**
  String weeksAgo(int count);

  /// No description provided for @monthsAgo.
  ///
  /// In en, this message translates to:
  /// **'{count, plural, =1{1 month ago} other{{count} months ago}}'**
  String monthsAgo(int count);

  /// No description provided for @yearsAgo.
  ///
  /// In en, this message translates to:
  /// **'{count, plural, =1{1 year ago} other{{count} years ago}}'**
  String yearsAgo(int count);

  /// No description provided for @clearConversationTitle.
  ///
  /// In en, this message translates to:
  /// **'Clear conversation'**
  String get clearConversationTitle;

  /// No description provided for @clearConversationMessage.
  ///
  /// In en, this message translates to:
  /// **'Are you sure you want to clear this conversation? This action cannot be undone.'**
  String get clearConversationMessage;

  /// No description provided for @listeningIndicator.
  ///
  /// In en, this message translates to:
  /// **'Listening... (release to stop)'**
  String get listeningIndicator;

  /// No description provided for @messageHint.
  ///
  /// In en, this message translates to:
  /// **'Message Selcuk AI Assistant...'**
  String get messageHint;

  /// No description provided for @imageSelectedTitle.
  ///
  /// In en, this message translates to:
  /// **'Image selected'**
  String get imageSelectedTitle;

  /// No description provided for @imageSelectedMessage.
  ///
  /// In en, this message translates to:
  /// **'Image: {fileName}'**
  String imageSelectedMessage(String fileName);

  /// No description provided for @startConversationTitle.
  ///
  /// In en, this message translates to:
  /// **'Start a conversation'**
  String get startConversationTitle;

  /// No description provided for @startConversationSubtitle.
  ///
  /// In en, this message translates to:
  /// **'Ask me anything!'**
  String get startConversationSubtitle;

  /// No description provided for @suggestedPrompt1.
  ///
  /// In en, this message translates to:
  /// **'Explain quantum computing'**
  String get suggestedPrompt1;

  /// No description provided for @suggestedPrompt2.
  ///
  /// In en, this message translates to:
  /// **'Write a poem'**
  String get suggestedPrompt2;

  /// No description provided for @suggestedPrompt3.
  ///
  /// In en, this message translates to:
  /// **'Help with code'**
  String get suggestedPrompt3;

  /// No description provided for @streamErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Stream error'**
  String get streamErrorTitle;

  /// No description provided for @streamErrorMessage.
  ///
  /// In en, this message translates to:
  /// **'{error}'**
  String streamErrorMessage(String error);

  /// No description provided for @streamInterruptedTag.
  ///
  /// In en, this message translates to:
  /// **'[Stream interrupted]'**
  String get streamInterruptedTag;

  /// No description provided for @copyAction.
  ///
  /// In en, this message translates to:
  /// **'Copy'**
  String get copyAction;

  /// No description provided for @editMessageTitle.
  ///
  /// In en, this message translates to:
  /// **'Edit message'**
  String get editMessageTitle;

  /// No description provided for @editMessageHint.
  ///
  /// In en, this message translates to:
  /// **'Update your message'**
  String get editMessageHint;

  /// No description provided for @editMessageAction.
  ///
  /// In en, this message translates to:
  /// **'Resend'**
  String get editMessageAction;

  /// No description provided for @regenerateAction.
  ///
  /// In en, this message translates to:
  /// **'Regenerate'**
  String get regenerateAction;

  /// No description provided for @retryAction.
  ///
  /// In en, this message translates to:
  /// **'Retry'**
  String get retryAction;

  /// No description provided for @diagnosticsConnectionSection.
  ///
  /// In en, this message translates to:
  /// **'CONNECTION'**
  String get diagnosticsConnectionSection;

  /// No description provided for @diagnosticsBaseUrlLabel.
  ///
  /// In en, this message translates to:
  /// **'Base URL'**
  String get diagnosticsBaseUrlLabel;

  /// No description provided for @diagnosticsBaseUrlSource.
  ///
  /// In en, this message translates to:
  /// **'Source: {source}'**
  String diagnosticsBaseUrlSource(String source);

  /// No description provided for @diagnosticsPlatformLabel.
  ///
  /// In en, this message translates to:
  /// **'Platform'**
  String get diagnosticsPlatformLabel;

  /// No description provided for @diagnosticsLatencyLabel.
  ///
  /// In en, this message translates to:
  /// **'Latency'**
  String get diagnosticsLatencyLabel;

  /// No description provided for @diagnosticsLatencyUnavailable.
  ///
  /// In en, this message translates to:
  /// **'No latency recorded yet.'**
  String get diagnosticsLatencyUnavailable;

  /// No description provided for @diagnosticsModelLabel.
  ///
  /// In en, this message translates to:
  /// **'Selected model'**
  String get diagnosticsModelLabel;

  /// No description provided for @diagnosticsModelAvailable.
  ///
  /// In en, this message translates to:
  /// **'Available'**
  String get diagnosticsModelAvailable;

  /// No description provided for @diagnosticsModelUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Unavailable'**
  String get diagnosticsModelUnavailable;

  /// No description provided for @diagnosticsOllamaLabel.
  ///
  /// In en, this message translates to:
  /// **'Ollama health'**
  String get diagnosticsOllamaLabel;

  /// No description provided for @diagnosticsOllamaReady.
  ///
  /// In en, this message translates to:
  /// **'Ready'**
  String get diagnosticsOllamaReady;

  /// No description provided for @diagnosticsOllamaUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Unavailable'**
  String get diagnosticsOllamaUnavailable;

  /// No description provided for @diagnosticsOllamaButton.
  ///
  /// In en, this message translates to:
  /// **'Test /health/ollama'**
  String get diagnosticsOllamaButton;

  /// No description provided for @diagnosticsOllamaDetail.
  ///
  /// In en, this message translates to:
  /// **'Status: {status} | Model: {model} | {availability} | Models: {count}'**
  String diagnosticsOllamaDetail(
      String status, String model, String availability, String count);

  /// No description provided for @diagnosticsHfLabel.
  ///
  /// In en, this message translates to:
  /// **'HF GPU Ready'**
  String get diagnosticsHfLabel;

  /// No description provided for @diagnosticsHfReady.
  ///
  /// In en, this message translates to:
  /// **'Ready'**
  String get diagnosticsHfReady;

  /// No description provided for @diagnosticsHfUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Unavailable'**
  String get diagnosticsHfUnavailable;

  /// No description provided for @diagnosticsHfButton.
  ///
  /// In en, this message translates to:
  /// **'Test /health/hf'**
  String get diagnosticsHfButton;

  /// No description provided for @diagnosticsHfDetail.
  ///
  /// In en, this message translates to:
  /// **'GPU: {gpu} | Torch: {torch} | CUDA: {cuda} | Transformers: {transformers} | bitsandbytes: {bnb}'**
  String diagnosticsHfDetail(
      String gpu, String torch, String cuda, String transformers, String bnb);

  /// No description provided for @diagnosticsHealthButton.
  ///
  /// In en, this message translates to:
  /// **'Test /health'**
  String get diagnosticsHealthButton;

  /// No description provided for @diagnosticsModelsButton.
  ///
  /// In en, this message translates to:
  /// **'Test /models'**
  String get diagnosticsModelsButton;

  /// No description provided for @diagnosticsSourceOverride.
  ///
  /// In en, this message translates to:
  /// **'User override'**
  String get diagnosticsSourceOverride;

  /// No description provided for @diagnosticsSourceDartDefine.
  ///
  /// In en, this message translates to:
  /// **'Dart define'**
  String get diagnosticsSourceDartDefine;

  /// No description provided for @diagnosticsSourceDotenv.
  ///
  /// In en, this message translates to:
  /// **'Dotenv'**
  String get diagnosticsSourceDotenv;

  /// No description provided for @diagnosticsSourceWebRelease.
  ///
  /// In en, this message translates to:
  /// **'Web release (/api)'**
  String get diagnosticsSourceWebRelease;

  /// No description provided for @diagnosticsSourceWebDev.
  ///
  /// In en, this message translates to:
  /// **'Web dev (localhost)'**
  String get diagnosticsSourceWebDev;

  /// No description provided for @diagnosticsSourceAndroidEmulator.
  ///
  /// In en, this message translates to:
  /// **'Android emulator (10.0.2.2)'**
  String get diagnosticsSourceAndroidEmulator;

  /// No description provided for @diagnosticsSourceDesktop.
  ///
  /// In en, this message translates to:
  /// **'Desktop (localhost)'**
  String get diagnosticsSourceDesktop;

  /// No description provided for @diagnosticsChatButton.
  ///
  /// In en, this message translates to:
  /// **'Test /chat'**
  String get diagnosticsChatButton;

  /// No description provided for @diagnosticsStreamButton.
  ///
  /// In en, this message translates to:
  /// **'Test /chat/stream'**
  String get diagnosticsStreamButton;

  /// No description provided for @diagnosticsStreamRunning.
  ///
  /// In en, this message translates to:
  /// **'Streaming...'**
  String get diagnosticsStreamRunning;

  /// No description provided for @diagnosticsLastErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Last error'**
  String get diagnosticsLastErrorTitle;

  /// No description provided for @diagnosticsErrorStatusLabel.
  ///
  /// In en, this message translates to:
  /// **'Status'**
  String get diagnosticsErrorStatusLabel;

  /// No description provided for @diagnosticsErrorBodyLabel.
  ///
  /// In en, this message translates to:
  /// **'Body'**
  String get diagnosticsErrorBodyLabel;

  /// No description provided for @diagnosticsErrorHeadersLabel.
  ///
  /// In en, this message translates to:
  /// **'Headers'**
  String get diagnosticsErrorHeadersLabel;

  /// No description provided for @diagnosticsNoErrors.
  ///
  /// In en, this message translates to:
  /// **'No errors recorded yet.'**
  String get diagnosticsNoErrors;

  /// No description provided for @diagnosticsStreamSampleTitle.
  ///
  /// In en, this message translates to:
  /// **'SSE sample'**
  String get diagnosticsStreamSampleTitle;

  /// No description provided for @diagnosticsNoStreamSample.
  ///
  /// In en, this message translates to:
  /// **'No stream events captured.'**
  String get diagnosticsNoStreamSample;

  /// No description provided for @diagnosticsLogsTitle.
  ///
  /// In en, this message translates to:
  /// **'Diagnostics log'**
  String get diagnosticsLogsTitle;

  /// No description provided for @diagnosticsCopyLog.
  ///
  /// In en, this message translates to:
  /// **'Copy log'**
  String get diagnosticsCopyLog;

  /// No description provided for @diagnosticsNoLogs.
  ///
  /// In en, this message translates to:
  /// **'No diagnostics run yet.'**
  String get diagnosticsNoLogs;

  /// No description provided for @diagnosticsTestMessage.
  ///
  /// In en, this message translates to:
  /// **'Hello'**
  String get diagnosticsTestMessage;

  /// No description provided for @microphonePermissionRequired.
  ///
  /// In en, this message translates to:
  /// **'Microphone permission is required for voice input'**
  String get microphonePermissionRequired;

  /// No description provided for @speechNotAvailable.
  ///
  /// In en, this message translates to:
  /// **'Speech recognition is not available'**
  String get speechNotAvailable;

  /// No description provided for @enterMessagePrompt.
  ///
  /// In en, this message translates to:
  /// **'Please enter a message or use voice input!'**
  String get enterMessagePrompt;

  /// No description provided for @exportFailedTitle.
  ///
  /// In en, this message translates to:
  /// **'Export failed'**
  String get exportFailedTitle;

  /// No description provided for @noMessagesToExport.
  ///
  /// In en, this message translates to:
  /// **'No messages to export'**
  String get noMessagesToExport;

  /// No description provided for @exportSuccessTitle.
  ///
  /// In en, this message translates to:
  /// **'Export successful'**
  String get exportSuccessTitle;

  /// No description provided for @exportSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'Saved to {path}\\nAlso copied to clipboard'**
  String exportSuccessMessage(String path);

  /// No description provided for @exportSuccessWebMessage.
  ///
  /// In en, this message translates to:
  /// **'Downloaded file and copied to clipboard'**
  String get exportSuccessWebMessage;

  /// No description provided for @logout.
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logout;

  /// No description provided for @clearChat.
  ///
  /// In en, this message translates to:
  /// **'Clear chat'**
  String get clearChat;

  /// No description provided for @exportChat.
  ///
  /// In en, this message translates to:
  /// **'Export chat'**
  String get exportChat;

  /// No description provided for @logoutSuccessTitle.
  ///
  /// In en, this message translates to:
  /// **'Success'**
  String get logoutSuccessTitle;

  /// No description provided for @logoutSuccessMessage.
  ///
  /// In en, this message translates to:
  /// **'Logged out successfully'**
  String get logoutSuccessMessage;

  /// No description provided for @logoutErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get logoutErrorTitle;

  /// No description provided for @copiedToClipboard.
  ///
  /// In en, this message translates to:
  /// **'Copied to clipboard'**
  String get copiedToClipboard;

  /// No description provided for @yesterdayAt.
  ///
  /// In en, this message translates to:
  /// **'Yesterday {time}'**
  String yesterdayAt(String time);

  /// No description provided for @aiThinking.
  ///
  /// In en, this message translates to:
  /// **'AI is thinking...'**
  String get aiThinking;

  /// No description provided for @infoTitle.
  ///
  /// In en, this message translates to:
  /// **'Info'**
  String get infoTitle;

  /// No description provided for @successTitle.
  ///
  /// In en, this message translates to:
  /// **'Success'**
  String get successTitle;

  /// No description provided for @errorTitle.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get errorTitle;

  /// No description provided for @imagePickerErrorTitle.
  ///
  /// In en, this message translates to:
  /// **'Error'**
  String get imagePickerErrorTitle;

  /// No description provided for @imagePickerErrorMessage.
  ///
  /// In en, this message translates to:
  /// **'Failed to pick image: {error}'**
  String imagePickerErrorMessage(String error);

  /// No description provided for @chooseImageSourceTitle.
  ///
  /// In en, this message translates to:
  /// **'Choose image source'**
  String get chooseImageSourceTitle;

  /// No description provided for @cameraLabel.
  ///
  /// In en, this message translates to:
  /// **'Camera'**
  String get cameraLabel;

  /// No description provided for @galleryLabel.
  ///
  /// In en, this message translates to:
  /// **'Gallery'**
  String get galleryLabel;

  /// No description provided for @appwritePingSuccess.
  ///
  /// In en, this message translates to:
  /// **'Appwrite connection is successful!'**
  String get appwritePingSuccess;

  /// No description provided for @appwritePingNoSession.
  ///
  /// In en, this message translates to:
  /// **'Appwrite connection is OK but no session is active.'**
  String get appwritePingNoSession;

  /// No description provided for @appwritePingError.
  ///
  /// In en, this message translates to:
  /// **'Appwrite ping error: {error}'**
  String appwritePingError(String error);

  /// No description provided for @sendPingTooltip.
  ///
  /// In en, this message translates to:
  /// **'Send a ping'**
  String get sendPingTooltip;

  /// No description provided for @logoutTooltip.
  ///
  /// In en, this message translates to:
  /// **'Logout'**
  String get logoutTooltip;

  /// No description provided for @assistantTitle.
  ///
  /// In en, this message translates to:
  /// **'AI assistant'**
  String get assistantTitle;

  /// No description provided for @assistantHint.
  ///
  /// In en, this message translates to:
  /// **'Type a message or hold for voice input...'**
  String get assistantHint;

  /// No description provided for @listeningStatus.
  ///
  /// In en, this message translates to:
  /// **'Listening to voice input...'**
  String get listeningStatus;

  /// No description provided for @startChatHint.
  ///
  /// In en, this message translates to:
  /// **'Start chatting with the AI assistant!'**
  String get startChatHint;

  /// No description provided for @errorInvalidRequest.
  ///
  /// In en, this message translates to:
  /// **'Error: Invalid request'**
  String get errorInvalidRequest;

  /// No description provided for @errorInvalidRequestFormat.
  ///
  /// In en, this message translates to:
  /// **'Error: Invalid request format.'**
  String get errorInvalidRequestFormat;

  /// No description provided for @errorServiceUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Error: AI service is unavailable.'**
  String get errorServiceUnavailable;

  /// No description provided for @errorTimeout.
  ///
  /// In en, this message translates to:
  /// **'Error: AI response timeout.'**
  String get errorTimeout;

  /// No description provided for @errorBackendUnavailable.
  ///
  /// In en, this message translates to:
  /// **'Error: Backend service unavailable.'**
  String get errorBackendUnavailable;

  /// No description provided for @errorNoInternet.
  ///
  /// In en, this message translates to:
  /// **'Error: No internet connection.'**
  String get errorNoInternet;

  /// No description provided for @errorInvalidServerResponse.
  ///
  /// In en, this message translates to:
  /// **'Error: Invalid server response.'**
  String get errorInvalidServerResponse;

  /// No description provided for @errorUnexpected.
  ///
  /// In en, this message translates to:
  /// **'Error: Unexpected error.'**
  String get errorUnexpected;

  /// No description provided for @noResponseGenerated.
  ///
  /// In en, this message translates to:
  /// **'Sorry, no response generated.'**
  String get noResponseGenerated;

  /// No description provided for @requestTimeoutMessage.
  ///
  /// In en, this message translates to:
  /// **'Request timed out. Please try again.'**
  String get requestTimeoutMessage;

  /// No description provided for @speechRecognitionFailed.
  ///
  /// In en, this message translates to:
  /// **'Speech recognition failed. Please try again.'**
  String get speechRecognitionFailed;

  /// No description provided for @speechRecognitionError.
  ///
  /// In en, this message translates to:
  /// **'Speech recognition error. Please check your network.'**
  String get speechRecognitionError;

  /// No description provided for @serverConnectionFailed.
  ///
  /// In en, this message translates to:
  /// **'Server connection failed.'**
  String get serverConnectionFailed;
}

class _AppLocalizationsDelegate
    extends LocalizationsDelegate<AppLocalizations> {
  const _AppLocalizationsDelegate();

  @override
  Future<AppLocalizations> load(Locale locale) {
    return SynchronousFuture<AppLocalizations>(lookupAppLocalizations(locale));
  }

  @override
  bool isSupported(Locale locale) =>
      <String>['en', 'tr'].contains(locale.languageCode);

  @override
  bool shouldReload(_AppLocalizationsDelegate old) => false;
}

AppLocalizations lookupAppLocalizations(Locale locale) {
  // Lookup logic when only language code is specified.
  switch (locale.languageCode) {
    case 'en':
      return AppLocalizationsEn();
    case 'tr':
      return AppLocalizationsTr();
  }

  throw FlutterError(
      'AppLocalizations.delegate failed to load unsupported locale "$locale". This is likely '
      'an issue with the localizations generation tool. Please file an issue '
      'on GitHub with a reproducible sample app and the gen-l10n configuration '
      'that was used.');
}
