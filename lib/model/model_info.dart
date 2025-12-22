class ModelInfo {
  ModelInfo({
    required this.id,
    required this.provider,
    required this.modelId,
    required this.displayName,
    required this.isDefault,
    required this.localOrRemote,
    required this.requiresApiKey,
    required this.available,
    required this.reasonUnavailable,
    required this.contextLength,
    required this.tags,
    required this.notes,
  });

  factory ModelInfo.fromJson(Map<String, dynamic> json) {
    return ModelInfo(
      id: json['id'] as String? ?? '',
      provider: json['provider'] as String? ?? '',
      modelId: json['model_id'] as String? ?? '',
      displayName: json['display_name'] as String? ?? '',
      isDefault: json['is_default'] as bool? ?? false,
      localOrRemote: json['local_or_remote'] as String? ?? '',
      requiresApiKey: json['requires_api_key'] as bool? ?? false,
      available: json['available'] as bool? ?? false,
      reasonUnavailable: json['reason_unavailable'] as String? ?? '',
      contextLength: json['context_length'] as int?,
      tags: (json['tags'] as List<dynamic>?)
              ?.map((tag) => tag.toString())
              .toList() ??
          const [],
      notes: json['notes'] as String? ?? '',
    );
  }

  final String id;
  final String provider;
  final String modelId;
  final String displayName;
  final bool isDefault;
  final String localOrRemote;
  final bool requiresApiKey;
  final bool available;
  final String reasonUnavailable;
  final int? contextLength;
  final List<String> tags;
  final String notes;

  bool get isLocal => localOrRemote == 'local';
  bool get isRemote => localOrRemote == 'remote';
}
