import 'package:flutter/material.dart';

/// RimaAI brand palette. Greens evoke farming/growth; amber/red carry the
/// outbreak risk semantics used across the heat map and alert badges.
abstract final class AppColors {
  static const Color primary = Color(0xFF2E7D32); // rima green
  static const Color primaryDark = Color(0xFF1B5E20);
  static const Color primaryLight = Color(0xFF66BB6A);
  static const Color accent = Color(0xFFF9A825); // maize/amber
  static const Color surface = Color(0xFFF6F8F6);
  static const Color surfaceDark = Color(0xFF121712);

  // Risk levels — shared by the map, badges and alert cards.
  static const Color riskLow = Color(0xFF43A047); // 🟢
  static const Color riskModerate = Color(0xFFF9A825); // 🟡
  static const Color riskHigh = Color(0xFFE53935); // 🔴

  // Urgency (livestock triage).
  static const Color urgencyEmergency = Color(0xFFD32F2F);
  static const Color urgencyHigh = Color(0xFFF4511E);
  static const Color urgencyMedium = Color(0xFFF9A825);
  static const Color urgencyLow = Color(0xFF43A047);
}
