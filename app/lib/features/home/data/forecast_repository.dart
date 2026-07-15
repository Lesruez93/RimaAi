import '../../../core/network/api_client.dart';

/// Planting-window / rainfall forecast for a region (`GET /forecast`).
class ForecastRepository {
  ForecastRepository(this._api);

  final ApiClient _api;

  Future<Forecast> forecast(String regionName) async {
    final json =
        await _api.getJson('/forecast', query: {'region_name': regionName});
    return Forecast.fromJson(json as Map<String, dynamic>);
  }
}

/// Seeded planting-window guidance.
class Forecast {
  const Forecast({
    required this.regionName,
    required this.plantingWindow,
    required this.expectedRainfallMm,
    required this.confidence,
    required this.advice,
  });

  final String regionName;
  final String plantingWindow;
  final double expectedRainfallMm;
  final String confidence;
  final String advice;

  factory Forecast.fromJson(Map<String, dynamic> json) {
    return Forecast(
      regionName: json['region_name'] as String,
      plantingWindow: json['planting_window'] as String,
      expectedRainfallMm: (json['expected_rainfall_mm'] as num).toDouble(),
      confidence: json['confidence'] as String,
      advice: json['advice'] as String,
    );
  }
}
