import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

/// Holds the locally-registered farmer identity.
///
/// The full product uses Supabase Auth; for the MVP demo we persist the farmer
/// id + region returned by `POST /farmers` so subscription screens have a
/// stable identity without a login flow.
class FarmerSession extends ChangeNotifier {
  static const _idKey = 'rimaai.farmer_id';
  static const _regionKey = 'rimaai.farmer_region';

  int? _farmerId;
  String? _region;

  int? get farmerId => _farmerId;
  String? get region => _region;
  bool get isRegistered => _farmerId != null;

  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    final id = prefs.getInt(_idKey);
    if (id != null) {
      _farmerId = id;
      _region = prefs.getString(_regionKey);
      notifyListeners();
    }
  }

  Future<void> save(int farmerId, String? region) async {
    _farmerId = farmerId;
    _region = region;
    notifyListeners();
    final prefs = await SharedPreferences.getInstance();
    await prefs.setInt(_idKey, farmerId);
    if (region != null) await prefs.setString(_regionKey, region);
  }
}
