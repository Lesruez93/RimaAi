import 'package:flutter/material.dart';

/// A switch tile for toggling a single alert-category subscription.
class SubscriptionTile extends StatelessWidget {
  const SubscriptionTile({
    super.key,
    required this.title,
    required this.icon,
    required this.value,
    required this.onChanged,
    this.subtitle,
  });

  final String title;
  final String? subtitle;
  final IconData icon;
  final bool value;
  final ValueChanged<bool> onChanged;

  @override
  Widget build(BuildContext context) {
    return Card(
      child: SwitchListTile(
        value: value,
        onChanged: onChanged,
        secondary: Icon(icon, color: Theme.of(context).colorScheme.primary),
        title: Text(title),
        subtitle: subtitle == null ? null : Text(subtitle!),
      ),
    );
  }
}
