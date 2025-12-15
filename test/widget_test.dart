import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/main.dart';

void main() {
  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();

    // Initialize Hive with a temporary path for testing
    // Note: Hive.init is deprecated in favor of initFlutter but for unit tests
    // without path_provider it's safer to use init with a fixed path if possible,
    // or mock the channel as we do below.
  });

  testWidgets('AI Asistanı uygulama testi', (WidgetTester tester) async {
    // Mock the path_provider channel to return a temp path.
    // This allows Hive.initFlutter() (called inside Pref.initialize) to succeed.
    const channel = MethodChannel('plugins.flutter.io/path_provider');
    tester.binding.defaultBinaryMessenger.setMockMethodCallHandler(channel,
        (MethodCall methodCall) async {
      return '.';
    });

    // Initialize Preferences (which initializes Hive)
    await Pref.initialize();

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Allow animations to settle (loading screen etc)
    await tester.pump(const Duration(seconds: 2));

    // Verify that the app starts properly (Splash screen usually has a loader or logo)
    // We check for the MaterialApp widget as a basic smoke test.
    // Use find.byType(GetMaterialApp) if checking specifically for GetX root,
    // but MaterialApp is inside it or it wraps it.
    // Actually MyApp returns GetMaterialApp.
    expect(find.byType(MaterialApp), findsOneWidget);
  });
}
