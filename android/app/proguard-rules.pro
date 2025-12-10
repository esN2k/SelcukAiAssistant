# Flutter wrapper
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.** { *; }
-keep class io.flutter.util.** { *; }
-keep class io.flutter.view.** { *; }
-keep class io.flutter.** { *; }
-keep class io.flutter.plugins.** { *; }

# Facebook SDK
-keep class com.facebook.** { *; }
-keep interface com.facebook.** { *; }
-keep enum com.facebook.** { *; }
-keep class com.facebook.infer.annotation.** { *; }
-keep @interface com.facebook.infer.annotation.** { *; }
-dontwarn com.facebook.**
-dontwarn com.facebook.infer.annotation.**

# Easy Audience Network (Facebook Audience Network)
-keep class com.facebook.ads.** { *; }
-dontwarn com.facebook.ads.**

# Google Play Core Library
-keep class com.google.android.play.core.** { *; }
-keep interface com.google.android.play.core.** { *; }
-dontwarn com.google.android.play.core.**

# Keep nullable annotations
-dontwarn javax.annotation.**
-keep interface javax.annotation.** { *; }
-keep class javax.annotation.** { *; }

# Keep generated code
-keep class **.R { *; }
-keep class **.R$* { *; }


