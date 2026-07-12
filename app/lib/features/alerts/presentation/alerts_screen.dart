import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../../../core/constants/app_constants.dart';
import '../../../core/l10n/app_strings.dart';
import '../../../core/network/api_client.dart';
import '../../../core/session/farmer_session.dart';
import '../../../shared/widgets/primary_button.dart';
import '../../../shared/widgets/subscription_tile.dart';
import '../data/alerts_repository.dart';
import '../domain/subscription.dart';

/// Alerts screen: register (with consent) then toggle per-category subscriptions.
class AlertsScreen extends StatelessWidget {
  const AlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final session = context.watch<FarmerSession>();
    final s = AppStrings.of(context);
    return Scaffold(
      appBar: AppBar(title: Text(s.t('alerts'))),
      body: session.isRegistered
          ? const _SubscriptionsView()
          : const _RegistrationView(),
    );
  }
}

class _RegistrationView extends StatefulWidget {
  const _RegistrationView();

  @override
  State<_RegistrationView> createState() => _RegistrationViewState();
}

class _RegistrationViewState extends State<_RegistrationView> {
  final _repo = AlertsRepository(ApiClient());
  final _phone = TextEditingController();
  final _name = TextEditingController();
  String _region = AppConstants.zimbabweDistricts.first;
  bool _consent = false;
  bool _loading = false;
  String? _error;

  @override
  void dispose() {
    _phone.dispose();
    _name.dispose();
    super.dispose();
  }

  Future<void> _register() async {
    if (_phone.text.trim().length < 6 || !_consent) return;
    setState(() {
      _loading = true;
      _error = null;
    });
    final language = Localizations.localeOf(context).languageCode;
    try {
      final id = await _repo.registerFarmer(
        phoneNumber: _phone.text.trim(),
        consentGiven: _consent,
        name: _name.text.trim().isEmpty ? null : _name.text.trim(),
        language: language,
        regionName: _region,
      );
      if (!mounted) return;
      await context.read<FarmerSession>().save(id, _region);
    } on ApiException catch (e) {
      setState(() => _error = e.message);
    } catch (_) {
      setState(() => _error = 'Could not reach the server.');
    } finally {
      if (mounted) setState(() => _loading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final s = AppStrings.of(context);
    return SingleChildScrollView(
      padding: const EdgeInsets.all(16),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          Text('Subscribe to alerts',
              style: Theme.of(context).textTheme.headlineSmall),
          const SizedBox(height: 8),
          const Text(
            'Get weather, disease outbreak, livestock and insurance alerts by '
            'SMS — even on a basic phone via *123#.',
          ),
          const SizedBox(height: 20),
          TextField(
            controller: _phone,
            keyboardType: TextInputType.phone,
            decoration: const InputDecoration(
              labelText: 'Phone number',
              hintText: '+2637...',
              prefixIcon: Icon(Icons.phone_outlined),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: _name,
            decoration: const InputDecoration(
              labelText: 'Name (optional)',
              prefixIcon: Icon(Icons.person_outline),
            ),
          ),
          const SizedBox(height: 12),
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
          const SizedBox(height: 8),
          CheckboxListTile(
            value: _consent,
            onChanged: (v) => setState(() => _consent = v ?? false),
            contentPadding: EdgeInsets.zero,
            controlAffinity: ListTileControlAffinity.leading,
            title: Text(s.t('consentNotice')),
          ),
          if (_error != null) ...[
            const SizedBox(height: 8),
            Text(_error!, style: TextStyle(color: Theme.of(context).colorScheme.error)),
          ],
          const SizedBox(height: 12),
          PrimaryButton(
            label: s.t('subscribe'),
            icon: Icons.notifications_active_outlined,
            loading: _loading,
            onPressed: (_consent && _phone.text.trim().length >= 6)
                ? _register
                : null,
          ),
        ],
      ),
    );
  }
}

class _SubscriptionsView extends StatefulWidget {
  const _SubscriptionsView();

  @override
  State<_SubscriptionsView> createState() => _SubscriptionsViewState();
}

class _SubscriptionsViewState extends State<_SubscriptionsView> {
  final _repo = AlertsRepository(ApiClient());
  Map<String, bool> _active = {};
  bool _loading = true;

  @override
  void initState() {
    super.initState();
    _load();
  }

  Future<void> _load() async {
    final session = context.read<FarmerSession>();
    try {
      final subs = await _repo.list(session.farmerId!);
      setState(() {
        _active = {
          for (final c in AppConstants.alertCategories)
            c.id: subs.any((Subscription s) => s.category == c.id && s.active),
        };
        _loading = false;
      });
    } catch (_) {
      setState(() {
        _active = {for (final c in AppConstants.alertCategories) c.id: false};
        _loading = false;
      });
    }
  }

  Future<void> _toggle(String category, bool value) async {
    final session = context.read<FarmerSession>();
    setState(() => _active[category] = value);
    try {
      await _repo.upsert(
        farmerId: session.farmerId!,
        category: category,
        active: value,
        regionName: session.region,
      );
    } catch (_) {
      if (!mounted) return;
      setState(() => _active[category] = !value); // revert on failure
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Could not update subscription.')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_loading) {
      return const Center(child: CircularProgressIndicator());
    }
    return ListView(
      padding: const EdgeInsets.all(12),
      children: [
        for (final category in AppConstants.alertCategories)
          SubscriptionTile(
            title: category.label,
            icon: category.icon,
            value: _active[category.id] ?? false,
            onChanged: (v) => _toggle(category.id, v),
          ),
      ],
    );
  }
}
