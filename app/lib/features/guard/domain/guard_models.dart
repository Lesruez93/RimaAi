/// A normalized detection box (0-1 coordinates) for UI overlay.
class DetectionBox {
  const DetectionBox({
    required this.label,
    required this.confidence,
    required this.x,
    required this.y,
    required this.width,
    required this.height,
  });

  final String label;
  final double confidence;
  final double x;
  final double y;
  final double width;
  final double height;

  factory DetectionBox.fromJson(Map<String, dynamic> json) {
    return DetectionBox(
      label: json['label'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      x: (json['x'] as num).toDouble(),
      y: (json['y'] as num).toDouble(),
      width: (json['width'] as num).toDouble(),
      height: (json['height'] as num).toDouble(),
    );
  }
}

/// Result of running Guard detection on one frame.
class GuardDetection {
  const GuardDetection({
    required this.cameraId,
    required this.frameId,
    required this.boxes,
    required this.isIntrusion,
    this.eventId,
  });

  final String cameraId;
  final String frameId;
  final List<DetectionBox> boxes;
  final bool isIntrusion;
  final int? eventId;

  factory GuardDetection.fromJson(Map<String, dynamic> json) {
    return GuardDetection(
      cameraId: json['camera_id'] as String,
      frameId: json['frame_id'] as String,
      isIntrusion: json['is_intrusion'] as bool? ?? false,
      eventId: json['event_id'] as int?,
      boxes: (json['boxes'] as List? ?? [])
          .map((e) => DetectionBox.fromJson(e as Map<String, dynamic>))
          .toList(),
    );
  }
}

/// A persisted Guard intrusion event for the history list.
class GuardEvent {
  const GuardEvent({
    required this.id,
    required this.cameraId,
    required this.label,
    required this.confidence,
    required this.isIntrusion,
    required this.createdAt,
  });

  final int id;
  final String cameraId;
  final String label;
  final double confidence;
  final bool isIntrusion;
  final DateTime createdAt;

  factory GuardEvent.fromJson(Map<String, dynamic> json) {
    return GuardEvent(
      id: json['id'] as int,
      cameraId: json['camera_id'] as String,
      label: json['label'] as String,
      confidence: (json['confidence'] as num).toDouble(),
      isIntrusion: json['is_intrusion'] as bool? ?? false,
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ??
          DateTime.now(),
    );
  }
}
