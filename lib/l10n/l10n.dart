import 'package:flutter/widgets.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';

class L10n {
  static const supportedLocales = [Locale('tr'), Locale('en')];

  static Locale get fallbackLocale => const Locale('tr');

  static Locale get currentLocale {
    final stored = Pref.localeCode;
    if (stored == null || stored.isEmpty) {
      return fallbackLocale;
    }
    return Locale(stored);
  }

  static Locale resolveLocale(Locale? deviceLocale) {
    if (deviceLocale == null) {
      return fallbackLocale;
    }
    for (final locale in supportedLocales) {
      if (locale.languageCode == deviceLocale.languageCode) {
        return locale;
      }
    }
    return fallbackLocale;
  }

  static AppLocalizations? of(BuildContext context) {
    return AppLocalizations.of(context);
  }

  static AppLocalizations? current() {
    final context = Get.context;
    if (context == null) {
      return null;
    }
    return AppLocalizations.of(context);
  }
}

extension AppLocalizationsX on BuildContext {
  AppLocalizations get l10n => AppLocalizations.of(this);
}
