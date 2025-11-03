import 'package:flutter/material.dart';
import 'package:get/route_manager.dart';
import 'package:lottie/lottie.dart';
import 'package:selcukaiassistant/helper/global.dart';
import 'package:selcukaiassistant/main.dart';
import 'package:selcukaiassistant/model/onboard.dart';
import 'package:selcukaiassistant/screen/home_screen.dart';
import 'package:selcukaiassistant/widget/custom_btn.dart';

class OnboardingScreen extends StatelessWidget {
  const OnboardingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final c = PageController();

    final list = [
      //onboarding 1
      Onboard(
        title: 'Bana bir şey sor',
        subtitle:
            'Senin en iyi arkadaşın olabilirim ve bana her şeyi sorabilirsin, sana yardım ederim!',
        lottie: 'ai_ask_me',
      ),

      //onboarding 2
      Onboard(
        title: 'Hayalden Gerçeğe',
        lottie: 'ai_play',
        subtitle:
            'Sadece hayal edin ve bana söyleyin, sizin için harika bir şey yaratacağım!',
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
                height: mq.height * .6,
                width: isLast ? mq.width * .7 : null,
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
              SizedBox(height: mq.height * .015),

              //subtitle
              SizedBox(
                width: mq.width * .7,
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
                    Get.off<dynamic>(() => const HomeScreen());
                    // Navigator.of(context).pushReplacement(MaterialPageRoute(
                    //     builder: (_) => const HomeScreen()));
                  } else {
                    c.nextPage(
                      duration: const Duration(milliseconds: 600),
                      curve: Curves.ease,
                    );
                  }
                },
                text: isLast ? 'Bitti' : 'Sıradaki',
              ),

              const Spacer(flex: 2),
            ],
          );
        },
      ),
    );
  }
}
