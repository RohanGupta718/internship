import cv2
from ultralytics import YOLO
from tracker import Tracker
from target import get_center
from visualization import draw_target

def main():
    model = YOLO("yolo26n.pt")
    tracker = Tracker(model)
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        raise RuntimeError("yo camera broke g")
    while True:
        success, frame = camera.read()
        if not success:
            print("frema read error bruh")
            break
        results = tracker.track(frame)
        result = results[0]
        if result.boxes is not None:
            for box in result.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                if class_id != 4:
                    continue
                coordinates = box.xyxy[0].cpu().numpy()
                track_id = None
                if box.id is not None:
                    track_id = int(box.id[0])
                center = get_center(coordinates)

                print(
                    f"plane "
                    f"conf: {confidence:.2f} | "
                    f"mid: ({center[0]:.0f}, {center[1]:.0f}) | "
                    f"id: {track_id}"
                )
                frame = draw_target(
                    frame,
                    coordinates,
                    track_id
                )

        cv2.imshow("plane trackerr ", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()