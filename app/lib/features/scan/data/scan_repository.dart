import 'dart:io';

import '../../../core/network/api_client.dart';
import '../domain/scan_result.dart';

/// Repository for disease scanning.
///
/// The production app runs a quantized MobileNetV3 TFLite model *on-device* for
/// offline scans; this repository is the network fallback (`POST /scan`) for
/// devices that cannot run TFLite. The on-device path would implement the same
/// [ScanResult] contract, so callers are agnostic to where inference ran.
class ScanRepository {
  ScanRepository(this._api);

  final ApiClient _api;

  /// Classify [image] server-side and return advice in [language].
  Future<ScanResult> scanImage(
    File image, {
    String scanType = 'crop',
    String language = 'en',
    int? farmerId,
  }) async {
    final json = await _api.uploadImage(
      '/scan',
      image,
      fields: {
        'scan_type': scanType,
        'language': language,
        if (farmerId != null) 'farmer_id': '$farmerId',
      },
    );
    return ScanResult.fromJson(json as Map<String, dynamic>);
  }
}
