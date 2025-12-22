import 'dart:async';

import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:lottie/lottie.dart';
import 'package:selcukaiassistant/helper/app_theme.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/onboard.dart';
import 'package:selcukaiassistant/screen/home_screen.dart';
import 'package:selcukaiassistant/widget/custom_btn.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final c = PageController();

    final list = [
      Onboard(
        title: context.l10n.onboardingTitle1,
        subtitle: context.l10n.onboardingSubtitle1,
        lottie: 'ai_ask_me',
      ),
      Onboard(
        title: context.l10n.onboardingTitle2,
        subtitle: context.l10n.onboardingSubtitle2,
        lottie: 'ai_play',
      ),
    ];

    return Scaffold(
      body: PageView.builder(
        controller: c,
        itemCount: list.length,
        itemBuilder: (ctx, ind) {
          final isLast = ind == list.length - 1;

          return Column(
            children: [
              //lottie
              Lottie.asset(
                'assets/lottie/${list[ind].lottie}.json',
                height: Global.mq.height * .6,
                width: isLast ? Global.mq.width * .7 : null,
              ),

              //title
              Text(
                list[ind].title,
                style: const TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w900,
                  letterSpacing: .5,
                ),
              ),

              //for adding some space
              SizedBox(height: Global.mq.height * .015),

              //subtitle
              SizedBox(
                width: Global.mq.width * .7,
                child: Text(
                  list[ind].subtitle,
                  textAlign: TextAlign.center,
                  style: TextStyle(
                    fontSize: 13.5,
                    letterSpacing: .5,
                    color: Theme.of(context).lightTextColor,
                  ),
                ),
              ),

              const Spacer(),

              //dots

              Wrap(
                spacing: 10,
                children: List.generate(
                  list.length,
                  (i) => Container(
                    width: i == ind ? 15 : 10,
                    height: 8,
                    decoration: BoxDecoration(
                      color: i == ind ? Colors.amber : Colors.grey,
                      borderRadius: const BorderRadius.all(Radius.circular(5)),
                    ),
                  ),
                ),
              ),

              const Spacer(),

              //button
              CustomBtn(
                onTap: () {
                  if (isLast) {
                    unawaited(Get.off<dynamic>(() => const HomeScreen()));
                  } else {
                    unawaited(
                      c.nextPage(
                        duration: const Duration(milliseconds: 600),
                        curve: Curves.ease,
                      ),
                    );
                  }
                },
                text: isLast
                    ? context.l10n.onboardingDone
                    : context.l10n.onboardingNext,
              ),

              const Spacer(flex: 2),
            ],
          );
        },
      ),
    );
  }
}
