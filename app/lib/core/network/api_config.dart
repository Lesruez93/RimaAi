import 'package:flutter/foundation.dart' show kReleaseMode;

/// Backend connection configuration.
///
/// Override at build time with:
/// `flutter run --dart-define=RIMAAI_API_BASE=http://10.0.2.2:8000`
/// (10.0.2.2 is the Android emulator's alias for the host machine.)
///
/// Without an override, debug builds (`flutter run`) default to the Android
/// emulator's local-host alias for a locally running backend, while release
/// builds (`flutter build apk/ipa --release`) default to the deployed Cloud
/// Run backend so a shipped build works out of the box.
abstract final class ApiConfig {
  static const String _devDefault = 'http://10.0.2.2:8000';
  static const String _releaseDefault =
      'https://rimaai-backend-943314742820.us-central1.run.app';

  static const String baseUrl = kReleaseMode
      ? String.fromEnvironment('RIMAAI_API_BASE', defaultValue: _releaseDefault)
      : String.fromEnvironment('RIMAAI_API_BASE', defaultValue: _devDefault);

  static const Duration timeout = Duration(seconds: 20);
}
