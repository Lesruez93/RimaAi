import 'package:flutter/material.dart';

import 'app_colors.dart';

/// Central Material 3 theme for RimaAI (light + dark).
abstract final class AppTheme {
  static ThemeData get light {
    final scheme = ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      primary: AppColors.primary,
      secondary: AppColors.accent,
    );
    return _base(scheme, AppColors.surface);
  }

  static ThemeData get dark {
    final scheme = ColorScheme.fromSeed(
      seedColor: AppColors.primary,
      brightness: Brightness.dark,
      primary: AppColors.primaryLight,
      secondary: AppColors.accent,
    );
    return _base(scheme, AppColors.surfaceDark);
  }

  static ThemeData _base(ColorScheme scheme, Color scaffold) {
    // Note: only the color scheme and button theme are overridden here.
    // AppBar/Card/InputDecoration theming is left to the Material 3 defaults so
    // the code stays portable across Flutter versions (their theme-data classes
    // were renamed in 3.29); component styling is applied at the widget level.
    return ThemeData(
      useMaterial3: true,
      colorScheme: scheme,
      scaffoldBackgroundColor: scaffold,
      filledButtonTheme: FilledButtonThemeData(
        style: FilledButton.styleFrom(
          minimumSize: const Size.fromHeight(52),
          shape: RoundedRectangleBorder(
            borderRadius: BorderRadius.circular(14),
          ),
        ),
      ),
    );
  }
}
