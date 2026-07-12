import 'package:flutter/material.dart';

import '../../../core/l10n/app_strings.dart';
import '../../alerts/presentation/alerts_screen.dart';
import '../../livestock/presentation/livestock_screen.dart';
import '../../outbreaks/presentation/outbreak_map_screen.dart';
import '../../scan/presentation/scan_screen.dart';
import 'home_screen.dart';

/// The main navigation shell with a bottom navigation bar.
///
/// Each tab hosts a self-contained feature screen; the Guard (commercial) and
/// photo-capture flows are reached from within their parent tabs.
class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  static const _tabs = <Widget>[
    HomeScreen(),
    ScanScreen(scanType: 'crop'),
    LivestockScreen(),
    AlertsScreen(),
    OutbreakMapScreen(),
  ];

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      body: IndexedStack(index: _index, children: _tabs),
      bottomNavigationBar: NavigationBar(
        selectedIndex: _index,
        onDestinationSelected: (i) => setState(() => _index = i),
        destinations: [
          NavigationDestination(
            icon: const Icon(Icons.home_outlined),
            selectedIcon: const Icon(Icons.home),
            label: s.t('home'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.center_focus_strong_outlined),
            selectedIcon: const Icon(Icons.center_focus_strong),
            label: s.t('scan'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.pets_outlined),
            selectedIcon: const Icon(Icons.pets),
            label: s.t('livestock'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.notifications_outlined),
            selectedIcon: const Icon(Icons.notifications),
            label: s.t('alerts'),
          ),
          NavigationDestination(
            icon: const Icon(Icons.map_outlined),
            selectedIcon: const Icon(Icons.map),
            label: s.t('outbreakMap'),
          ),
        ],
      ),
    );
  }
}
