import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/main.dart';

void main() {
  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();
  });

  testWidgets('AI Asistanı uygulama testi', (WidgetTester tester) async {
    // Mock path_provider for Hive
    const channel = MethodChannel('plugins.flutter.io/path_provider');
    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(channel,
        (MethodCall methodCall) async {
      return '.';
    });

    // Initialize Preferences
    await Pref.initialize();

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the app starts and builds the MaterialApp/GetMaterialApp
    expect(find.byType(MaterialApp), findsOneWidget);

    // We do NOT wait for the 2-second splash screen transition here
    // because it involves Lottie animations (which loops) and GetX navigation
    // which can cause timeouts in widget tests if not carefully handled.
    // The presence of MaterialApp confirms the app entry point works.
  });
}
