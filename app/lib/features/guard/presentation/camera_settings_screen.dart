import 'package:flutter/material.dart';

import '../../../core/network/api_client.dart';
import '../data/guard_repository.dart';
import '../domain/guard_models.dart';

/// Camera stream setup, in the spirit of a V380 Pro-style "add camera"
/// screen: paste the IP camera's stream URL and pick demo vs. live mode.
class CameraSettingsScreen extends StatefulWidget {
  const CameraSettingsScreen({super.key, required this.cameraId});

  final String cameraId;

  @override
  State<CameraSettingsScreen> createState() => _CameraSettingsScreenState();
}

class _CameraSettingsScreenState extends State<CameraSettingsScreen> {
  final _repo = GuardRepository(ApiClient());
  final _urlController = TextEditingController();
  final _formKey = GlobalKey<FormState>();

  String _mode = 'demo';
  bool _loading = true;
  bool _saving = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    try {
      final settings = await _repo.cameraSettings(widget.cameraId);
      if (!mounted) return;
      setState(() {
        _mode = settings.mode;
        _urlController.text = settings.streamUrl ?? '';
        _loading = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _error = 'Could not load camera settings.';
        _loading = false;
      });
    }
  }

  Future<void> _save() async {
    if (_mode == 'live' && !(_formKey.currentState?.validate() ?? false)) {
      return;
    }
    setState(() {
      _saving = true;
      _error = null;
    });
    try {
      final updated = await _repo.updateCameraSettings(
        CameraSettings(
          cameraId: widget.cameraId,
          // Demo mode always plays the built-in demo stream, so there's
          // nothing farmer-specific to persist until they switch to live.
          streamUrl: _mode == 'live'
              ? (_urlController.text.trim().isEmpty
                  ? null
                  : _urlController.text.trim())
              : null,
          mode: _mode,
        ),
      );
      if (!mounted) return;
      Navigator.of(context).pop(updated);
    } catch (e) {
      if (!mounted) return;
      setState(() => _error = 'Could not save camera settings.');
    } finally {
      if (mounted) setState(() => _saving = false);
    }
  }

  @override
  void dispose() {
    _urlController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Camera settings')),
      body: _loading
          ? const Center(child: CircularProgressIndicator())
          : Form(
              key: _formKey,
              child: ListView(
                padding: const EdgeInsets.all(16),
                children: [
                  Text(
                    'Camera: ${widget.cameraId}',
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                  const SizedBox(height: 4),
                  Text(
                    'Point RimaAI Guard at your IP camera\'s stream, or stay '
                    'in demo mode to preview the feature without one.',
                    style: Theme.of(context).textTheme.bodySmall,
                  ),
                  const SizedBox(height: 20),
                  SegmentedButton<String>(
                    segments: const [
                      ButtonSegment(value: 'demo', label: Text('Demo')),
                      ButtonSegment(value: 'live', label: Text('Live camera')),
                    ],
                    selected: {_mode},
                    onSelectionChanged: (s) => setState(() => _mode = s.first),
                  ),
                  const SizedBox(height: 20),
                  TextFormField(
                    controller: _urlController,
                    enabled: _mode == 'live',
                    decoration: const InputDecoration(
                      labelText: 'Stream URL',
                      hintText: 'https://your-camera/live/index.m3u8',
                      helperText: 'HLS (.m3u8) stream from your camera or NVR.',
                      border: OutlineInputBorder(),
                    ),
                    validator: (v) {
                      if (_mode != 'live') return null;
                      final value = v?.trim() ?? '';
                      if (value.isEmpty) return 'Enter a stream URL.';
                      final uri = Uri.tryParse(value);
                      if (uri == null || !uri.isAbsolute) {
                        return 'Enter a valid URL.';
                      }
                      return null;
                    },
                  ),
                  if (_error != null) ...[
                    const SizedBox(height: 12),
                    Text(_error!,
                        style: TextStyle(
                            color: Theme.of(context).colorScheme.error)),
                  ],
                  const SizedBox(height: 24),
                  FilledButton(
                    onPressed: _saving ? null : _save,
                    child: _saving
                        ? const SizedBox(
                            height: 18,
                            width: 18,
                            child: CircularProgressIndicator(strokeWidth: 2),
                          )
                        : const Text('Save'),
                  ),
                ],
              ),
            ),
    );
  }
}
