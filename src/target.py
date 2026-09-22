import math
def get_center(box):
    x1, y1, x2, y2 = box
    return (
        (x1 + x2) / 2,
        (y1 + y2) / 2
    )

def distance_from_center(box, frame_width, frame_height):
    cx, cy = get_center(box)
    image_cx = frame_width / 2
    image_cy = frame_height / 2
    return math.sqrt(
        (cx - image_cx) ** 2 +
        (cy - image_cy) ** 2
    )

def select_target(boxes, frame_width, frame_height):
    valid_boxes = [
        box for box in boxes
        if box.id is not None
    ]
    if not valid_boxes:
        return None
    return min(
        valid_boxes,
        key=lambda box: distance_from_center(
            box.xyxy[0].cpu().numpy(),
            frame_width,
            frame_height
        )
    )