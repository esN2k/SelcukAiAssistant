class ModelInfo {
  ModelInfo({
    required this.id,
    required this.provider,
    required this.modelId,
    required this.displayName,
    required this.isDefault,
  });

  factory ModelInfo.fromJson(Map<String, dynamic> json) {
    return ModelInfo(
      id: json['id'] as String? ?? '',
      provider: json['provider'] as String? ?? '',
      modelId: json['model_id'] as String? ?? '',
      displayName: json['display_name'] as String? ?? '',
      isDefault: json['is_default'] as bool? ?? false,
    );
  }

  final String id;
  final String provider;
  final String modelId;
  final String displayName;
  final bool isDefault;
}
