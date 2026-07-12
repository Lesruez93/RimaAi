/// Result of a crop/livestock disease scan (device or server inference).
class ScanResult {
  const ScanResult({
    required this.label,
    required this.confidence,
    required this.advice,
    required this.scanType,
    required this.source,
    this.adviceI18n = const {},
  });

  final String label;
  final double confidence;
  final String advice;
  final String scanType;
  final String source;
  final Map<String, String> adviceI18n;

  /// A human-friendly title from the model's snake_case label.
  String get displayLabel => label
      .split('_')
      .map((w) => w.isEmpty ? w : '${w[0].toUpperCase()}${w.substring(1)}')
      .join(' ');

  factory ScanResult.fromJson(Map<String, dynamic> json) {
    return ScanResult(
      label: json['label'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      advice: json['advice'] as String,
      scanType: json['scan_type'] as String? ?? 'crop',
      source: json['source'] as String? ?? 'server',
      adviceI18n: (json['advice_i18n'] as Map?)?.map(
            (k, v) => MapEntry(k.toString(), v.toString()),
          ) ??
          const {},
    );
  }
}
