from pathlib import Path
from ultralytics import YOLO

# Load the pretrained YOLO11 model.
model = YOLO("yolo11n.pt")

# Folder containing the input photos.
image_folder = Path("images")

if not image_folder.exists():
    print("The 'images' folder does not exist.")
    print("Create it and put your photos inside it.")
    raise SystemExit

# Run YOLO on every supported image in the folder.
results = model.predict(
    source=str(image_folder),
    classes=[4],              # COCO class 4 = airplane
    conf=0.25,
    save=True,
    project="runs",
    name="detection",
    exist_ok=True
)

# Print the result for each image.
for result in results:
    image_name = Path(result.path).name
    number_detected = len(result.boxes)

    print(f"{image_name}: {number_detected} airplane(s) detected")

print()
print("Finished processing all images.")
print("Annotated images are in:")
print("runs/detection/")