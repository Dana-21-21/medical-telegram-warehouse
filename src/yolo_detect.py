import os
import cv2
import pandas as pd
from ultralytics import YOLO
from datetime import datetime

# ----------------------------
# CONFIGURATION
# ----------------------------
IMAGE_DIR = "data/raw/images"
OUTPUT_CSV = "data/processed/yolo_detections.csv"

# Load YOLOv8 nano model
model = YOLO("yolov8n.pt")

# ----------------------------
# HELPER: CLASSIFICATION RULE
# ----------------------------
def classify_image(detections):
    """
    Rules:
    - promotional: person + product/object
    - product_display: bottle/cup/package but no person
    - lifestyle: person but no product
    - other: nothing meaningful
    """

    classes = [d["name"] for d in detections]

    has_person = "person" in classes
    has_product = any(obj in classes for obj in ["bottle", "cup", "cell phone", "book", "laptop", "tv"])

    if has_person and has_product:
        return "promotional"
    elif has_product and not has_person:
        return "product_display"
    elif has_person and not has_product:
        return "lifestyle"
    else:
        return "other"

# ----------------------------
# RUN DETECTION
# ----------------------------
results_list = []

for root, _, files in os.walk(IMAGE_DIR):
    for file in files:
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            path = os.path.join(root, file)

            # Run YOLO
            results = model(path)

            detections = []

            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = model.names[cls_id]

                    detections.append({
                        "name": label,
                        "confidence": conf
                    })

            # Classify image
            image_category = classify_image(detections)

            # Save row
            results_list.append({
                "image_path": path,
                "detected_objects": str(detections),
                "image_category": image_category,
                "num_objects": len(detections),
                "timestamp": datetime.now()
            })

# ----------------------------
# SAVE OUTPUT
# ----------------------------
df = pd.DataFrame(results_list)
os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
df.to_csv(OUTPUT_CSV, index=False)

print(f"Saved YOLO results to: {OUTPUT_CSV}")
print(df.head())
