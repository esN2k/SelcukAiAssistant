import 'dart:async';
import 'dart:developer';

import 'package:easy_audience_network/easy_audience_network.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/my_dialog.dart';

class AdHelper {
  static void init() {
    unawaited(
      EasyAudienceNetwork.init(
        testMode: true,
      ),
    );
  }

  static void showInterstitialAd(VoidCallback onComplete) {
    MyDialog.showLoadingDialog();

    InterstitialAd? interstitialAd;
    interstitialAd = InterstitialAd(InterstitialAd.testPlacementId)
      ..listener = InterstitialAdListener(
        onLoaded: () {
          Get.back<dynamic>();
          onComplete();

          unawaited(interstitialAd!.show());
        },
        onDismissed: () => interstitialAd!.destroy(),
        onError: (i, e) {
          Get.back<dynamic>();
          onComplete();

          log('interstitial error: $e');
        },
      );
    unawaited(interstitialAd.load());
  }

  static Widget nativeAd() {
    return SafeArea(
      child: NativeAd(
        adType: NativeAdType.NATIVE_AD,
        keepExpandedWhileLoading: false,
        expandAnimationDuraion: 1000,
        listener: NativeAdListener(
          onError: (code, message) => log('error'),
          onLoaded: () => log('loaded'),
          onClicked: () => log('clicked'),
          onLoggingImpression: () => log('logging impression'),
          onMediaDownloaded: () => log('media downloaded'),
        ),
      ),
    );
  }

  static Widget nativeBannerAd() {
    return SafeArea(
      child: NativeAd(
        adType: NativeAdType.NATIVE_BANNER_AD,
        bannerAdSize: NativeBannerAdSize.HEIGHT_100,
        keepExpandedWhileLoading: false,
        height: 100,
        expandAnimationDuraion: 1000,
        listener: NativeAdListener(
          onError: (code, message) => log('error'),
          onLoaded: () => log('loaded'),
          onClicked: () => log('clicked'),
          onLoggingImpression: () => log('logging impression'),
          onMediaDownloaded: () => log('media downloaded'),
        ),
      ),
    );
  }
}
