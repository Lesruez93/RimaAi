/// Backend connection configuration.
///
/// Override at build time with:
/// `flutter run --dart-define=RIMAAI_API_BASE=http://10.0.2.2:8000`
/// (10.0.2.2 is the Android emulator's alias for the host machine.)
abstract final class ApiConfig {
  static const String baseUrl = String.fromEnvironment(
    'RIMAAI_API_BASE',
    defaultValue: 'http://10.0.2.2:8000',
  );

  static const Duration timeout = Duration(seconds: 20);
}
