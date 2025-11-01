import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/screen/home_screen.dart';
import 'package:selcukaiassistant/screen/onboarding_screen.dart';
import 'package:selcukaiassistant/widget/custom_loading.dart';

class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();

    //wait for some time on splash & then move to next screen
    Future.delayed(const Duration(seconds: 2), () {
      Get.off<Widget>(
        () =>
            Pref.showOnboarding ? const OnboardingScreen() : const HomeScreen(),
      );
    });
  }

  @override
  Widget build(BuildContext context) {
    //initializing device size
    mq = MediaQuery.sizeOf(context);

    return Scaffold(
      //body
      body: SizedBox(
        width: double.maxFinite,
        child: Column(
          children: [
            //for adding some space
            const Spacer(flex: 2),

            //logo
            Card(
              shape: const RoundedRectangleBorder(
                borderRadius: BorderRadius.all(Radius.circular(20)),
              ),
              child: Padding(
                padding: EdgeInsets.all(mq.width * .05),
                child: Image.asset(
                  'assets/images/logo.png',
                  width: mq.width * .4,
                ),
              ),
            ),

            //for adding some space
            const Spacer(),

            //lottie loading
            const CustomLoading(),

            //for adding some space
            const Spacer(),
          ],
        ),
      ),
    );
  }
}
