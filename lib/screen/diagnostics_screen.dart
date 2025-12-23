import 'dart:async';
import 'dart:convert';

import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:http/http.dart' as http;
import 'package:selcukaiassistant/config/backend_config.dart';
import 'package:selcukaiassistant/helper/pref.dart';
import 'package:selcukaiassistant/l10n/app_localizations.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';
import 'package:selcukaiassistant/model/model_info.dart';
import 'package:selcukaiassistant/services/model_service.dart';
import 'package:selcukaiassistant/services/sse_client.dart';

class DiagnosticsScreen extends StatefulWidget {
  const DiagnosticsScreen({super.key});

  @override
  State<DiagnosticsScreen> createState() => _DiagnosticsScreenState();
}

class _DiagnosticsScreenState extends State<DiagnosticsScreen> {
  final List<String> _logs = [];
  final ScrollController _logScrollController = ScrollController();

  List<ModelInfo> _models = [];
  bool _isLoadingModels = false;
  bool _isStreaming = false;
  String _streamSample = '';
  bool _isLoadingHf = false;
  Map<String, dynamic>? _hfInfo;
  String? _hfError;
  bool _isLoadingOllama = false;
  Map<String, dynamic>? _ollamaInfo;
  String? _ollamaError;
  int? _lastLatencyMs;
  String? _lastRequestLabel;
  int? _lastRequestStatus;
  String? _lastErrorDetails;
  String? _lastErrorTimestamp;
  int? _lastErrorStatus;
  String? _lastErrorBody;
  Map<String, String>? _lastErrorHeaders;

  @override
  void initState() {
    super.initState();
    unawaited(_loadModels());
    unawaited(_loadOllamaHealth());
    unawaited(_loadHfHealth());
  }

  @override
  void dispose() {
    _logScrollController.dispose();
    super.dispose();
  }

  Future<void> _loadModels() async {
    setState(() => _isLoadingModels = true);
    final models = await ModelService.fetchModels();
    if (!mounted) return;
    setState(() {
      _models = models;
      _isLoadingModels = false;
    });
  }

  Future<void> _loadOllamaHealth({bool log = false}) async {
    final url = Uri.parse('${BackendConfig.baseUrl}/health/ollama');
    setState(() => _isLoadingOllama = true);
    if (log) {
      _appendLog('GET /health/ollama -> start');
    }
    final stopwatch = Stopwatch()..start();
    try {
      final response = await http.get(url, headers: _headers()).timeout(
        const Duration(seconds: 12),
        onTimeout: () => http.Response('Timeout', 408),
      );
      stopwatch.stop();
      _updateLastRequest(
        'GET /health/ollama',
        response.statusCode,
        stopwatch.elapsedMilliseconds,
      );
      final body = utf8.decode(response.bodyBytes);
      if (response.statusCode == 200) {
        setState(() {
          _ollamaInfo = jsonDecode(body) as Map<String, dynamic>;
          _ollamaError = null;
        });
      } else {
        final snippet = _truncate(body);
        setState(() {
          _ollamaError = 'HTTP ${response.statusCode} $snippet';
          _ollamaInfo = null;
        });
        _recordError(
          'GET /health/ollama -> ${response.statusCode} $snippet',
          statusCode: response.statusCode,
          body: snippet,
          headers: response.headers,
        );
      }
      if (log) {
        _appendLog(
          'GET /health/ollama -> ${response.statusCode} ${_truncate(body)}',
        );
      }
    } on Exception catch (e) {
      stopwatch.stop();
      _updateLastRequest(
        'GET /health/ollama',
        null,
        stopwatch.elapsedMilliseconds,
      );
      setState(() {
        _ollamaError = e.toString();
        _ollamaInfo = null;
      });
      _recordError('GET /health/ollama -> $e');
      if (log) {
        _appendLog('GET /health/ollama -> error: $e');
      }
    } finally {
      if (mounted) {
        setState(() => _isLoadingOllama = false);
      }
    }
  }

  Future<void> _loadHfHealth({bool log = false}) async {
    final url = Uri.parse('${BackendConfig.baseUrl}/health/hf');
    setState(() => _isLoadingHf = true);
    if (log) {
      _appendLog('GET /health/hf -> start');
    }
    final stopwatch = Stopwatch()..start();
    try {
      final response = await http.get(url, headers: _headers()).timeout(
        const Duration(seconds: 12),
        onTimeout: () => http.Response('Timeout', 408),
      );
      stopwatch.stop();
      _updateLastRequest(
        'GET /health/hf',
        response.statusCode,
        stopwatch.elapsedMilliseconds,
      );
      final body = utf8.decode(response.bodyBytes);
      if (response.statusCode == 200) {
        setState(() {
          _hfInfo = jsonDecode(body) as Map<String, dynamic>;
          _hfError = null;
        });
      } else {
        final snippet = _truncate(body);
        setState(() {
          _hfError = 'HTTP ${response.statusCode} $snippet';
          _hfInfo = null;
        });
        _recordError(
          'GET /health/hf -> ${response.statusCode} $snippet',
          statusCode: response.statusCode,
          body: snippet,
          headers: response.headers,
        );
      }
      if (log) {
        _appendLog('GET /health/hf -> ${response.statusCode} ${_truncate(body)}');
      }
    } on Exception catch (e) {
      stopwatch.stop();
      _updateLastRequest(
        'GET /health/hf',
        null,
        stopwatch.elapsedMilliseconds,
      );
      setState(() {
        _hfError = e.toString();
        _hfInfo = null;
      });
      _recordError('GET /health/hf -> $e');
      if (log) {
        _appendLog('GET /health/hf -> error: $e');
      }
    } finally {
      if (mounted) {
        setState(() => _isLoadingHf = false);
      }
    }
  }

  Map<String, String> _headers() {
    final locale = Pref.localeCode ?? L10n.fallbackLocale.languageCode;
    return {
      'Content-Type': 'application/json; charset=utf-8',
      'Accept-Language': locale,
    };
  }

  Map<String, dynamic> _buildPayload({required bool stream}) {
    final l10n = L10n.current();
    return {
      'model': Pref.selectedModel,
      'messages': [
        {
          'role': 'user',
          'content': l10n?.diagnosticsTestMessage ?? 'Merhaba',
        },
      ],
      'temperature': 0.2,
      'top_p': 0.9,
      'max_tokens': 128,
      'stream': stream,
      'rag_enabled': Pref.ragEnabled,
      'rag_strict': Pref.ragStrict,
      'rag_top_k': Pref.ragTopK,
    };
  }

  void _appendLog(String message) {
    final timestamp = DateTime.now().toIso8601String();
    setState(() {
      _logs.add('[$timestamp] $message');
    });
    WidgetsBinding.instance.addPostFrameCallback((_) {
      if (_logScrollController.hasClients) {
        _logScrollController.jumpTo(
          _logScrollController.position.maxScrollExtent,
        );
      }
    });
  }

  void _updateLastRequest(
    String label,
    int? statusCode,
    int elapsedMs,
  ) {
    if (!mounted) return;
    setState(() {
      _lastRequestLabel = label;
      _lastRequestStatus = statusCode;
      _lastLatencyMs = elapsedMs;
    });
  }

  void _recordError(
    String details, {
    int? statusCode,
    String? body,
    Map<String, String>? headers,
  }) {
    setState(() {
      _lastErrorDetails = details;
      _lastErrorTimestamp = DateTime.now().toIso8601String();
      _lastErrorStatus = statusCode;
      _lastErrorBody = body;
      _lastErrorHeaders = headers;
    });
  }

  String _truncate(String value, {int maxLength = 500}) {
    if (value.length <= maxLength) return value;
    return '${value.substring(0, maxLength)}...';
  }

  Future<void> _runRequest(
    String label,
    Future<http.Response> Function() request,
  ) async {
    _appendLog('$label -> start');
    final stopwatch = Stopwatch()..start();
    try {
      final response = await request().timeout(
        const Duration(seconds: 12),
        onTimeout: () => http.Response('Timeout', 408),
      );
      stopwatch.stop();
      _updateLastRequest(
        label,
        response.statusCode,
        stopwatch.elapsedMilliseconds,
      );
      final body = utf8.decode(response.bodyBytes);
      final snippet = _truncate(body);
      _appendLog('$label -> ${response.statusCode} $snippet');
      if (response.statusCode < 200 || response.statusCode >= 300) {
        _recordError(
          '$label -> ${response.statusCode} $snippet',
          statusCode: response.statusCode,
          body: snippet,
          headers: response.headers,
        );
      }
    } on Exception catch (e) {
      stopwatch.stop();
      _updateLastRequest(label, null, stopwatch.elapsedMilliseconds);
      _appendLog('$label -> error: $e');
      _recordError('$label -> $e');
    }
  }

  Future<void> _testHealth() async {
    final url = Uri.parse('${BackendConfig.baseUrl}/health');
    await _runRequest(
      'GET /health',
      () => http.get(url, headers: _headers()),
    );
  }

  Future<void> _testModels() async {
    final url = Uri.parse(BackendConfig.modelsEndpoint);
    await _runRequest(
      'GET /models',
      () => http.get(url, headers: _headers()),
    );
  }

  Future<void> _testOllamaHealth() async {
    await _loadOllamaHealth(log: true);
  }

  Future<void> _testHfHealth() async {
    await _loadHfHealth(log: true);
  }

  Future<void> _testChat() async {
    final url = Uri.parse(BackendConfig.chatEndpoint);
    await _runRequest(
      'POST /chat',
      () => http.post(
        url,
        headers: _headers(),
        body: jsonEncode(_buildPayload(stream: false)),
      ),
    );
  }

  Future<void> _testStream() async {
    if (_isStreaming) return;
    setState(() => _isStreaming = true);
    _appendLog('POST /chat/stream -> start');

    ChatStreamSession? session;
    StreamSubscription<ChatStreamEvent>? subscription;
    final buffer = StringBuffer();
    var lines = 0;

    try {
      session = await SseClient().connect(
        url: Uri.parse(BackendConfig.chatStreamEndpoint),
        headers: _headers(),
        body: jsonEncode(_buildPayload(stream: true)),
      );

      final completer = Completer<void>();
      subscription = session.stream.listen(
        (event) {
          final payload = <String, dynamic>{
            'type': event.type,
            'request_id': event.requestId,
          };
          if (event.token != null) {
            payload['token'] = event.token;
          }
          if (event.message != null) {
            payload['message'] = event.message;
          }
          if (event.usage != null) {
            payload['usage'] = event.usage;
          }

          buffer.writeln('data: ${jsonEncode(payload)}');
          lines++;
          if (event.type == 'end' || event.type == 'error' || lines >= 12) {
            if (!completer.isCompleted) {
              completer.complete();
            }
          }
        },
        onError: (Object error) {
          if (!completer.isCompleted) {
            completer.completeError(error);
          }
        },
        onDone: () {
          if (!completer.isCompleted) {
            completer.complete();
          }
        },
      );

      await completer.future.timeout(
        const Duration(seconds: 15),
        onTimeout: () {
          _appendLog('POST /chat/stream -> timeout waiting for events');
          return;
        },
      );

      final sample = buffer.toString().trim();
      setState(() {
        _streamSample = sample.isEmpty
            ? (L10n.current()?.diagnosticsNoStreamSample ??
                'No stream events captured.')
            : sample;
      });
      _appendLog('POST /chat/stream -> captured $lines events');
    } on Exception catch (e) {
      _appendLog('POST /chat/stream -> error: $e');
      _recordError('POST /chat/stream -> $e');
    } finally {
      await subscription?.cancel();
      session?.close();
      if (mounted) {
        setState(() => _isStreaming = false);
      }
    }
  }

  ModelInfo? _selectedModelInfo() {
    final selected = Pref.selectedModel;
    if (selected == null || selected.isEmpty) {
      return null;
    }
    for (final model in _models) {
      if (model.id == selected) {
        return model;
      }
    }
    return null;
  }

  String _platformLabel() {
    if (kIsWeb) {
      return 'Web';
    }
    switch (defaultTargetPlatform) {
      case TargetPlatform.android:
        return 'Android';
      case TargetPlatform.iOS:
        return 'iOS';
      case TargetPlatform.macOS:
        return 'macOS';
      case TargetPlatform.windows:
        return 'Windows';
      case TargetPlatform.linux:
        return 'Linux';
      case TargetPlatform.fuchsia:
        return 'Fuchsia';
    }
  }

  String _formatHeaders(Map<String, String>? headers) {
    if (headers == null || headers.isEmpty) {
      return '-';
    }
    return headers.entries
        .map((entry) => '${entry.key}: ${entry.value}')
        .join('\n');
  }

  String _buildErrorDetails(AppLocalizations l10n) {
    final parts = <String>[];
    if (_lastErrorStatus != null) {
      parts.add('${l10n.diagnosticsErrorStatusLabel}: $_lastErrorStatus');
    }
    if (_lastErrorBody != null && _lastErrorBody!.isNotEmpty) {
      parts.add('${l10n.diagnosticsErrorBodyLabel}: $_lastErrorBody');
    }
    if (_lastErrorHeaders != null && _lastErrorHeaders!.isNotEmpty) {
      parts.add('${l10n.diagnosticsErrorHeadersLabel}:\n'
          '${_formatHeaders(_lastErrorHeaders)}');
    }
    return parts.join('\n');
  }

  String _backendSourceLabel(
    AppLocalizations l10n,
    BackendUrlSource source,
  ) {
    switch (source) {
      case BackendUrlSource.override:
        return l10n.diagnosticsSourceOverride;
      case BackendUrlSource.dartDefine:
        return l10n.diagnosticsSourceDartDefine;
      case BackendUrlSource.dotenv:
        return l10n.diagnosticsSourceDotenv;
      case BackendUrlSource.webRelease:
        return l10n.diagnosticsSourceWebRelease;
      case BackendUrlSource.webDev:
        return l10n.diagnosticsSourceWebDev;
      case BackendUrlSource.androidEmulator:
        return l10n.diagnosticsSourceAndroidEmulator;
      case BackendUrlSource.desktop:
        return l10n.diagnosticsSourceDesktop;
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = context.l10n;
    final selectedModel = _selectedModelInfo();
    final selectedLabel = selectedModel == null
        ? l10n.modelNotSelected
        : '${selectedModel.displayName} '
            '(${selectedModel.provider}: ${selectedModel.modelId})';
    final availabilityLabel = selectedModel == null
        ? l10n.diagnosticsModelUnavailable
        : (selectedModel.available
            ? l10n.diagnosticsModelAvailable
            : l10n.diagnosticsModelUnavailable);
    final availabilityReason = selectedModel != null &&
            !selectedModel.available &&
            selectedModel.reasonUnavailable.isNotEmpty
        ? l10n.modelUnavailableReason(selectedModel.reasonUnavailable)
        : null;
    final hfStatus = _hfInfo?['status'] as String?;
    final hfCuda = _hfInfo?['cuda_available'] as bool? ?? false;
    final hfReady = hfStatus == 'ok' && hfCuda;
    final hfLabel = hfReady
        ? l10n.diagnosticsHfReady
        : l10n.diagnosticsHfUnavailable;
    final hfDetail = _hfInfo == null
        ? _hfError
        : l10n.diagnosticsHfDetail(
            (_hfInfo?['gpu_name'] as String?) ?? '-',
            (_hfInfo?['torch_version'] as String?) ?? '-',
            (_hfInfo?['cuda_version'] as String?) ?? '-',
            (_hfInfo?['transformers_version'] as String?) ?? '-',
            (_hfInfo?['bitsandbytes_version'] as String?) ?? '-',
          );
    final resolution = BackendConfig.resolution;
    final sourceLabel = _backendSourceLabel(l10n, resolution.source);
    final baseUrlSubtitle =
        '${resolution.url}\n${l10n.diagnosticsBaseUrlSource(sourceLabel)}';
    final latencyLabel = _lastLatencyMs == null
        ? l10n.diagnosticsLatencyUnavailable
        : '$_lastLatencyMs ms'
            '${_lastRequestLabel == null ? '' : ' - ${_lastRequestLabel!}'}'
            '${_lastRequestStatus == null ? '' : ' ($_lastRequestStatus)'}';
    final ollamaStatus = _ollamaInfo?['status'] as String?;
    final ollamaAvailable =
        _ollamaInfo?['model_available'] as bool? ?? false;
    final ollamaModels =
        _ollamaInfo?['available_models'] as List<dynamic>? ?? const [];
    final ollamaReady = ollamaStatus == 'healthy';
    final ollamaLabel = ollamaReady
        ? l10n.diagnosticsOllamaReady
        : l10n.diagnosticsOllamaUnavailable;
    final ollamaDetail = _ollamaInfo == null
        ? _ollamaError
        : l10n.diagnosticsOllamaDetail(
            ollamaStatus ?? '-',
            (_ollamaInfo?['model'] as String?) ?? '-',
            ollamaAvailable ? l10n.modelAvailable : l10n.modelUnavailable,
            ollamaModels.length.toString(),
          );
    final errorDetails =
        _lastErrorDetails == null ? null : _buildErrorDetails(l10n);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.diagnosticsTitle),
        centerTitle: true,
      ),
      body: ListView(
        padding: const EdgeInsets.only(bottom: 24),
        children: [
          _buildSection(
            context,
            l10n.diagnosticsConnectionSection,
            [
              ListTile(
                title: Text(l10n.diagnosticsBaseUrlLabel),
                subtitle: Text(baseUrlSubtitle),
                leading: const Icon(Icons.link),
              ),
              ListTile(
                title: Text(l10n.diagnosticsPlatformLabel),
                subtitle: Text(_platformLabel()),
                leading: const Icon(Icons.devices),
              ),
              ListTile(
                title: Text(l10n.diagnosticsLatencyLabel),
                subtitle: Text(latencyLabel),
                leading: const Icon(Icons.speed),
              ),
              ListTile(
                title: Text(l10n.diagnosticsModelLabel),
                subtitle: availabilityReason == null
                    ? Text(selectedLabel)
                    : Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(selectedLabel),
                          Text(availabilityReason),
                        ],
                      ),
                trailing: _isLoadingModels
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Text(availabilityLabel),
                leading: const Icon(Icons.psychology),
              ),
              ListTile(
                title: Text(l10n.diagnosticsOllamaLabel),
                subtitle: ollamaDetail == null ? null : Text(ollamaDetail),
                trailing: _isLoadingOllama
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Text(ollamaLabel),
                leading: const Icon(Icons.storage),
              ),
              ListTile(
                title: Text(l10n.diagnosticsHfLabel),
                subtitle: hfDetail == null ? null : Text(hfDetail),
                trailing: _isLoadingHf
                    ? const SizedBox(
                        width: 16,
                        height: 16,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : Text(hfLabel),
                leading: const Icon(Icons.memory),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                child: Wrap(
                  spacing: 8,
                  runSpacing: 8,
                  children: [
                    ElevatedButton(
                      onPressed: _testHealth,
                      child: Text(l10n.diagnosticsHealthButton),
                    ),
                    ElevatedButton(
                      onPressed: _testModels,
                      child: Text(l10n.diagnosticsModelsButton),
                    ),
                    ElevatedButton(
                      onPressed: _testOllamaHealth,
                      child: Text(l10n.diagnosticsOllamaButton),
                    ),
                    ElevatedButton(
                      onPressed: _testHfHealth,
                      child: Text(l10n.diagnosticsHfButton),
                    ),
                    ElevatedButton(
                      onPressed: _testChat,
                      child: Text(l10n.diagnosticsChatButton),
                    ),
                    ElevatedButton(
                      onPressed: _isStreaming ? null : _testStream,
                      child: Text(
                        _isStreaming
                            ? l10n.diagnosticsStreamRunning
                            : l10n.diagnosticsStreamButton,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
          _buildSection(
            context,
            l10n.diagnosticsLastErrorTitle,
            [
              ListTile(
                title: Text(_lastErrorDetails ?? l10n.diagnosticsNoErrors),
                subtitle: _lastErrorTimestamp == null
                    ? null
                    : Text(_lastErrorTimestamp!),
                leading: Icon(
                  _lastErrorDetails == null ? Icons.check_circle : Icons.error,
                  color: _lastErrorDetails == null ? Colors.green : Colors.red,
                ),
              ),
              if (errorDetails != null && errorDetails.isNotEmpty)
                Padding(
                  padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
                  child: SelectableText(errorDetails),
                ),
            ],
          ),
          _buildSection(
            context,
            l10n.diagnosticsStreamSampleTitle,
            [
              Padding(
                padding: const EdgeInsets.all(16),
                child: SelectableText(
                  _streamSample.isEmpty
                      ? l10n.diagnosticsNoStreamSample
                      : _streamSample,
                ),
              ),
            ],
          ),
          _buildSection(
            context,
            l10n.diagnosticsLogsTitle,
            [
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
                child: Align(
                  alignment: Alignment.centerRight,
                  child: TextButton.icon(
                    onPressed: _logs.isEmpty
                        ? null
                        : () async {
                            final messenger = ScaffoldMessenger.of(context);
                            await Clipboard.setData(
                              ClipboardData(text: _logs.join('\n')),
                            );
                            if (!mounted) return;
                            messenger.showSnackBar(
                              SnackBar(content: Text(l10n.copiedToClipboard)),
                            );
                          },
                    icon: const Icon(Icons.copy),
                    label: Text(l10n.diagnosticsCopyLog),
                  ),
                ),
              ),
              SizedBox(
                height: 220,
                child: Card(
                  margin: const EdgeInsets.fromLTRB(16, 8, 16, 16),
                  child: Padding(
                    padding: const EdgeInsets.all(12),
                    child: Scrollbar(
                      controller: _logScrollController,
                      child: SingleChildScrollView(
                        controller: _logScrollController,
                        child: SelectableText(
                          _logs.isEmpty
                              ? l10n.diagnosticsNoLogs
                              : _logs.join('\n'),
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSection(
    BuildContext context,
    String title,
    List<Widget> children,
  ) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(16, 24, 16, 8),
          child: Text(
            title,
            style: TextStyle(
              fontSize: 14,
              fontWeight: FontWeight.w600,
              color: Theme.of(context).colorScheme.primary,
            ),
          ),
        ),
        ...children,
      ],
    );
  }
}
