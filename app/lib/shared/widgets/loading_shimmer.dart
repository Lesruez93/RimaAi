import 'package:flutter/material.dart';

/// A lightweight shimmering placeholder block for loading states.
///
/// Implemented with a looping [AnimatedBuilder] gradient so it needs no extra
/// package dependency.
class LoadingShimmer extends StatefulWidget {
  const LoadingShimmer({
    super.key,
    this.height = 72,
    this.width = double.infinity,
    this.borderRadius = 12,
  });

  final double height;
  final double width;
  final double borderRadius;

  @override
  State<LoadingShimmer> createState() => _LoadingShimmerState();
}

class _LoadingShimmerState extends State<LoadingShimmer>
    with SingleTickerProviderStateMixin {
  late final AnimationController _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1200),
  )..repeat();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final base = Theme.of(context).colorScheme.surfaceContainerHighest;
    final highlight = base.withValues(alpha: 0.4);
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, _) {
        return Container(
          height: widget.height,
          width: widget.width,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(widget.borderRadius),
            gradient: LinearGradient(
              begin: Alignment(-1 - 2 * _controller.value, 0),
              end: Alignment(1 - 2 * _controller.value, 0),
              colors: [base, highlight, base],
            ),
          ),
        );
      },
    );
  }
}
