from .detectioninterface import Detection

class MockDetector:

    def detect(self, frame):
        height, width = frame.shape[:2]

        # Simulated aircraft detection
        return [
            Detection(
                bbox=[
                    width * 0.45,
                    height * 0.45,
                    width * 0.50,
                    height * 0.49
                ],
                confidence=0.95,
                class_id=4
            )
        ]