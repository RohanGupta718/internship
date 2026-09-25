import cv2

class Tracker:
    def __init__(
        self,
        model,
        detection_interval=4,
        confidence=0.25,
        image_size=640
    ):
        self.model = model
        self.detection_interval = detection_interval
        self.confidence = confidence
        self.image_size = image_size
        self.tracker = None
        self.frame_count = 0
        self.last_box = None
        self.track_id = None

    def update(self, frame):
        self.frame_count += 1
        if (
            self.tracker is None
            or self.frame_count % self.detection_interval == 0
        ):
            return self._detect(frame)
        success, box = self.tracker.update(frame)
        if success:
            x, y, w, h = box
            self.last_box = (
                x,
                y,
                x + w,
                y + h
            )
            return self.last_box, self.track_id
        self.tracker = None
        return None, None

    def _detect(self, frame):
        results = self.model.predict(
            frame,
            classes=[0],
            conf=self.confidence,
            imgsz=self.image_size,
            verbose=False
        )
        result = results[0]
        if result.boxes is None or len(result.boxes) == 0:
            return None, None
        best_box = max(
            result.boxes,
            key=lambda box: float(box.conf[0])
        )
        coordinates = best_box.xyxy[0].cpu().numpy()
        x1, y1, x2, y2 = coordinates
        width = x2 - x1
        height = y2 - y1

        self.tracker = cv2.TrackerCSRT_create()
        self.tracker.init(
            frame,
            (
                int(x1),
                int(y1),
                int(width),
                int(height)
            )
        )
        self.last_box = (
            x1,
            y1,
            x2,
            y2
        )

        if self.track_id is None:
            self.track_id = 1

        return self.last_box, self.track_id
