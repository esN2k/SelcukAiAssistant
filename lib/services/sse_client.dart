// ════════════════════════════════════════════════════════════════════
// DOSYA ADI: sse_client.dart
// AMAÇ: Server-Sent Events (SSE) istemci entegrasyonu
// KULLANIM: Platform bazlı SSE implementasyonunu export eder
// YAZAN: esN2k - Selçuk Üniversitesi
// ════════════════════════════════════════════════════════════════════
//
// DETAYLI AÇIKLAMA:
// Bu dosya, SSE (Server-Sent Events) istemcisini platform bazlı
// export eder.
//
// SSE NEDİR:
// SSE, sunucudan istemciye tek yönlü gerçek zamanlı veri akışı
// sağlar. Bu projede LLM yanıtları token token alınır (streaming).
//
// PLATFORM AYRIMI:
// • sse_client_io.dart: Mobil ve masaüstü platformlar için
// • sse_client_web.dart: Web platformu için
//
// KULLANIM:
// import 'package:selcukaiassistant/services/sse_client.dart';
// ════════════════════════════════════════════════════════════════════

export 'sse_client_io.dart' if (dart.library.html) 'sse_client_web.dart';
export 'sse_client_types.dart';
