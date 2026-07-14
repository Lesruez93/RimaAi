import '../../../core/network/api_client.dart';
import '../domain/subscription.dart';

/// Repository for farmer registration and alert-subscription management.
class AlertsRepository {
  AlertsRepository(this._api);

  final ApiClient _api;

  /// Register a farmer. Consent is mandatory (enforced server-side too).
  Future<int> registerFarmer({
    required String phoneNumber,
    required bool consentGiven,
    String? name,
    String language = 'en',
    String? regionName,
  }) async {
    final json = await _api.postJson('/farmers', {
      'phone_number': phoneNumber,
      'consent_given': consentGiven,
      'name': name,
      'language': language,
      'region_name': regionName,
    });
    return (json as Map<String, dynamic>)['id'] as int;
  }

  Future<List<Subscription>> list(int farmerId) async {
    final json = await _api.getJson('/subscriptions/$farmerId');
    return (json as List)
        .map((e) => Subscription.fromJson(e as Map<String, dynamic>))
        .toList();
  }

  Future<Subscription> upsert({
    required int farmerId,
    required String category,
    required bool active,
    String channel = 'sms',
    String? regionName,
  }) async {
    final json = await _api.postJson('/subscriptions', {
      'farmer_id': farmerId,
      'category': category,
      'channel': channel,
      'active': active,
      'region_name': regionName,
    });
    return Subscription.fromJson(json as Map<String, dynamic>);
  }
}
