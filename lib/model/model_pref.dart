import 'package:hive/hive.dart';

const String defaultModelPreferenceId = 'default';

class ModelPreference extends HiveObject {
  ModelPreference({
    required this.id,
    this.selectedModelId,
    DateTime? updatedAt,
  }) : updatedAt = updatedAt ?? DateTime.now();

  String id;
  String? selectedModelId;
  DateTime updatedAt;
}

class ModelPreferenceAdapter extends TypeAdapter<ModelPreference> {
  @override
  final int typeId = 2;

  @override
  ModelPreference read(BinaryReader reader) {
    final numOfFields = reader.readByte();
    final fields = <int, dynamic>{
      for (int i = 0; i < numOfFields; i++) reader.readByte(): reader.read(),
    };

    return ModelPreference(
      id: fields[0] as String,
      selectedModelId: fields[1] as String?,
      updatedAt: fields[2] as DateTime?,
    );
  }

  @override
  void write(BinaryWriter writer, ModelPreference obj) {
    writer
      ..writeByte(3)
      ..writeByte(0)
      ..write(obj.id)
      ..writeByte(1)
      ..write(obj.selectedModelId)
      ..writeByte(2)
      ..write(obj.updatedAt);
  }
}
