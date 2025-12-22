import 'package:flutter_test/flutter_test.dart';
import 'package:selcukaiassistant/services/response_cleaner.dart';

void main() {
  test('removes complete think block', () {
    const input = '<think>secret</think>Hello';
    final output = ResponseCleaner.clean(input);
    expect(output, 'Hello');
  });

  test('removes incomplete think tail', () {
    const input = 'Hello<think>abc';
    final output = ResponseCleaner.clean(input);
    expect(output, 'Hello');
  });

  test('preserves fenced code blocks', () {
    const input = '```\nReasoning: keep\n```';
    final output = ResponseCleaner.clean(input);
    expect(output, input);
  });

  test('does not remove normal Turkish content', () {
    const input = 'Mantık devreleri dijital sistemlerin temelidir.';
    final output = ResponseCleaner.clean(input);
    expect(output, input);
  });

  test('does not remove mid-body Analysis line', () {
    const input = 'Hello\n\nAnalysis: keep this\nMore';
    final output = ResponseCleaner.clean(input);
    expect(output, input);
  });
}
