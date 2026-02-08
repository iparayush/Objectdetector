from flask import Flask, jsonify, Response
from flask_cors import CORS
import cv2
import json
import os
import threading

# Import our custom modules
# We need to make sure python path includes current directory
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from detector.macbook_detector import detect_macbook
from detector.animation import draw_scanning_line, draw_manual_overlays

app = Flask(__name__)
CORS(app)

# Load Manual Data
MANUAL_FILE = os.path.join(os.path.dirname(__file__), "manual/macbook_manual.json")
GOBOLT_FILE = os.path.join(os.path.dirname(__file__), "manual/gobolt_manual.json")

MANUAL_DATA = {}
GOBOLT_DATA = {}

try:
    with open(MANUAL_FILE, "r") as f:
        MANUAL_DATA = json.load(f)
    with open(GOBOLT_FILE, "r") as f:
        GOBOLT_DATA = json.load(f)
except Exception as e:
    print(f"Error loading manuals: {e}")

camera = None
camera_lock = threading.Lock()
latest_detection_result = {"detected": False}
current_device_mode = "macbook" # Can be 'macbook' or 'gobolt'

def get_camera():
    global camera
    if camera is None or not camera.isOpened():
        camera = cv2.VideoCapture(0)
    return camera

def generate_frames():
    global latest_detection_result
    while True:
        with camera_lock:
            cam = get_camera()
            if not cam.isOpened():
                break
            success, frame = cam.read()
        
        if not success:
            break
            
        # 1. Run Detection
        result = detect_macbook(frame)
        latest_detection_result = result
        
        # 2. Apply Animations if detected
        if result["detected"]:
            draw_scanning_line(frame)
            draw_manual_overlays(frame, MANUAL_DATA)
            
            # Draw bounding box (simple version, assuming result might have coords later)
            # For now just a label
            cv2.putText(frame, f"MacBook Detected: {result['confidence']:.2f}", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        else:
             cv2.putText(frame, "Scanning...", (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        # 3. Encode Frame
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/set_mode/<mode>", methods=["POST"])
def set_mode(mode):
    global current_device_mode
    if mode in ["macbook", "gobolt"]:
        current_device_mode = mode
        return jsonify({"status": "success", "mode": mode})
    return jsonify({"status": "error", "message": "Invalid mode"}), 400

@app.route("/detect", methods=["GET"])
def detect():
    global latest_detection_result, current_device_mode
    
    # Return the latest result from the video feed loop
    # For GoBOLT, we mock detection since we don't have a model yet
    if current_device_mode == "gobolt":
        return jsonify({
            "detected": True,
            "device": "GoBOLT Headphones",
            "confidence": 0.98,
            "manual": GOBOLT_DATA,
            "type": "rich" # Signal frontend to use rich renderer
        })
    
    if latest_detection_result["detected"]:
        return jsonify({
            "detected": True,
            "device": "MacBook Air M1",
            "confidence": latest_detection_result["confidence"],
            "manual": MANUAL_DATA,
            "type": "simple"
        })

    return jsonify({"detected": False})

if __name__ == "__main__":
    print("Starting Flask server on port 5001...")
    try:
        app.run(debug=True, host="0.0.0.0", port=5001, use_reloader=False) # use_reloader=False to avoid double loading in some envs
    except Exception as e:
        print(f"Failed to start server: {e}")
