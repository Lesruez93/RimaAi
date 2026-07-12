import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rimaai/core/constants/app_constants.dart';
import 'package:rimaai/shared/widgets/risk_badge.dart';

void main() {
  Widget wrap(Widget child) => MaterialApp(home: Scaffold(body: child));

  testWidgets('uppercases the level label', (tester) async {
    await tester.pumpWidget(wrap(const RiskBadge(level: 'high')));
    expect(find.text('HIGH'), findsOneWidget);
  });

  test('risk colours map by level', () {
    expect(AppConstants.riskColor('high'), isNot(AppConstants.riskColor('low')));
    expect(
      AppConstants.riskColor('moderate'),
      isNot(AppConstants.riskColor('high')),
    );
    // Unknown levels fall back to the low colour.
    expect(AppConstants.riskColor('unknown'), AppConstants.riskColor('low'));
  });
}
