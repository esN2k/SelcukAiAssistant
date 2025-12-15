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

    // Mock path_provider channel to return a safe temp directory
    // This is safer than returning '.' which might cause lock issues in CI
    const channel = MethodChannel('plugins.flutter.io/path_provider');

    // We create a temp dir for the test
    final tempDir = Directory.systemTemp.createTempSync();

    // Mock the channel to return this temp dir path
    TestDefaultBinaryMessengerBinding.instance.defaultBinaryMessenger
        .setMockMethodCallHandler(channel, (MethodCall methodCall) async {
      return tempDir.path;
    });
  });

  testWidgets('AI Asistanı uygulama testi', (WidgetTester tester) async {
    // Initialize Preferences
    // This calls Hive.initFlutter()
    // which calls getApplicationDocumentsDirectory
    // which hits our mock above.
    await Pref.initialize();

    // Build our app and trigger a frame.
    await tester.pumpWidget(const MyApp());

    // Verify that the app starts properly
    // We check for MaterialApp (or GetMaterialApp)
    expect(find.byType(MaterialApp), findsOneWidget);

    // Pump once more to ensure everything is rendered
    await tester.pump();
  });

  tearDownAll(Hive.close);
}
