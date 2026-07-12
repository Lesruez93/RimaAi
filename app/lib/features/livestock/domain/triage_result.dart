/// Result of a livestock symptom triage request.
class TriageResult {
  const TriageResult({
    required this.condition,
    required this.urgency,
    required this.advice,
    required this.escalation,
    required this.backend,
    required this.disclaimer,
  });

  final String condition;
  final String urgency; // low | medium | high | emergency
  final String advice;
  final String escalation;
  final String backend; // rule | llm
  final String disclaimer;

  factory TriageResult.fromJson(Map<String, dynamic> json) {
    return TriageResult(
      condition: json['condition'] as String,
      urgency: json['urgency'] as String,
      advice: json['advice'] as String,
      escalation: json['escalation'] as String,
      backend: json['backend'] as String? ?? 'rule',
      disclaimer: json['disclaimer'] as String? ?? '',
    );
  }
}
