import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/main.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';

void main() {
  late Directory tempDir;

  setUpAll(() async {
    TestWidgetsFlutterBinding.ensureInitialized();

    tempDir = Directory.systemTemp.createTempSync();
    await StorageService.initializeForTesting(tempDir.path);
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
    await StorageService.close();
    await tempDir.delete(recursive: true);
  });
}
