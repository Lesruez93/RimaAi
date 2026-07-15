import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../../../shared/widgets/risk_badge.dart';
import '../data/outbreak_repository.dart';
import '../domain/outbreak_models.dart';
import 'report_outbreak_screen.dart';

/// Zimbabwe outbreak heat map: coloured district markers by risk level, with an
/// outbreak-type filter and a "Report outbreak" entry point.
class OutbreakMapScreen extends StatefulWidget {
  const OutbreakMapScreen({super.key});

  @override
  State<OutbreakMapScreen> createState() => _OutbreakMapScreenState();
}

class _OutbreakMapScreenState extends State<OutbreakMapScreen> {
  final _repo = OutbreakRepository(ApiClient());

  static const _zimCenter = LatLng(-19.0, 29.7);

  String? _typeFilter;
  List<DistrictRisk> _risks = [];
  bool _loading = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final risks = await _repo.map(outbreakType: _typeFilter);
      setState(() {
        _risks =
            risks.where((r) => r.latitude != 0 || r.longitude != 0).toList();
        _loading = false;
      });
    } catch (_) {
      setState(() {
        _error = 'Could not load the outbreak map. Is the backend running?';
        _loading = false;
      });
    }
  }

  Future<void> _openReport() async {
    final changed = await Navigator.of(context).push<bool>(
      MaterialPageRoute(builder: (_) => const ReportOutbreakScreen()),
    );
    if (changed == true) _load();
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(s.t('outbreakMap'))),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: _openReport,
        icon: const Icon(Icons.add_alert_outlined),
        label: Text(s.t('reportOutbreak')),
      ),
      body: Column(
        children: [
          _TypeFilterBar(
            selected: _typeFilter,
            onChanged: (value) {
              setState(() => _typeFilter = value);
              _load();
            },
          ),
          Expanded(
            child: Stack(
              children: [
                FlutterMap(
                  options: const MapOptions(
                    initialCenter: _zimCenter,
                    initialZoom: 5.6,
                    minZoom: 4,
                    maxZoom: 12,
                  ),
                  children: [
                    TileLayer(
                      urlTemplate:
                          'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
                      userAgentPackageName: 'com.rimaai.app',
                    ),
                    MarkerLayer(
                      markers: [
                        for (final r in _risks)
                          Marker(
                            point: LatLng(r.latitude, r.longitude),
                            width: 44,
                            height: 44,
                            child: _RiskMarker(risk: r),
                          ),
                      ],
                    ),
                  ],
                ),
                if (_loading) const Center(child: CircularProgressIndicator()),
                if (_error != null)
                  Center(
                    child: Card(
                      color: Theme.of(context).colorScheme.errorContainer,
                      child: Padding(
                        padding: const EdgeInsets.all(16),
                        child: Text(_error!),
                      ),
                    ),
                  ),
                const Positioned(left: 12, bottom: 12, child: _Legend()),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _TypeFilterBar extends StatelessWidget {
  const _TypeFilterBar({required this.selected, required this.onChanged});
  final String? selected;
  final ValueChanged<String?> onChanged;

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      scrollDirection: Axis.horizontal,
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
      child: Row(
        children: [
          ChoiceChip(
            label: const Text('All'),
            selected: selected == null,
            onSelected: (_) => onChanged(null),
          ),
          const SizedBox(width: 8),
          for (final t in AppConstants.outbreakTypes) ...[
            ChoiceChip(
              avatar: Icon(t.icon, size: 18),
              label: Text(t.label),
              selected: selected == t.id,
              onSelected: (_) => onChanged(t.id),
            ),
            const SizedBox(width: 8),
          ],
        ],
      ),
    );
  }
}

class _RiskMarker extends StatelessWidget {
  const _RiskMarker({required this.risk});
  final DistrictRisk risk;

  @override
  Widget build(BuildContext context) {
    final color = AppConstants.riskColor(risk.level);
    return GestureDetector(
      onTap: () => showModalBottomSheet<void>(
        context: context,
        builder: (_) => _RiskSheet(risk: risk),
      ),
      child: Container(
        decoration: BoxDecoration(
          color: color.withValues(alpha: 0.85),
          shape: BoxShape.circle,
          border: Border.all(color: Colors.white, width: 2),
        ),
        alignment: Alignment.center,
        child: Text(
          '${risk.reportCount}',
          style:
              const TextStyle(color: Colors.white, fontWeight: FontWeight.bold),
        ),
      ),
    );
  }
}

class _RiskSheet extends StatelessWidget {
  const _RiskSheet({required this.risk});
  final DistrictRisk risk;

  @override
  Widget build(BuildContext context) {
    final label = AppConstants.outbreakTypes
        .firstWhere(
          (t) => t.id == risk.outbreakType,
          orElse: () => AppConstants.outbreakTypes.first,
        )
        .label;
    return Padding(
      padding: const EdgeInsets.all(20),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Expanded(
                child: Text(
                  risk.regionName,
                  style: Theme.of(context).textTheme.headlineSmall,
                ),
              ),
              RiskBadge(level: risk.level),
            ],
          ),
          const SizedBox(height: 8),
          Text('$label • ${risk.reportCount} recent reports'),
          const SizedBox(height: 4),
          Text('Risk score: ${risk.score.toStringAsFixed(1)}',
              style: Theme.of(context).textTheme.bodySmall),
        ],
      ),
    );
  }
}

class _Legend extends StatelessWidget {
  const _Legend();

  @override
  Widget build(BuildContext context) {
    return Card(
      child: Padding(
        padding: const EdgeInsets.all(10),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            _legendRow(AppConstants.riskColor('low'), 'Low'),
            _legendRow(AppConstants.riskColor('moderate'), 'Moderate'),
            _legendRow(AppConstants.riskColor('high'), 'High'),
          ],
        ),
      ),
    );
  }

  Widget _legendRow(Color color, String label) => Padding(
        padding: const EdgeInsets.symmetric(vertical: 2),
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
                width: 14,
                height: 14,
                decoration:
                    BoxDecoration(color: color, shape: BoxShape.circle)),
            const SizedBox(width: 6),
            Text(label, style: const TextStyle(fontSize: 12)),
          ],
        ),
      );
}
