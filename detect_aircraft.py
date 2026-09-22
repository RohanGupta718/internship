import cv2
from ultralytics import YOLO

# Load the pretrained YOLO26 nano model.
# The first run may download yolo26n.pt.
model = YOLO("yolo26n.pt")

# COCO class ID 4 represents airplane.
AIRPLANE_CLASS_ID = 4

# Open the default camera.
camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Could not open the camera.")
    print("Check camera permissions or try changing VideoCapture(0) to VideoCapture(1).")
    raise SystemExit

# Request camera settings.
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
camera.set(cv2.CAP_PROP_FPS, 30)

actual_width = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
actual_height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
actual_fps = camera.get(cv2.CAP_PROP_FPS)

print(f"Camera resolution: {actual_width} x {actual_height}")
print(f"Camera-reported FPS: {actual_fps}")
print("Live YOLO26 aircraft detection started.")
print("Click the camera window, then press Q or Escape to quit.")

while True:
    success, frame = camera.read()

    if not success:
        print("Could not read a camera frame.")
        break

    # Detect and track airplanes in every frame.
    results = model.track(
        source=frame,
        persist=True,
        classes=[AIRPLANE_CLASS_ID],
        conf=0.05,
        iou=0.45,
        imgsz=640,
        tracker="bytetrack.yaml",
        verbose=False
    )

    detections = []

    for result in results:
        if result.boxes is None:
            continue

        for box in result.boxes:
            # Boundary-box coordinates:
            # [x1, y1, x2, y2]
            coordinates = box.xyxy[0].tolist()

            x1, y1, x2, y2 = map(int, coordinates)

            # Required data types.
            confidence = float(box.conf[0])
            class_id = int(box.cls[0])

            detection = {
                "box": [x1, y1, x2, y2],
                "confidence": confidence,
                "class_id": class_id
            }

            # Include the tracking ID when available.
            if box.id is not None:
                detection["track_id"] = int(box.id[0])

            detections.append(detection)

            # Draw the boundary box.
            label = f"airplane {confidence:.2f}"

            if box.id is not None:
                label += f" ID {int(box.id[0])}"

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            cv2.putText(
                frame,
                label,
                (x1, max(y1 - 10, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

    # Print detections for the current frame.
    if detections:
        print(detections)

    # Resize only the display copy.
    display_width = 1280
    display_height = int(
        frame.shape[0] * display_width / frame.shape[1]
    )

    display_frame = cv2.resize(
        frame,
        (display_width, display_height)
    )

    cv2.imshow(
        "YOLO26 Live Aircraft Detection",
        display_frame
    )

    # The camera window must have focus for these keys to work.
    key = cv2.waitKey(1) & 0xFF

    if key == ord("q") or key == 27:
        print("Stopping program...")
        break

camera.release()
cv2.destroyAllWindows()