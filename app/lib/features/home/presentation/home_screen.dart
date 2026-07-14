import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/l10n/app_strings.dart';
import '../../../core/l10n/locale_controller.dart';
import '../../../core/network/api_client.dart';
import '../../../core/session/farmer_session.dart';
import '../../../core/theme/app_colors.dart';
import '../../../shared/widgets/info_card.dart';
import '../../alerts/presentation/alerts_screen.dart';
import '../../guard/presentation/guard_screen.dart';
import '../../livestock/presentation/livestock_screen.dart';
import '../../scan/presentation/scan_screen.dart';
import '../data/forecast_repository.dart';

/// The dashboard: greeting, seasonal forecast, and feature entry cards.
class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  final _forecastRepo = ForecastRepository(ApiClient());
  Forecast? _forecast;

  @override
  void didChangeDependencies() {
    super.didChangeDependencies();
    _loadForecast();
  }

  Future<void> _loadForecast() async {
    final region = context.read<FarmerSession>().region ??
        AppConstants.zimbabweDistricts.first;
    try {
      final f = await _forecastRepo.forecast(region);
      if (mounted) setState(() => _forecast = f);
    } catch (_) {
      /* offline: hide forecast card */
    }
  }

  void _open(Widget screen) => Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => screen),
      );

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(
        title: Text(s.t('appName')),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            tooltip: s.t('alerts'),
            onPressed: () => _open(const AlertsScreen()),
          ),
          PopupMenuButton<String>(
            icon: const Icon(Icons.language),
            onSelected: (code) =>
                context.read<LocaleController>().setLanguage(code),
            itemBuilder: (context) => AppStrings.supportedLanguages.entries
                .map((e) => PopupMenuItem(value: e.key, child: Text(e.value)))
                .toList(),
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(s.t('tagline'), style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 16),
          if (_forecast != null) _ForecastCard(forecast: _forecast!),
          const SizedBox(height: 8),
          InfoCard(
            title: s.t('scanCrop'),
            description: 'Identify crop disease from a photo, offline',
            icon: Icons.center_focus_strong_outlined,
            onTap: () => _open(const ScanScreen(scanType: 'crop')),
          ),
          InfoCard(
            title: s.t('livestock'),
            description: 'Health check + symptom triage for your animals',
            icon: Icons.pets_outlined,
            onTap: () => _open(const LivestockScreen()),
          ),
          InfoCard(
            title: s.t('guard'),
            description: 'RimaAI Guard — camera intrusion alerts (commercial)',
            icon: Icons.videocam_outlined,
            color: AppColors.accent,
            onTap: () => _open(const GuardScreen()),
          ),
        ],
      ),
    );
  }
}

class _ForecastCard extends StatelessWidget {
  const _ForecastCard({required this.forecast});
  final Forecast forecast;

  @override
  Widget build(BuildContext context) {
    return Card(
      color: Theme.of(context).colorScheme.primaryContainer,
      child: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Icon(Icons.wb_sunny_outlined),
                const SizedBox(width: 8),
                Text('${forecast.regionName} — planting window',
                    style: Theme.of(context).textTheme.titleMedium),
              ],
            ),
            const SizedBox(height: 8),
            Text(forecast.plantingWindow,
                style: Theme.of(context).textTheme.headlineSmall),
            Text(
              'Expected rain: ${forecast.expectedRainfallMm.round()} mm '
              '(${forecast.confidence} confidence)',
              style: Theme.of(context).textTheme.bodySmall,
            ),
            const SizedBox(height: 8),
            Text(forecast.advice),
          ],
        ),
      ),
    );
  }
}
