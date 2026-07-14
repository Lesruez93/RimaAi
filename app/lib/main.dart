import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import 'core/l10n/locale_controller.dart';
import 'core/session/farmer_session.dart';
import 'core/theme/app_theme.dart';
import 'features/auth/presentation/onboarding_screen.dart';
import 'features/home/presentation/app_shell.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();

  final localeController = LocaleController();
  final session = FarmerSession();
  await Future.wait([localeController.load(), session.load()]);

  final prefs = await SharedPreferences.getInstance();
  final onboarded = prefs.getBool(OnboardingScreen.onboardedKey) ?? false;

  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider.value(value: localeController),
        ChangeNotifierProvider.value(value: session),
      ],
      child: RimaAiApp(onboarded: onboarded),
    ),
  );
}

/// Root application widget.
class RimaAiApp extends StatelessWidget {
  const RimaAiApp({super.key, required this.onboarded});

  final bool onboarded;

  @override
  Widget build(BuildContext context) {
    final locale = context.watch<LocaleController>().locale;
    return MaterialApp(
      title: 'RimaAI',
      debugShowCheckedModeBanner: false,
      theme: AppTheme.light,
      darkTheme: AppTheme.dark,
      locale: locale,
      supportedLocales: const [Locale('en'), Locale('sn'), Locale('nd')],
      home: onboarded ? const AppShell() : const OnboardingScreen(),
    );
  }
}
