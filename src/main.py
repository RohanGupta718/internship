import cv2
from pathlib import Path
from ultralytics import YOLO
from tracker import Tracker
from target import get_center
from visualization import draw_target

def main():
    model = YOLO(Path(__file__).parent / "best.pt")
    tracker = Tracker(
        model,
        detection_interval=4,
        confidence=0.25,
        image_size=640
    )
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("yo camera brokee")
    while True:
        success, frame = camera.read()
        if not success:
            print("frame read error rbuhhh")
            break
        box, track_id = tracker.update(frame)
        if box is not None:
            center = get_center(box)
            print(
                f"plane "
                f"mid: ({center[0]:.0f}, {center[1]:.0f}) | "
                f"id: {track_id}"
            )
            frame = draw_target(
                frame,
                box,
                track_id
            )
        cv2.imshow("plane trackerr", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()