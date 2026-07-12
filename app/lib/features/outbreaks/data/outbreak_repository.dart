import '../../../core/network/api_client.dart';
import '../domain/outbreak_models.dart';

/// Repository for community outbreak reporting and the risk heat map.
class OutbreakRepository {
  OutbreakRepository(this._api);

  final ApiClient _api;

  /// Fetch aggregated district risk, optionally filtered by outbreak type.
  Future<List<DistrictRisk>> map({String? outbreakType}) async {
    final json = await _api.getJson(
      '/outbreaks/map',
      query: outbreakType == null ? null : {'outbreak_type': outbreakType},
    );
    return (json as List)
        .map((e) => DistrictRisk.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  /// Submit a community outbreak report.
  Future<OutbreakReportResult> report({
    required String regionName,
    required String outbreakType,
    String? description,
    int? farmerId,
  }) async {
    final json = await _api.postJson('/outbreaks/report', {
      'region_name': regionName,
      'outbreak_type': outbreakType,
      'description': description,
      'farmer_id': farmerId,
    });
    return OutbreakReportResult.fromJson(json as Map<String, dynamic>);
  }
}
