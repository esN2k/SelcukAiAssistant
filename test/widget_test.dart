import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/controller/enhanced_chat_controller.dart';
import 'package:selcukaiassistant/controller/settings_controller.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/main.dart';
import 'package:selcukaiassistant/model/conversation.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/screen/feature/new_chat_screen.dart';
import 'package:selcukaiassistant/screen/settings_screen.dart';
import 'package:selcukaiassistant/services/conversation_service.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';
import 'package:selcukaiassistant/widget/enhanced_message_card.dart';

class FakeEnhancedChatController extends EnhancedChatController {
  // ...existing code...

  @override
  void onClose() {
    textC.dispose();
    scrollC.dispose();
  }
}

Widget _wrapWithApp(Widget child, {Locale locale = const Locale('tr')}) {
  return GetMaterialApp(
    locale: locale,
    supportedLocales: L10n.supportedLocales,
    localizationsDelegates: AppLocalizations.localizationsDelegates,
    home: child,
  );
}

void main() {
  late Directory tempDir;

  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();
    Get.testMode = true;

    tempDir = Directory.systemTemp.createTempSync();
    await StorageService.initializeForTesting(tempDir.path);
    await Pref.initialize();
    await ConversationService.init();
  });

  tearDown(Get.reset);

  testWidgets('AI Asistanı uygulama testi', (WidgetTester tester) async {
    await tester.pumpWidget(const MyApp());

    expect(find.byType(MaterialApp), findsOneWidget);

    await tester.pump(const Duration(seconds: 3));
  });

  testWidgets('Ayarlar ekranı render edilir', (WidgetTester tester) async {
    final l10n = await AppLocalizations.delegate.load(const Locale('tr'));
    Get.put<SettingsController>(
      SettingsController(fetchModels: () async => <ModelInfo>[]),
    );

    await tester.pumpWidget(_wrapWithApp(const SettingsScreen()));
    await tester.pumpAndSettle();

    expect(find.text(l10n.settingsTitle), findsOneWidget);
  });

  testWidgets('Yeni sohbet ekranı render edilir', (WidgetTester tester) async {
    final l10n = await AppLocalizations.delegate.load(const Locale('tr'));
    Get.put<EnhancedChatController>(FakeEnhancedChatController());

    await tester.pumpWidget(_wrapWithApp(const NewChatScreen()));
    await tester.pumpAndSettle();

    expect(find.text(l10n.startConversationTitle), findsOneWidget);
  });

  testWidgets('RAG kaynakları görünür', (WidgetTester tester) async {
    final l10n = await AppLocalizations.delegate.load(const Locale('tr'));
    final message = ChatMessage(
      id: 'm1',
      content: 'Örnek yanıt.',
      isUser: false,
      createdAt: DateTime.now(),
      citations: const ['Kaynak A', 'Kaynak B'],
    );

    await tester.pumpWidget(
      _wrapWithApp(EnhancedMessageCard(message: message)),
    );

    expect(find.text(l10n.sourcesTitle), findsOneWidget);
    expect(find.textContaining('Kaynak A'), findsOneWidget);
    expect(find.textContaining('Kaynak B'), findsOneWidget);
  });

  tearDownAll(() async {
    await StorageService.close();
    await tempDir.delete(recursive: true);
  });
}
