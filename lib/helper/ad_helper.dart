import 'dart:developer';

import 'package:easy_audience_network/easy_audience_network.dart';
import 'package:flutter/material.dart';
import 'package:get/get.dart';

import 'package:selcukaiassistant/helper/my_dialog.dart';

class AdHelper {
  static void init() {
    EasyAudienceNetwork.init(
      testMode:
          true, // for testing purpose but comment it before making the app live
    );
  }

  static void showInterstitialAd(VoidCallback onComplete) {
    //show loading
    MyDialog.showLoadingDialog();

    final interstitialAd = InterstitialAd(InterstitialAd.testPlacementId);

    interstitialAd.listener = InterstitialAdListener(
      onLoaded: () {
        //hide loading
        Get.back<dynamic>();
        onComplete();

        interstitialAd.show();
      },
      onDismissed: interstitialAd.destroy,
      onError: (i, e) {
        //hide loading
        Get.back<dynamic>();
        onComplete();

        log('interstitial error: $e');
      },
    );

    interstitialAd.load();
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
