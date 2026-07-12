import 'package:flutter/material.dart';

/// RimaAI brand palette. Greens evoke farming/growth; amber/red carry the
/// outbreak risk semantics used across the heat map and alert badges.
abstract final class AppColors {
  // Brand palette sampled from the RimaAI badge logo.
  static const Color primary = Color(0xFF18532E); // deep badge green
  static const Color primaryDark = Color(0xFF0E3D21);
  static const Color primaryLight = Color(0xFF2E8B4E);
  static const Color leaf = Color(0xFF73A64B); // maize-leaf green
  static const Color blue = Color(0xFF136A90); // badge blue half
  static const Color accent = Color(0xFFC5A763); // badge gold ring
  static const Color surface = Color(0xFFF4F6F1);
  static const Color surfaceDark = Color(0xFF0E140F);

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
