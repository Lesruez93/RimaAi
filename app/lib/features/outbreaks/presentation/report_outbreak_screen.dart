import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../../../core/session/farmer_session.dart';
import '../../../shared/widgets/primary_button.dart';
import '../data/outbreak_repository.dart';
import '../domain/outbreak_models.dart';

/// Community "Report an outbreak" flow: type + district + description.
class ReportOutbreakScreen extends StatefulWidget {
  const ReportOutbreakScreen({super.key});

  @override
  State<ReportOutbreakScreen> createState() => _ReportOutbreakScreenState();
}

class _ReportOutbreakScreenState extends State<ReportOutbreakScreen> {
  final _repo = OutbreakRepository(ApiClient());
  final _description = TextEditingController();

  String _type = AppConstants.outbreakTypes.first.id;
  late String _region = AppConstants.zimbabweDistricts.first;
  bool _loading = false;
  String? _error;

  @override
  void initState() {
    super.initState();
    final sessionRegion = context.read<FarmerSession>().region;
    if (sessionRegion != null &&
        AppConstants.zimbabweDistricts.contains(sessionRegion)) {
      _region = sessionRegion;
    }
  }

  @override
  void dispose() {
    _description.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _error = null;
    });
    try {
      final result = await _repo.report(
        regionName: _region,
        outbreakType: _type,
        description:
            _description.text.trim().isEmpty ? null : _description.text.trim(),
        farmerId: context.read<FarmerSession>().farmerId,
      );
      if (!mounted) return;
      await _showResult(result);
      if (mounted) Navigator.of(context).pop(true);
    } catch (_) {
      setState(() => _error = 'Could not submit the report.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  Future<void> _showResult(OutbreakReportResult result) {
    final message = result.alertDispatched
        ? 'Thank you. $_region is now HIGH risk — a targeted alert was sent to '
            '${result.alertRecipients} subscriber(s).'
        : 'Thank you. Your report was recorded. Current $_region risk: '
            '${result.riskLevel}.';
    return showDialog<void>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Report submitted'),
        content: Text(message),
        actions: [
          TextButton(
            onPressed: () => Navigator.of(context).pop(),
            child: const Text('OK'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(s.t('reportOutbreak'))),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text('Outbreak type', style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final t in AppConstants.outbreakTypes)
                  ChoiceChip(
                    avatar: Icon(t.icon, size: 18),
                    label: Text(t.label),
                    selected: _type == t.id,
                    onSelected: (_) => setState(() => _type = t.id),
                  ),
              ],
            ),
            const SizedBox(height: 20),
            DropdownButtonFormField<String>(
              value: _region,
              decoration: const InputDecoration(
                labelText: 'District',
                prefixIcon: Icon(Icons.place_outlined),
              ),
              items: AppConstants.zimbabweDistricts
                  .map((d) => DropdownMenuItem(value: d, child: Text(d)))
                  .toList(),
              onChanged: (v) => setState(() => _region = v ?? _region),
            ),
            const SizedBox(height: 16),
            TextField(
              controller: _description,
              minLines: 3,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'What did you see? (optional)',
                alignLabelWithHint: true,
              ),
            ),
            if (_error != null) ...[
              const SizedBox(height: 12),
              Text(_error!,
                  style: TextStyle(color: Theme.of(context).colorScheme.error)),
            ],
            const SizedBox(height: 20),
            PrimaryButton(
              label: 'Submit report',
              icon: Icons.send_outlined,
              loading: _loading,
              onPressed: _submit,
            ),
            const SizedBox(height: 8),
            Text(
              'Community reports are aggregated by district using plain weighted '
              'rules (report count × recency × reporter trust). High-risk '
              'districts trigger automatic SMS alerts to nearby subscribers.',
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}
