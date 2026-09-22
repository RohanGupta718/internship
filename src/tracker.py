class Tracker:
    def __init__(self, model, tracker_config="botsort.yaml"):
        self.model = model
        self.tracker_config = tracker_config
    def track(self, frame):
        return self.model.track(
            frame,
            persist=True,
            tracker=self.tracker_config,
            verbose=False
        )