import 'package:flutter/material.dart';

import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../data/guard_repository.dart';
import '../domain/guard_models.dart';

/// RimaAI Guard (commercial): a simulated camera feed with AI detection boxes
/// and an intrusion alert history. Sample frames stand in for a live IP camera.
class GuardScreen extends StatefulWidget {
  const GuardScreen({super.key});

  @override
  State<GuardScreen> createState() => _GuardScreenState();
}

class _GuardScreenState extends State<GuardScreen> {
  final _repo = GuardRepository(ApiClient());

  // Cyclable sample frames representing what the kraal camera "sees".
  static const _frames = [
    ('sample_quiet_01', 'Quiet — cattle only'),
    ('sample_night_01', 'Night — intruder'),
    ('sample_night_02', 'Night — intruder + vehicle'),
    ('sample_empty_01', 'Empty paddock'),
  ];

  int _frameIndex = 0;
  GuardDetection? _detection;
  List<GuardEvent> _events = [];
  bool _loading = false;

  @override
  void initState() {
    super.initState();
    _runDetection();
    _loadEvents();
  }

  Future<void> _runDetection() async {
    setState(() => _loading = true);
    try {
      final det = await _repo.detect(
        cameraId: 'kraal-cam-01',
        frameId: _frames[_frameIndex].$1,
      );
      setState(() => _detection = det);
      if (det.isIntrusion) await _loadEvents();
    } catch (_) {
      // Leave last detection; the demo needs the backend running.
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _loadEvents() async {
    try {
      final events = await _repo.events();
      if (mounted) setState(() => _events = events);
    } catch (_) {
      /* offline: keep current list */
    }
  }

  void _nextFrame() {
    setState(() => _frameIndex = (_frameIndex + 1) % _frames.length);
    _runDetection();
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    final det = _detection;
    final intrusion = det?.isIntrusion ?? false;
    return Scaffold(
      appBar: AppBar(
        title: Text(s.t('guard')),
        actions: [
          IconButton(
            onPressed: _loading ? null : _nextFrame,
            icon: const Icon(Icons.skip_next),
            tooltip: 'Next camera frame',
          ),
        ],
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          _CameraView(
            label: _frames[_frameIndex].$2,
            boxes: det?.boxes ?? const [],
            loading: _loading,
          ),
          const SizedBox(height: 12),
          if (intrusion)
            Card(
              color: Theme.of(context).colorScheme.errorContainer,
              child: ListTile(
                leading: const Icon(Icons.warning_amber_rounded),
                title: const Text('Intrusion detected!'),
                subtitle: Text(
                  'Alert sent to the farmer for camera ${det!.cameraId}.',
                ),
              ),
            ),
          const SizedBox(height: 8),
          Text('Alert history', style: Theme.of(context).textTheme.titleMedium),
          const SizedBox(height: 8),
          if (_events.isEmpty)
            const Padding(
              padding: EdgeInsets.all(16),
              child: Text('No intrusion events yet.'),
            ),
          for (final e in _events)
            Card(
              child: ListTile(
                leading: Icon(
                  e.label == 'vehicle'
                      ? Icons.directions_car_outlined
                      : Icons.person_outline,
                  color: Theme.of(context).colorScheme.error,
                ),
                title: Text('${e.label} @ ${e.cameraId}'),
                subtitle: Text(
                  '${(e.confidence * 100).round()}% • ${_fmt(e.createdAt)}',
                ),
              ),
            ),
        ],
      ),
    );
  }

  String _fmt(DateTime dt) =>
      '${dt.year}-${dt.month.toString().padLeft(2, '0')}-${dt.day.toString().padLeft(2, '0')} '
      '${dt.hour.toString().padLeft(2, '0')}:${dt.minute.toString().padLeft(2, '0')}';
}

/// The simulated camera viewport with detection boxes drawn over it.
class _CameraView extends StatelessWidget {
  const _CameraView({
    required this.label,
    required this.boxes,
    required this.loading,
  });

  final String label;
  final List<DetectionBox> boxes;
  final bool loading;

  @override
  Widget build(BuildContext context) {
    return AspectRatio(
      aspectRatio: 16 / 10,
      child: ClipRRect(
        borderRadius: BorderRadius.circular(14),
        child: LayoutBuilder(
          builder: (context, constraints) {
            return Stack(
              children: [
                // Faux night-vision backdrop.
                Container(
                  decoration: const BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [Color(0xFF0d1f14), Color(0xFF04120a)],
                    ),
                  ),
                ),
                for (final b in boxes)
                  Positioned(
                    left: b.x * constraints.maxWidth,
                    top: b.y * constraints.maxHeight,
                    width: b.width * constraints.maxWidth,
                    height: b.height * constraints.maxHeight,
                    child: _BoxOverlay(box: b),
                  ),
                Positioned(
                  left: 10,
                  top: 8,
                  child: Row(
                    children: [
                      const Icon(Icons.circle, size: 10, color: Colors.redAccent),
                      const SizedBox(width: 6),
                      Text('LIVE • $label',
                          style: const TextStyle(color: Colors.white70, fontSize: 12)),
                    ],
                  ),
                ),
                if (loading)
                  const Positioned.fill(
                    child: Center(child: CircularProgressIndicator()),
                  ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _BoxOverlay extends StatelessWidget {
  const _BoxOverlay({required this.box});
  final DetectionBox box;

  @override
  Widget build(BuildContext context) {
    final isThreat = box.label == 'person' || box.label == 'vehicle';
    final color = isThreat ? Colors.redAccent : Colors.lightGreenAccent;
    return Container(
      decoration: BoxDecoration(
        border: Border.all(color: color, width: 2),
        borderRadius: BorderRadius.circular(4),
      ),
      alignment: Alignment.topLeft,
      child: Container(
        color: color,
        padding: const EdgeInsets.symmetric(horizontal: 4, vertical: 1),
        child: Text(
          '${box.label} ${(box.confidence * 100).round()}%',
          style: const TextStyle(color: Colors.black, fontSize: 10),
        ),
      ),
    );
  }
}
