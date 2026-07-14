import 'package:flutter/material.dart';

import '../../core/constants/app_constants.dart';

/// A small coloured pill showing a risk level (low / moderate / high).
class RiskBadge extends StatelessWidget {
  const RiskBadge({super.key, required this.level});

  final String level;

  @override
  Widget build(BuildContext context) {
    final color = AppConstants.riskColor(level);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color),
      ),
      child: Text(
        level.toUpperCase(),
        style: TextStyle(
          color: color,
          fontWeight: FontWeight.w700,
          fontSize: 12,
          letterSpacing: 0.5,
        ),
      ),
    );
  }
}
