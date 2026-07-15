import 'package:flutter/material.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../../../shared/widgets/result_card.dart';
import '../../scan/presentation/scan_screen.dart';
import '../data/triage_repository.dart';
import '../domain/triage_result.dart';

/// Livestock advisor: a photo health-check shortcut + a symptom triage chat.
class LivestockScreen extends StatefulWidget {
  const LivestockScreen({super.key});

  @override
  State<LivestockScreen> createState() => _LivestockScreenState();
}

class _LivestockScreenState extends State<LivestockScreen> {
  final _repo = TriageRepository(ApiClient());
  final _controller = TextEditingController();
  final _messages = <_ChatEntry>[];
  bool _loading = false;

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  Future<void> _send() async {
    final text = _controller.text.trim();
    if (text.isEmpty || _loading) return;
    setState(() {
      _messages.add(_ChatEntry.user(text));
      _controller.clear();
      _loading = true;
    });
    final language = Localizations.localeOf(context).languageCode;
    try {
      final result = await _repo.triage(text, language: language);
      setState(() => _messages.add(_ChatEntry.result(result)));
    } catch (_) {
      setState(() => _messages.add(_ChatEntry.error(
            'Could not reach the triage service. Please check your connection.',
          )));
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(s.t('triageTitle'))),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(12),
            child: Card(
              child: ListTile(
                leading: const Icon(Icons.photo_camera_outlined),
                title: const Text('Photo health check'),
                subtitle:
                    const Text('Check tick load / skin condition from a photo'),
                trailing: const Icon(Icons.chevron_right),
                onTap: () => Navigator.of(context).push(
                  MaterialPageRoute(
                    builder: (_) => const ScanScreen(scanType: 'livestock'),
                  ),
                ),
              ),
            ),
          ),
          Expanded(
            child: _messages.isEmpty
                ? _EmptyHint(text: s.t('describeSymptoms'))
                : ListView.builder(
                    padding: const EdgeInsets.symmetric(horizontal: 12),
                    itemCount: _messages.length,
                    itemBuilder: (context, i) => _messages[i].build(context, s),
                  ),
          ),
          if (_loading)
            const Padding(
              padding: EdgeInsets.all(8),
              child: LinearProgressIndicator(),
            ),
          SafeArea(
            top: false,
            child: Padding(
              padding: const EdgeInsets.all(12),
              child: Row(
                children: [
                  Expanded(
                    child: TextField(
                      controller: _controller,
                      minLines: 1,
                      maxLines: 3,
                      textInputAction: TextInputAction.send,
                      onSubmitted: (_) => _send(),
                      decoration: InputDecoration(
                        hintText: s.t('describeSymptoms'),
                      ),
                    ),
                  ),
                  const SizedBox(width: 8),
                  IconButton.filled(
                    onPressed: _send,
                    icon: const Icon(Icons.send),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }
}

class _EmptyHint extends StatelessWidget {
  const _EmptyHint({required this.text});
  final String text;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.chat_bubble_outline, size: 56),
            const SizedBox(height: 12),
            Text(
              text,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            const SizedBox(height: 8),
            Text(
              'e.g. "my cow has many ticks and a swollen neck"',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodySmall,
            ),
          ],
        ),
      ),
    );
  }
}

/// A single chat entry — a user message, a triage result card, or an error.
class _ChatEntry {
  const _ChatEntry._({this.userText, this.result, this.errorText});

  factory _ChatEntry.user(String text) => _ChatEntry._(userText: text);
  factory _ChatEntry.result(TriageResult r) => _ChatEntry._(result: r);
  factory _ChatEntry.error(String text) => _ChatEntry._(errorText: text);

  final String? userText;
  final TriageResult? result;
  final String? errorText;

  Widget build(BuildContext context, AppStrings s) {
    if (userText != null) {
      return Align(
        alignment: Alignment.centerRight,
        child: Container(
          margin: const EdgeInsets.symmetric(vertical: 6),
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: Theme.of(context).colorScheme.primaryContainer,
            borderRadius: BorderRadius.circular(14),
          ),
          child: Text(userText!),
        ),
      );
    }
    if (errorText != null) {
      return Padding(
        padding: const EdgeInsets.symmetric(vertical: 6),
        child: Card(
          color: Theme.of(context).colorScheme.errorContainer,
          child: Padding(
              padding: const EdgeInsets.all(14), child: Text(errorText!)),
        ),
      );
    }
    final r = result!;
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 6),
      child: ResultCard(
        title: r.condition,
        advice: '${r.advice}\n\n${r.escalation}',
        accentColor: AppConstants.urgencyColor(r.urgency),
        badge: _UrgencyBadge(urgency: r.urgency),
        footer: r.disclaimer,
      ),
    );
  }
}

class _UrgencyBadge extends StatelessWidget {
  const _UrgencyBadge({required this.urgency});
  final String urgency;

  @override
  Widget build(BuildContext context) {
    final color = AppConstants.urgencyColor(urgency);
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.15),
        borderRadius: BorderRadius.circular(20),
        border: Border.all(color: color),
      ),
      child: Text(
        urgency.toUpperCase(),
        style:
            TextStyle(color: color, fontWeight: FontWeight.w700, fontSize: 12),
      ),
    );
  }
}
