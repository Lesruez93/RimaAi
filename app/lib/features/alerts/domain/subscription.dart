/// A farmer's subscription to one alert category on one channel.
class Subscription {
  const Subscription({
    required this.id,
    required this.farmerId,
    required this.category,
    required this.channel,
    required this.active,
    this.regionName,
  });

  final int id;
  final int farmerId;
  final String category;
  final String channel;
  final bool active;
  final String? regionName;

  factory Subscription.fromJson(Map<String, dynamic> json) {
    return Subscription(
      id: json['id'] as int,
      farmerId: json['farmer_id'] as int,
      category: json['category'] as String,
      channel: json['channel'] as String,
      active: json['active'] as bool,
      regionName: json['region_name'] as String?,
    );
  }
}
