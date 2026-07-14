import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Holds the app's active locale and persists the user's language choice.
class LocaleController extends ChangeNotifier {
  LocaleController([Locale? initial]) : _locale = initial ?? const Locale('en');

  static const _prefsKey = 'rimaai.language';

  Locale _locale;
  Locale get locale => _locale;

  /// Load the previously chosen language from local storage.
  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    final code = prefs.getString(_prefsKey);
    if (code != null) {
      _locale = Locale(code);
      notifyListeners();
    }
  }

  /// Change and persist the active language (`en` / `sn` / `nd`).
  Future<void> setLanguage(String code) async {
    _locale = Locale(code);
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_prefsKey, code);
  }
}
