import 'package:flutter/material.dart';

import '../../../core/l10n/app_strings.dart';
import '../../../core/theme/app_colors.dart';
import '../../livestock/presentation/livestock_screen.dart';
import '../../outbreaks/presentation/outbreak_map_screen.dart';
import '../../scan/presentation/scan_screen.dart';
import 'home_screen.dart';

/// The main navigation shell: a notched bottom bar with the crop-scan action
/// docked as a centre FAB. Alerts live in each tab's app bar instead of
/// taking a bottom-bar slot; the Guard (commercial) flow is reached from Home.
class AppShell extends StatefulWidget {
  const AppShell({super.key});

  @override
  State<AppShell> createState() => _AppShellState();
}

class _AppShellState extends State<AppShell> {
  int _index = 0;

  static const _tabs = <Widget>[
    HomeScreen(),
    LivestockScreen(),
    OutbreakMapScreen(),
  ];

  void _openScan() => Navigator.of(context).push(
        MaterialPageRoute(builder: (_) => const ScanScreen(scanType: 'crop')),
      );

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      body: IndexedStack(index: _index, children: _tabs),
      floatingActionButtonLocation: FloatingActionButtonLocation.centerDocked,
      floatingActionButton: FloatingActionButton(
        onPressed: _openScan,
        tooltip: s.t('scan'),
        elevation: 4,
        backgroundColor: AppColors.primary,
        shape: const CircleBorder(),
        child: const Icon(Icons.center_focus_strong, color: Colors.white),
      ),
      bottomNavigationBar: BottomAppBar(
        shape: const CircularNotchedRectangle(),
        notchMargin: 8,
        elevation: 8,
        padding: EdgeInsets.zero,
        child: SizedBox(
          height: 64,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              _NavItem(
                icon: Icons.home_outlined,
                selectedIcon: Icons.home,
                label: s.t('home'),
                selected: _index == 0,
                onTap: () => setState(() => _index = 0),
              ),
              _NavItem(
                icon: Icons.pets_outlined,
                selectedIcon: Icons.pets,
                label: s.t('livestock'),
                selected: _index == 1,
                onTap: () => setState(() => _index = 1),
              ),
              const SizedBox(width: 56), // notch clearance for the FAB
              _NavItem(
                icon: Icons.map_outlined,
                selectedIcon: Icons.map,
                label: s.t('outbreakMap'),
                selected: _index == 2,
                onTap: () => setState(() => _index = 2),
              ),
              const SizedBox(width: 12),
            ],
          ),
        ),
      ),
    );
  }
}

class _NavItem extends StatelessWidget {
  const _NavItem({
    required this.icon,
    required this.selectedIcon,
    required this.label,
    required this.selected,
    required this.onTap,
  });

  final IconData icon;
  final IconData selectedIcon;
  final String label;
  final bool selected;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = selected ? AppColors.primary : Colors.grey.shade600;
    return Expanded(
      child: InkWell(
        onTap: onTap,
        customBorder: const StadiumBorder(),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(selected ? selectedIcon : icon, color: color, size: 24),
            const SizedBox(height: 2),
            Text(
              label,
              style: TextStyle(
                color: color,
                fontSize: 11,
                fontWeight: selected ? FontWeight.w600 : FontWeight.w400,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
