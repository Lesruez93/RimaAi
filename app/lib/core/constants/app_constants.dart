import 'package:flutter/material.dart';

import '../theme/app_colors.dart';

/// App-wide constants: alert categories, outbreak types and their display meta.
abstract final class AppConstants {
  /// Subscription categories (must match backend `ALERT_CATEGORIES`).
  static const alertCategories = <AlertCategory>[
    AlertCategory('weather', 'Weather alerts', Icons.cloud_outlined),
    AlertCategory(
        'disease', 'Disease outbreak alerts', Icons.coronavirus_outlined),
    AlertCategory('tips', 'Farming tips', Icons.tips_and_updates_outlined),
    AlertCategory('livestock', 'Livestock tips', Icons.pets_outlined),
    AlertCategory('insurance', 'Insurance tips', Icons.verified_user_outlined),
  ];

  /// Outbreak types (must match backend `OUTBREAK_TYPES`).
  static const outbreakTypes = <OutbreakType>[
    OutbreakType('crop_disease', 'Crop disease', Icons.grass_outlined),
    OutbreakType('armyworm', 'Fall armyworm', Icons.bug_report_outlined),
    OutbreakType('locusts', 'Locusts', Icons.grain),
    OutbreakType(
        'tick_disease', 'Tick / January disease', Icons.pest_control_outlined),
    OutbreakType('flood', 'Flood', Icons.water_outlined),
  ];

  static const zimbabweDistricts = <String>[
    'Harare',
    'Bulawayo',
    'Mutare',
    'Masvingo',
    'Gweru',
    'Gokwe',
    'Chinhoyi',
    'Marondera',
  ];

  /// Map a backend risk level to its display colour.
  static Color riskColor(String level) => switch (level) {
        'high' => AppColors.riskHigh,
        'moderate' => AppColors.riskModerate,
        _ => AppColors.riskLow,
      };

  /// Map a triage urgency to its display colour.
  static Color urgencyColor(String urgency) => switch (urgency) {
        'emergency' => AppColors.urgencyEmergency,
        'high' => AppColors.urgencyHigh,
        'medium' => AppColors.urgencyMedium,
        _ => AppColors.urgencyLow,
      };
}

/// A subscribable alert category with display metadata.
class AlertCategory {
  const AlertCategory(this.id, this.label, this.icon);
  final String id;
  final String label;
  final IconData icon;
}

/// A reportable outbreak type with display metadata.
class OutbreakType {
  const OutbreakType(this.id, this.label, this.icon);
  final String id;
  final String label;
  final IconData icon;
}
