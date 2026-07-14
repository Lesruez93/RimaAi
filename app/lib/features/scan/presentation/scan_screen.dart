import 'dart:io';

import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';

import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../../../shared/widgets/loading_shimmer.dart';
import '../../../shared/widgets/primary_button.dart';
import '../../../shared/widgets/result_card.dart';
import '../data/scan_repository.dart';
import '../domain/scan_result.dart';

/// Crop/livestock disease scan screen: pick/capture a photo -> result + advice.
class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key, this.scanType = 'crop'});

  /// `crop` or `livestock` — reuses the same inference pipeline.
  final String scanType;

  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> {
  final _picker = ImagePicker();
  final _repo = ScanRepository(ApiClient());

  File? _image;
  ScanResult? _result;
  bool _loading = false;
  String? _error;

  Future<void> _pick(ImageSource source) async {
    final picked = await _picker.pickImage(source: source, imageQuality: 85);
    if (picked == null) return;
    setState(() {
      _image = File(picked.path);
      _result = null;
      _error = null;
    });
    await _analyze();
  }

  Future<void> _analyze() async {
    if (_image == null) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    final language = Localizations.localeOf(context).languageCode;
    try {
      final result = await _repo.scanImage(
        _image!,
        scanType: widget.scanType,
        language: language,
      );
      setState(() => _result = result);
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } catch (_) {
      setState(() => _error =
          'Could not reach the server. On-device scanning works offline in the '
          'full app; the demo needs the backend running.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    final isCrop = widget.scanType == 'crop';
    return Scaffold(
      appBar: AppBar(title: Text(isCrop ? s.t('scanCrop') : s.t('livestock'))),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            AspectRatio(
              aspectRatio: 4 / 3,
              child: Container(
                decoration: BoxDecoration(
                  borderRadius: BorderRadius.circular(16),
                  color: Theme.of(context).colorScheme.surfaceContainerHighest,
                ),
                clipBehavior: Clip.antiAlias,
                child: _image == null
                    ? const Center(
                        child: Icon(Icons.image_outlined, size: 64),
                      )
                    : Image.file(_image!, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(height: 16),
            Row(
              children: [
                Expanded(
                  child: PrimaryButton(
                    label: 'Camera',
                    icon: Icons.photo_camera_outlined,
                    onPressed: () => _pick(ImageSource.camera),
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: PrimaryButton(
                    label: 'Gallery',
                    icon: Icons.photo_library_outlined,
                    onPressed: () => _pick(ImageSource.gallery),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 20),
            if (_loading) const LoadingShimmer(height: 160),
            if (_error != null)
              Card(
                color: Theme.of(context).colorScheme.errorContainer,
                child: Padding(
                  padding: const EdgeInsets.all(16),
                  child: Text(_error!),
                ),
              ),
            if (_result != null)
              ResultCard(
                title: _result!.displayLabel,
                confidence: _result!.confidence,
                advice: _result!.advice,
                footer: s.t('consultVet'),
              ),
          ],
        ),
      ),
    );
  }
}
