import cv2
import time
import numpy as np

def draw_scanning_line(frame):
    """
    Draws a vertical scanning line that moves back and forth.
    """
    h, w, _ = frame.shape
    t = time.time()
    
    # Calculate position (sine wave for smooth movement)
    scan_x = int((np.sin(t * 2) + 1) / 2 * w)
    
    cv2.line(frame, (scan_x, 0), (scan_x, h), (0, 255, 0), 2)
    cv2.addWeighted(frame, 0.9, frame, 0.1, 0) # slight fade effect if we had a history buffer, but here it just does nothing effectively without a second image
    
    # Add a glowing strip
    overlay = frame.copy()
    cv2.rectangle(overlay, (scan_x - 5, 0), (scan_x + 5, h), (0, 255, 0), -1)
    cv2.addWeighted(overlay, 0.3, frame, 0.7, 0, frame)

def draw_manual_overlays(frame, manual_data):
    """
    Draws manual information overlays on the frame.
    """
    h, w, _ = frame.shape
    
    # Mock positions for demo (in real app, use object detection keypoints)
    # Left side: Ports
    cv2.circle(frame, (50, h//2), 10, (0, 255, 255), -1)
    cv2.line(frame, (50, h//2), (150, h//2 - 50), (0, 255, 255), 2)
    cv2.putText(frame, "USB-C / Thunderbolt", (160, h//2 - 50), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    
    # Center: Chip
    cv2.circle(frame, (w//2, h//2), 10, (0, 0, 255), -1)
    cv2.putText(frame, "M1 Chip", (w//2 + 20, h//2), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Bottom: Trackpad
    cv2.rectangle(frame, (w//2 - 100, h - 100), (w//2 + 100, h - 20), (255, 0, 0), 2)
    cv2.putText(frame, "Force Touch Trackpad", (w//2 - 80, h - 110), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
