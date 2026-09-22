import cv2

def draw_target(frame, box, track_id=None):
    x1, y1, x2, y2 = map(int, box)
    cv2.rectangle(
        frame,
        (x1, y1),
        (x2, y2),
        (0, 255, 0),
        2
    )
    cx = int((x1 + x2) / 2)
    cy = int((y1 + y2) / 2)
    cv2.circle(
        frame,
        (cx, cy),
        5,
        (0, 0, 255),
        -1
    )
    if track_id is not None:
        cv2.putText(
            frame,
            f"id======> {track_id}",
            (x1, y1 - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 255, 255),
            2
        )
    return frame