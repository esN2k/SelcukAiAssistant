import 'dart:developer';

import 'package:flutter/material.dart';

class AdHelper {
  static void init() {
    log('AdHelper: Web initialization (No-op)');
  }

  static void showInterstitialAd(VoidCallback onComplete) {
    log('AdHelper: Web interstitial (No-op)');
    onComplete();
  }

  static Widget nativeAd() {
    return const SizedBox.shrink();
  }

  static Widget nativeBannerAd() {
    return const SizedBox.shrink();
  }
}
