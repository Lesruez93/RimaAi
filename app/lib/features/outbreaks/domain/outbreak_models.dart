/// Aggregated per-district risk for one outbreak type (drives the heat map).
class DistrictRisk {
  const DistrictRisk({
    required this.regionName,
    required this.outbreakType,
    required this.score,
    required this.level,
    required this.reportCount,
    required this.latitude,
    required this.longitude,
  });

  final String regionName;
  final String outbreakType;
  final double score;
  final String level; // low | moderate | high
  final int reportCount;
  final double latitude;
  final double longitude;

  factory DistrictRisk.fromJson(Map<String, dynamic> json) {
    return DistrictRisk(
      regionName: json['region_name'] as String,
      outbreakType: json['outbreak_type'] as String,
      score: (json['score'] as num).toDouble(),
      level: json['level'] as String,
      reportCount: json['report_count'] as int? ?? 0,
      latitude: (json['latitude'] as num?)?.toDouble() ?? 0,
      longitude: (json['longitude'] as num?)?.toDouble() ?? 0,
    );
  }
}

/// Outcome of submitting a community outbreak report.
class OutbreakReportResult {
  const OutbreakReportResult({
    required this.riskLevel,
    required this.alertDispatched,
    required this.alertRecipients,
  });

  final String riskLevel;
  final bool alertDispatched;
  final int alertRecipients;

  factory OutbreakReportResult.fromJson(Map<String, dynamic> json) {
    final risk = json['risk'] as Map<String, dynamic>;
    return OutbreakReportResult(
      riskLevel: risk['level'] as String,
      alertDispatched: json['alert_dispatched'] as bool? ?? false,
      alertRecipients: json['alert_recipients'] as int? ?? 0,
    );
  }
}
