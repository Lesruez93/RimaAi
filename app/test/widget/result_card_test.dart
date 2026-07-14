import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rimaai/shared/widgets/result_card.dart';

void main() {
  Widget wrap(Widget child) => MaterialApp(home: Scaffold(body: child));

  testWidgets('shows title, advice and confidence percentage', (tester) async {
    await tester.pumpWidget(
      wrap(const ResultCard(
        title: 'Tomato Late Blight',
        advice: 'Remove infected plants.',
        confidence: 0.88,
      )),
    );

    expect(find.text('Tomato Late Blight'), findsOneWidget);
    expect(find.text('Remove infected plants.'), findsOneWidget);
    expect(find.text('88%'), findsOneWidget);
  });

  testWidgets('renders the disclaimer footer when provided', (tester) async {
    await tester.pumpWidget(
      wrap(const ResultCard(
        title: 'X',
        advice: 'Y',
        footer: 'Always confirm with a vet.',
      )),
    );
    expect(find.text('Always confirm with a vet.'), findsOneWidget);
  });
}
