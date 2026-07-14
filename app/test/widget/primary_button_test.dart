import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:rimaai/shared/widgets/primary_button.dart';

void main() {
  Widget wrap(Widget child) => MaterialApp(home: Scaffold(body: child));

  testWidgets('renders its label and fires onPressed', (tester) async {
    var tapped = false;
    await tester.pumpWidget(
      wrap(PrimaryButton(label: 'Subscribe', onPressed: () => tapped = true)),
    );

    expect(find.text('Subscribe'), findsOneWidget);
    await tester.tap(find.byType(PrimaryButton));
    expect(tapped, isTrue);
  });

  testWidgets('shows a spinner and blocks taps while loading', (tester) async {
    var tapped = false;
    await tester.pumpWidget(
      wrap(PrimaryButton(
        label: 'Subscribe',
        loading: true,
        onPressed: () => tapped = true,
      )),
    );

    expect(find.byType(CircularProgressIndicator), findsOneWidget);
    expect(find.text('Subscribe'), findsNothing);
    await tester.tap(find.byType(PrimaryButton));
    expect(tapped, isFalse);
  });
}
