import 'package:flutter/material.dart';

/// A modern typing indicator widget that shows animated dots
/// to indicate that the AI is processing a response.
class TypingIndicator extends StatefulWidget {
  const TypingIndicator({super.key});

  @override
  State<TypingIndicator> createState() => _TypingIndicatorState();
}

class _TypingIndicatorState extends State<TypingIndicator>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      vsync: this,
      duration: const Duration(milliseconds: 1400),
    )..repeat();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final isDark = Theme.of(context).brightness == Brightness.dark;
    final dotColor = isDark ? Colors.amber.withOpacity(0.6) : Colors.grey[600]!;

    return Row(
      mainAxisSize: MainAxisSize.min,
      children: [
        _buildDot(0, dotColor),
        const SizedBox(width: 4),
        _buildDot(1, dotColor),
        const SizedBox(width: 4),
        _buildDot(2, dotColor),
      ],
    );
  }

  Widget _buildDot(int index, Color color) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, child) {
        // Calculate animation progress for this dot
        // Each dot starts 200ms after the previous one
        final delayedProgress = (_controller.value - (index * 0.15)) % 1.0;
        
        // Create a smooth bounce animation
        double opacity;
        double scale;
        
        if (delayedProgress < 0.5) {
          // Fade in and scale up
          opacity = delayedProgress * 2;
          scale = 0.6 + (delayedProgress * 0.8);
        } else {
          // Fade out and scale down
          final reverseProgress = 1 - ((delayedProgress - 0.5) * 2);
          opacity = reverseProgress;
          scale = 0.6 + (reverseProgress * 0.8);
        }

        return Transform.scale(
          scale: scale,
          child: Opacity(
            opacity: opacity.clamp(0.3, 1.0),
            child: Container(
              width: 8,
              height: 8,
              decoration: BoxDecoration(
                color: color,
                shape: BoxShape.circle,
              ),
            ),
          ),
        );
      },
    );
  }
}
