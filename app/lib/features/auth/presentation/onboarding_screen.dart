import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../../../core/l10n/app_strings.dart';
import '../../../core/l10n/locale_controller.dart';
import '../../../shared/widgets/language_selector.dart';
import '../../../shared/widgets/primary_button.dart';
import '../../home/presentation/app_shell.dart';

/// First-run onboarding: brand intro + language selection.
class OnboardingScreen extends StatefulWidget {
  const OnboardingScreen({super.key});

  static const onboardedKey = 'rimaai.onboarded';

  @override
  State<OnboardingScreen> createState() => _OnboardingScreenState();
}

class _OnboardingScreenState extends State<OnboardingScreen> {
  Future<void> _continue() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(OnboardingScreen.onboardedKey, true);
    if (!mounted) return;
    Navigator.of(context).pushReplacement(
      MaterialPageRoute(builder: (_) => const AppShell()),
    );
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    final selected = context.watch<LocaleController>().locale.languageCode;
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(24),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: 24),
              Image.asset(
                'assets/images/logo.png',
                width: 128,
                height: 128,
                errorBuilder: (context, error, stackTrace) => Icon(
                  Icons.eco,
                  size: 72,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
              const SizedBox(height: 12),
              Text(
                s.t('appName'),
                textAlign: TextAlign.center,
                style: Theme.of(context)
                    .textTheme
                    .displaySmall
                    ?.copyWith(fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              Text(s.t('tagline'), textAlign: TextAlign.center),
              const SizedBox(height: 36),
              Text(s.t('chooseLanguage'),
                  style: Theme.of(context).textTheme.titleMedium),
              const SizedBox(height: 12),
              LanguageSelector(
                selected: selected,
                onSelected: (code) =>
                    context.read<LocaleController>().setLanguage(code),
              ),
              const Spacer(),
              PrimaryButton(
                label: s.t('getStarted'),
                icon: Icons.arrow_forward,
                onPressed: _continue,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
