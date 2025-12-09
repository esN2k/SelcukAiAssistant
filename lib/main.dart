// ignore_for_file: deprecated_member_use

import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';
import 'package:get/get_navigation/src/root/get_material_app.dart';
import 'package:selcukaiassistant/helper/ad_helper.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/splash_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // init hive@override
  // Widget build(BuildContext context) {
  //   return GetMaterialApp(
  //     title: appName,
  //     debugShowCheckedModeBanner: false,
  //
  //     themeMode: Pref.defaultTheme,
  //
  //     // Gece modu (Dark theme)
  //     darkTheme: ThemeData(
  //       useMaterial3: false,
  //       brightness: Brightness.dark,
  //       scaffoldBackgroundColor: Colors.black, // Siyah arka plan
  //       textTheme: const TextTheme(
  //         bodyLarge: TextStyle(color: Colors.yellow), // Ana metin rengi sarı
  //         bodyMedium: TextStyle(color: Colors.yellow),
  //         titleLarge: TextStyle(color: Colors.yellow),
  //       ),
  //       appBarTheme: const AppBarTheme(
  //         elevation: 1,
  //         centerTitle: true,
  //         backgroundColor: Colors.black,
  //         titleTextStyle: TextStyle(
  //           color: Colors.yellow,
  //           fontSize: 20,
  //           fontWeight: FontWeight.w500
  //         ),
  //         iconTheme: IconThemeData(color: Colors.yellow),
  //       ),
  //     ),
  //
  //     // Gündüz modu (Light theme)
  //     theme: ThemeData(
  //       useMaterial3: false,
  //       brightness: Brightness.light,
  //       scaffoldBackgroundColor: Colors.white, // Beyaz arka plan
  //       textTheme: const TextTheme(
  //         bodyLarge: TextStyle(color: Colors.yellow), // Ana metin rengi sarı
  //         bodyMedium: TextStyle(color: Colors.yellow),
  //         titleLarge: TextStyle(color: Colors.yellow),
  //       ),
  //       appBarTheme: const AppBarTheme(
  //         elevation: 1,
  //         centerTitle: true,
  //         backgroundColor: Colors.white,
  //         titleTextStyle: TextStyle(
  //           color: Colors.yellow,
  //           fontSize: 20,
  //           fontWeight: FontWeight.w500
  //         ),
  //         iconTheme: IconThemeData(color: Colors.yellow),
  //       ),
  //     ),
  //
  //     home: const SplashScreen(),
  //   );
  // }
  await Pref.initialize();

  await dotenv.load(); // .env dosyasını yükle
  runApp(const MyApp());

  // for app write initialization
  // AppWrite.init();

  // for initializing facebook ads sdk
  AdHelper.init();

  await SystemChrome.setEnabledSystemUIMode(SystemUiMode.immersiveSticky);
  await SystemChrome.setPreferredOrientations(
    [DeviceOrientation.portraitUp, DeviceOrientation.portraitDown],
  );

  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return GetMaterialApp(
      title: appName,
      debugShowCheckedModeBanner: false,

      themeMode: Pref.defaultTheme,

      //dark
      darkTheme: ThemeData(
        useMaterial3: false,
        brightness: Brightness.dark,
        appBarTheme: const AppBarTheme(
          elevation: 1,
          centerTitle: true,
          titleTextStyle: TextStyle(fontSize: 20, fontWeight: FontWeight.w500),
        ),
      ),

      //light
      theme: ThemeData(
        useMaterial3: false,
        appBarTheme: const AppBarTheme(
          elevation: 1,
          centerTitle: true,
          backgroundColor: Colors.white,
          iconTheme: IconThemeData(color: Colors.amber),
          titleTextStyle: TextStyle(
            color: Colors.amber,
            fontSize: 20,
            fontWeight: FontWeight.w500,
          ),
        ),
      ),

      //
      home: const SplashScreen(),
    );
  }
}

extension AppTheme on ThemeData {
  //light text color
  Color get lightTextColor =>
      brightness == Brightness.dark ? Colors.white70 : Colors.black54;

  //button color
  Color get buttonColor => brightness == Brightness.dark
      ? Colors.cyan.withOpacity(.5)
      : Colors.amber;
}
