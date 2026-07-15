import 'package:flutter/widgets.dart';

/// Lightweight trilingual string table (EN complete; SN/ND scaffolded).
///
/// A full app would use `flutter_localizations` + ARB files; for the MVP this
/// map-based lookup keeps the demo dependency-free and easy for reviewers to
/// extend. JSON mirrors live in `assets/l10n/` for future gen-l10n migration.
class AppStrings {
  const AppStrings(this.languageCode);

  final String languageCode;

  static const supportedLanguages = <String, String>{
    'en': 'English',
    'sn': 'chiShona',
    'nd': 'isiNdebele',
  };

  static const Map<String, Map<String, String>> _values = {
    'appName': {'en': 'RimaAI', 'sn': 'RimaAI', 'nd': 'RimaAI'},
    'tagline': {
      'en': 'Your smart farming companion',
      'sn': 'Shamwari yako yekurima ine njere',
      'nd': 'Umngane wakho wokulima ohlakaniphileyo',
    },
    'chooseLanguage': {
      'en': 'Choose your language',
      'sn': 'Sarudza mutauro wako',
      'nd': 'Khetha ulimi lwakho',
    },
    'getStarted': {
      'en': 'Get started',
      'sn': 'Tanga',
      'nd': 'Qalisa',
    },
    'home': {'en': 'Home', 'sn': 'Kumba', 'nd': 'Ekhaya'},
    'scan': {'en': 'Scan', 'sn': 'Skena', 'nd': 'Skena'},
    'scanCrop': {
      'en': 'Scan a crop',
      'sn': 'Skena chirimwa',
      'nd': 'Skena isilimo',
    },
    'livestock': {'en': 'Livestock', 'sn': 'Zvipfuwo', 'nd': 'Izifuyo'},
    'alerts': {'en': 'Alerts', 'sn': 'Yambiro', 'nd': 'Izaziso'},
    'guard': {'en': 'Guard', 'sn': 'Murindi', 'nd': 'Umlindi'},
    'outbreakMap': {
      'en': 'Outbreak map',
      'sn': 'Mepu yezvirwere',
      'nd': 'Imephu yezifo',
    },
    'reportOutbreak': {
      'en': 'Report an outbreak',
      'sn': 'Shuma chirwere',
      'nd': 'Bika isifo',
    },
    'triageTitle': {
      'en': 'Livestock health check',
      'sn': 'Kutarisa hutano hwezvipfuwo',
      'nd': 'Ukuhlola impilo yezifuyo',
    },
    'describeSymptoms': {
      'en': 'Describe the symptoms',
      'sn': 'Tsanangura zviratidzo',
      'nd': 'Chaza izimpawu',
    },
    'send': {'en': 'Send', 'sn': 'Tumira', 'nd': 'Thumela'},
    'consultVet': {
      'en': 'Always confirm with AGRITEX or a veterinarian.',
      'sn': 'Nguva dzose simbisa neAGRITEX kana chiremba wemhuka.',
      'nd': 'Hlala uqinisekisa le-AGRITEX kumbe udokotela wezifuyo.',
    },
    'subscribe': {'en': 'Subscribe', 'sn': 'Nyoresa', 'nd': 'Bhalisa'},
    'consentNotice': {
      'en': 'I consent to RimaAI storing my phone number to send me alerts.',
      'sn':
          'Ndinobvuma RimaAI kuchengeta nhamba yangu yefoni kuti inditumire yambiro.',
      'nd':
          'Ngiyavuma ukuthi i-RimaAI igcine inombolo yami yefoni ukuze ingithumele izaziso.',
    },
  };

  String t(String key) {
    final entry = _values[key];
    if (entry == null) return key;
    return entry[languageCode] ?? entry['en'] ?? key;
  }

  static AppStrings of(BuildContext context) {
    final code = Localizations.maybeLocaleOf(context)?.languageCode ?? 'en';
    return AppStrings(supportedLanguages.containsKey(code) ? code : 'en');
  }
}
