// Using deprecated Get.snackbar API until migrated to newer GetX version
// ignore_for_file: deprecated_member_use

import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/widget/custom_loading.dart';

class MyDialog {
//info
  static void info(String msg) {
    Get.snackbar(
      'Bilgi',
      msg,
      backgroundColor: Colors.amber.withOpacity(.7),
      colorText: Colors.white,
    );
  }

//success
  static void success(String msg) {
    Get.snackbar(
      'Başarılı',
      msg,
      backgroundColor: Colors.green.withOpacity(.7),
      colorText: Colors.white,
    );
  }

//error
  static void error(String msg) {
    Get.snackbar(
      'Hata',
      msg,
      backgroundColor: Colors.redAccent.withOpacity(.7),
      colorText: Colors.white,
    );
  }

  //loading dialog
  static void showLoadingDialog() {
    unawaited(Get.dialog<void>(const Center(child: CustomLoading())));
  }
}
