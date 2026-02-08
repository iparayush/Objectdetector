from ultralytics import YOLO
import os

# Try to load custom model, else fallback to standard YOLOv8n (laptop detection)
custom_model_path = "model/best.pt"
model = None
is_custom = False

if os.path.exists(custom_model_path):
    try:
        model = YOLO(custom_model_path)
        is_custom = True
        print("Loaded Custom MacBook Model")
    except Exception as e:
        print(f"Error loading custom model: {e}")

if model is None:
    try:
        # Fallback to standard YOLOv8n
        model = YOLO("yolov8n.pt")
        print("Loaded Standard YOLOv8n (Fallback)")
    except Exception as e:
        print(f"Error loading YOLOv8n: {e}")

def detect_macbook(frame):
    if model:
        results = model(frame, verbose=False)
        for r in results:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                conf = float(box.conf[0])
                
                # Logic: 
                # If custom model, we expect class 0 (MacBook).
                # If standard model, we look for class 63 (laptop) in COCO dataset.
                
                detected = False
                if is_custom and cls_id == 0:
                    detected = True
                elif not is_custom and cls_id == 63: # 63 is laptop in COCO
                    detected = True
                
                if detected:
                    return { 
                        "detected": True, 
                        "confidence": conf,
                        "box": box.xyxy[0].tolist() # Return bbox for animation usage if needed
                    }
    
    return {"detected": False}
