import '../../../core/network/api_client.dart';
import '../domain/guard_models.dart';

/// Repository for RimaAI Guard detection and event history.
class GuardRepository {
  GuardRepository(this._api);

  final ApiClient _api;

  Future<GuardDetection> detect({
    required String cameraId,
    required String frameId,
  }) async {
    final json = await _api.postJson('/guard/detect', {
      'camera_id': cameraId,
      'frame_id': frameId,
    });
    return GuardDetection.fromJson(json as Map<String, dynamic>);
  }

  Future<List<GuardEvent>> events() async {
    final json = await _api.getJson('/guard/events');
    return (json as List)
        .map((e) => GuardEvent.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<CameraSettings> cameraSettings(String cameraId) async {
    final json =
        await _api.getJson('/guard/camera', query: {'camera_id': cameraId});
    return CameraSettings.fromJson(json as Map<String, dynamic>);
  }

  Future<CameraSettings> updateCameraSettings(CameraSettings settings) async {
    final json = await _api.putJson('/guard/camera', settings.toJson());
    return CameraSettings.fromJson(json as Map<String, dynamic>);
  }
}
