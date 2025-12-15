import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:hive/hive.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/main.dart';

void main() {
  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();

    // Mock path_provider
    const channel = MethodChannel('plugins.flutter.io/path_provider');
    final tempDir = Directory.systemTemp.createTempSync();

    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
      return tempDir.path;
    });

    // Initialize Hive manually for the test environment
    Hive.init(tempDir.path);

    // Open the box used by Pref manually to ensure it's ready.
    // This avoids Pref.initialize() getting stuck if initFlutter behaves oddly.
    if (!Hive.isBoxOpen('myData')) {
      await Hive.openBox<dynamic>('myData');
    }
  });

  testWidgets('AI Asistanı uygulama testi', (WidgetTester tester) async {
    // Run Pref.initialize. Since Hive is already inited and box is open,
    // this should be fast/instant.
    await Pref.initialize();

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the app starts properly
    expect(find.byType(MaterialApp), findsOneWidget);

    // Let the splash screen timer complete so no pending timers remain
    await tester.pump(const Duration(seconds: 3));
  });

  tearDownAll(() async {
    await Hive.close();
  });
}
