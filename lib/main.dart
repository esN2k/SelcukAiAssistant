import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:get/get_navigation/src/root/get_material_app.dart';
import 'package:selcukaiassistant/helper/ad_helper.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/screen/splash_screen.dart';
import 'package:selcukaiassistant/services/storage/storage_service.dart';
import 'package:selcukaiassistant/theme/selcuk_theme.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Catch global errors
  FlutterError.onError = (details) {
    if (kDebugMode) {
      print('Flutter Error: ${details.exception}');
      print(details.stack);
    }
  };

  // Initialize storage before app bootstraps.
  await StorageService.initialize();

  // Initialize preferences
  await Pref.initialize();

  // Load environment variables
  await dotenv.load();

  // Mobile-only initializations
  if (!kIsWeb) {
    // Initialize facebook ads sdk
    AdHelper.init();

    // Set system UI mode and preferred orientations
    await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
    await SystemChrome.setPreferredOrientations(
      [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown],
    );
  }

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: Global.appName,
      debugShowCheckedModeBanner: false,
      themeMode: Pref.defaultTheme,
      theme: SelcukTheme.light(),
      darkTheme: SelcukTheme.dark(),
      supportedLocales: L10n.supportedLocales,
      localizationsDelegates: AppLocalizations.localizationsDelegates,
      locale: L10n.currentLocale,
      fallbackLocale: L10n.fallbackLocale,
      localeResolutionCallback: (deviceLocale, supportedLocales) {
        return L10n.resolveLocale(deviceLocale);
      },
      onGenerateTitle: (context) => context.l10n.appTitle,
      home: const SplashScreen(),
    );
  }
}
