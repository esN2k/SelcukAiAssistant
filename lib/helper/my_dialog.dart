// Using deprecated Get.snackbar API until migrated to newer GetX version

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/widget/custom_loading.dart';

class MyDialog {
  // Bilgi mesajı
  static void info(String msg) {
    final l10n = L10n.current();
    Get.snackbar(
      l10n?.infoTitle ?? 'Bilgi',
      msg,
      backgroundColor: Colors.amber.withValues(alpha: 0.7),
      colorText: Colors.white,
    );
  }

  // Başarı mesajı
  static void success(String msg) {
    final l10n = L10n.current();
    Get.snackbar(
      l10n?.successTitle ?? 'Başarılı',
      msg,
      backgroundColor: Colors.green.withValues(alpha: 0.7),
      colorText: Colors.white,
    );
  }

  // Hata mesajı
  static void error(String msg) {
    final l10n = L10n.current();
    Get.snackbar(
      l10n?.errorTitle ?? 'Hata',
      msg,
      backgroundColor: Colors.redAccent.withValues(alpha: 0.7),
      colorText: Colors.white,
    );
  }

  // Yükleme göstergesi
  static void showLoadingDialog() {
    unawaited(Get.dialog<void>(const Center(child: CustomLoading())));
  }
}
