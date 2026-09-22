from ultralytics import YOLO

class Detector:
    def __init__(self, model_path, confidence=0.35):
        self.model=YOLO(model_path)
        self.confidence=confidence

    def detect(self,frame):
        return self.model.predict(
            frame,
            conf=self.confidence,
            verbose=False
        )

