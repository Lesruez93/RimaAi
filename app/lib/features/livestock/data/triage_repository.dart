import '../../../core/network/api_client.dart';
import '../domain/triage_result.dart';

/// Repository for the livestock symptom triage endpoint (`POST /triage`).
class TriageRepository {
  TriageRepository(this._api);

  final ApiClient _api;

  Future<TriageResult> triage(
    String message, {
    String animal = 'cattle',
    String language = 'en',
  }) async {
    final json = await _api.postJson('/triage', {
      'message': message,
      'animal': animal,
      'language': language,
    });
    return TriageResult.fromJson(json as Map<String, dynamic>);
  }
}
