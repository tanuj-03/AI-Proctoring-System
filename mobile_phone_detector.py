from ultralytics import YOLO
import cv2

class PhoneDetector:
    def __init__(self):
        # Loads the lightweight YOLOv8 model
        self.model = YOLO('yolov8n.pt')

    def detect_phone(self, frame):
        """Scans the frame for cell phones and draws a box if found."""
        # verbose=False prevents YOLO from spamming your terminal 
        results = self.model(frame, verbose=False)
        
        phone_detected = False
        
        for box in results[0].boxes:
            # 67 is the official COCO dataset ID number for 'cell phone'
            if int(box.cls[0]) == 67: 
                phone_detected = True
                
                # Draw a red box around the phone
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
                cv2.putText(frame, "Phone", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                
        if phone_detected:
            return "Cell Phone Detected!"
        return None