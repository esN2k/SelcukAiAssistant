import 'package:flutter/material.dart';
import 'package:get/get.dart';
import 'package:image_picker/image_picker.dart';
import 'package:selcukaiassistant/l10n/l10n.dart';

class ImagePickerService {
  static final ImagePicker _picker = ImagePicker();

  static Future<XFile?> pickImage({
    required ImageSource source,
  }) async {
    final l10n = L10n.current();
    try {
      final image = await _picker.pickImage(
        source: source,
        maxWidth: 1920,
        maxHeight: 1920,
        imageQuality: 85,
      );

      return image;
    } on Exception catch (e) {
      Get.snackbar(
        l10n?.imagePickerErrorTitle ?? 'Error',
        l10n?.imagePickerErrorMessage(e.toString()) ??
            'Failed to pick image: $e',
        backgroundColor: Colors.red,
        colorText: Colors.white,
        snackPosition: SnackPosition.BOTTOM,
      );
      return null;
    }
  }

  static Future<XFile?> showImageSourceDialog() async {
    final l10n = L10n.current();
    final source = await Get.dialog<ImageSource>(
      AlertDialog(
        title: Text(l10n?.chooseImageSourceTitle ?? 'Choose image source'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            ListTile(
              leading: const Icon(Icons.camera_alt),
              title: Text(l10n?.cameraLabel ?? 'Camera'),
              onTap: () => Get.back(result: ImageSource.camera),
            ),
            ListTile(
              leading: const Icon(Icons.photo_library),
              title: Text(l10n?.galleryLabel ?? 'Gallery'),
              onTap: () => Get.back(result: ImageSource.gallery),
            ),
          ],
        ),
      ),
    );

    if (source != null) {
      return pickImage(source: source);
    }
    return null;
  }
}
