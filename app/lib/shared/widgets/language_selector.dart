import 'package:flutter/material.dart';

import '../../core/l10n/app_strings.dart';

/// A segmented control for choosing between the three supported languages.
class LanguageSelector extends StatelessWidget {
  const LanguageSelector({
    super.key,
    required this.selected,
    required this.onSelected,
  });

  /// Active language code (`en` / `sn` / `nd`).
  final String selected;
  final ValueChanged<String> onSelected;

  @override
  Widget build(BuildContext context) {
    return Column(
      children: AppStrings.supportedLanguages.entries.map((entry) {
        final isSelected = entry.key == selected;
        return Card(
          color: isSelected
              ? Theme.of(context).colorScheme.primaryContainer
              : null,
          child: ListTile(
            onTap: () => onSelected(entry.key),
            leading: Icon(
              isSelected ? Icons.radio_button_checked : Icons.radio_button_off,
              color: Theme.of(context).colorScheme.primary,
            ),
            title: Text(entry.value),
            trailing: Text(entry.key.toUpperCase()),
          ),
        );
      }).toList(),
    );
  }
}
