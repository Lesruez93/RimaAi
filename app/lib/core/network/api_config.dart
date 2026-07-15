/// Backend connection configuration.
///
/// Override at build time with:
/// `flutter run --dart-define=RIMAAI_API_BASE=http://10.0.2.2:8000`
/// (10.0.2.2 is the Android emulator's alias for the host machine.)
///
/// Without an override, both debug and release builds default to the
/// deployed Cloud Run backend, so `flutter run` works against live data
/// without needing a local backend.
abstract final class ApiConfig {
  static const String _defaultBaseUrl =
      'https://rimaai-backend-943314742820.us-central1.run.app';

  static const String baseUrl =
      String.fromEnvironment('RIMAAI_API_BASE', defaultValue: _defaultBaseUrl);

  static const Duration timeout = Duration(seconds: 20);
}
