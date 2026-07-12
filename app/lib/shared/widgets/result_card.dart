import 'package:flutter/material.dart';

/// Displays a classification/triage result: a title, confidence bar, advice
/// body and an always-present human-oversight footer.
class ResultCard extends StatelessWidget {
  const ResultCard({
    super.key,
    required this.title,
    required this.advice,
    this.confidence,
    this.badge,
    this.footer,
    this.accentColor,
  });

  final String title;
  final String advice;

  /// Confidence in [0, 1]; renders a labelled progress bar when provided.
  final double? confidence;

  /// Optional badge widget (e.g. urgency or risk pill) shown by the title.
  final Widget? badge;

  /// Optional footer (defaults to nothing); scan/triage pass the vet disclaimer.
  final String? footer;
  final Color? accentColor;

  @override
  Widget build(BuildContext context) {
    final scheme = Theme.of(context).colorScheme;
    final accent = accentColor ?? scheme.primary;
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(18),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                Expanded(
                  child: Text(
                    title,
                    style: Theme.of(context)
                        .textTheme
                        .titleLarge
                        ?.copyWith(fontWeight: FontWeight.w700),
                  ),
                ),
                if (badge != null) badge!,
              ],
            ),
            if (confidence != null) ...[
              const SizedBox(height: 12),
              Row(
                children: [
                  Expanded(
                    child: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: LinearProgressIndicator(
                        value: confidence!.clamp(0, 1),
                        minHeight: 8,
                        color: accent,
                        backgroundColor: accent.withValues(alpha: 0.15),
                      ),
                    ),
                  ),
                  const SizedBox(width: 10),
                  Text('${(confidence! * 100).round()}%'),
                ],
              ),
            ],
            const SizedBox(height: 14),
            Text(advice, style: Theme.of(context).textTheme.bodyLarge),
            if (footer != null) ...[
              const SizedBox(height: 14),
              Container(
                padding: const EdgeInsets.all(12),
                decoration: BoxDecoration(
                  color: scheme.secondaryContainer.withValues(alpha: 0.5),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.info_outline, size: 18),
                    const SizedBox(width: 8),
                    Expanded(
                      child: Text(
                        footer!,
                        style: Theme.of(context).textTheme.bodySmall,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
