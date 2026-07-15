import 'dart:convert';
import 'dart:io';

import 'package:http/http.dart' as http;

import 'api_config.dart';

/// Thrown when the backend returns a non-2xx response.
class ApiException implements Exception {
  ApiException(this.statusCode, this.message);
  final int statusCode;
  final String message;

  @override
  String toString() => 'ApiException($statusCode): $message';
}

/// Thin JSON/multipart HTTP client for the RimaAI backend.
///
/// Centralises base-URL handling, timeouts and error decoding so feature
/// repositories stay small and testable.
class ApiClient {
  ApiClient({http.Client? client, String? baseUrl})
      : _client = client ?? http.Client(),
        _baseUrl = baseUrl ?? ApiConfig.baseUrl;

  final http.Client _client;
  final String _baseUrl;

  Uri _uri(String path, [Map<String, dynamic>? query]) =>
      Uri.parse('$_baseUrl$path')
          .replace(queryParameters: query?.map((k, v) => MapEntry(k, '$v')));

  Future<dynamic> getJson(String path, {Map<String, dynamic>? query}) async {
    final res = await _client.get(_uri(path, query)).timeout(ApiConfig.timeout);
    return _decode(res);
  }

  Future<dynamic> postJson(String path, Map<String, dynamic> body) async {
    final res = await _client
        .post(
          _uri(path),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(body),
        )
        .timeout(ApiConfig.timeout);
    return _decode(res);
  }

  Future<dynamic> putJson(String path, Map<String, dynamic> body) async {
    final res = await _client
        .put(
          _uri(path),
          headers: {'Content-Type': 'application/json'},
          body: jsonEncode(body),
        )
        .timeout(ApiConfig.timeout);
    return _decode(res);
  }

  Future<void> delete(String path) async {
    final res = await _client.delete(_uri(path)).timeout(ApiConfig.timeout);
    _ensureOk(res);
  }

  /// Upload an image file (used by the server-side scan fallback).
  Future<dynamic> uploadImage(
    String path,
    File file, {
    Map<String, String> fields = const {},
  }) async {
    final request = http.MultipartRequest('POST', _uri(path))
      ..fields.addAll(fields)
      ..files.add(await http.MultipartFile.fromPath('file', file.path));
    final streamed = await request.send().timeout(ApiConfig.timeout);
    final res = await http.Response.fromStream(streamed);
    return _decode(res);
  }

  dynamic _decode(http.Response res) {
    _ensureOk(res);
    if (res.body.isEmpty) return null;
    return jsonDecode(res.body);
  }

  void _ensureOk(http.Response res) {
    if (res.statusCode < 200 || res.statusCode >= 300) {
      String message = res.body;
      try {
        final decoded = jsonDecode(res.body);
        if (decoded is Map && decoded['detail'] != null) {
          message = decoded['detail'].toString();
        }
      } catch (_) {
        // keep raw body
      }
      throw ApiException(res.statusCode, message);
    }
  }

  void close() => _client.close();
}
