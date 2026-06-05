import cv2
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import logging
import time
import os
import urllib.request

# --- IMPORT OUR CUSTOM MODULES ---
from multiple_face_detection import check_multiple_faces
from eye_tracker import track_eye
from mouth_opening_detector import MouthTracker
from head_pose_estimation import estimate_head_pose
from mobile_phone_detector import PhoneDetector
from audio_transcriber import AudioTracker 
from keyboard_tracker import KeyboardTracker 

# --- 1. SETUP LOGGING & SESSION MANAGEMENT ---
log_file = 'suspicious_events.log'

# Figure out what section number this is by counting previous runs
section_number = 1
if os.path.exists(log_file):
    with open(log_file, 'r') as f:
        section_number = f.read().count("SECTION START") + 1

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Record the exact start time
session_start_time = time.time()

# Write a clean, visible header to the log file
logging.info("")
logging.info(f"*** SECTION START: SESSION {section_number} ***")

# --- 2. DOWNLOAD MODEL (if missing) ---
mp_model_path = 'face_landmarker.task'
if not os.path.exists(mp_model_path):
    print("Downloading MediaPipe Face Landmarker model...")
    url = "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task"
    urllib.request.urlretrieve(url, mp_model_path)

# --- 3. SETUP MEDIAPIPE FACE LANDMARKER ---
base_options = python.BaseOptions(model_asset_path=mp_model_path)
options = vision.FaceLandmarkerOptions(
    base_options=base_options,
    running_mode=vision.RunningMode.IMAGE,
    num_faces=2, 
    output_face_blendshapes=True 
)
landmarker = vision.FaceLandmarker.create_from_options(options)

# --- 4. SYSTEM VARIABLES ---
cap = cv2.VideoCapture(0)
last_logged_time = 0 
log_cooldown = 3

# Initialize our custom tracker classes
mouth_tracker = MouthTracker() 
phone_tracker = PhoneDetector()
audio_tracker = AudioTracker() 
keyboard_tracker = KeyboardTracker() 

print(f"Starting Modular Proctoring System (Session {section_number})... Press 'q' to quit.")

# Timers for persistent warning display
active_audio_warnings = []
audio_warning_timer = 0

while cap.isOpened():
    success, frame = cap.read()
    if not success: continue

    h, w, _ = frame.shape
    current_time = time.time()
    active_warnings = []

    # --- A. KEYBOARD TRACKING MODULE ---
    new_kb_warnings = keyboard_tracker.get_warnings()
    if new_kb_warnings:
        active_warnings.extend(new_kb_warnings)

    # --- B. AUDIO TRACKING MODULE ---
    new_audio_warnings = audio_tracker.get_warnings()
    if new_audio_warnings:
        active_audio_warnings.extend(new_audio_warnings)
        audio_warning_timer = current_time 

    if current_time - audio_warning_timer < 5:
        active_warnings.extend(active_audio_warnings)
    else:
        active_audio_warnings.clear()

    # --- C. PHONE DETECTION MODULE ---
    phone_warning = phone_tracker.detect_phone(frame)
    if phone_warning:
        active_warnings.append(phone_warning)

    # --- D. VISUAL FACE MODULES ---
    mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    face_result = landmarker.detect(mp_image)
    
    if face_result.face_landmarks:
        face_count = len(face_result.face_landmarks)
        
        # 1. Multiple Face
        multiple_face_warning = check_multiple_faces(face_count)
        if multiple_face_warning:
            active_warnings.append(multiple_face_warning)

        landmarks = face_result.face_landmarks[0]
        blendshapes = face_result.face_blendshapes[0]

        # 2. Eye Tracking
        eye_warning = track_eye(blendshapes)
        if eye_warning:
            active_warnings.append(eye_warning)

        # 3. Mouth Opening
        mouth_warning = mouth_tracker.detect_mouth_opening(blendshapes)
        if mouth_warning:
            active_warnings.append(mouth_warning)

        # 4. Head Pose
        head_pose_warning = estimate_head_pose(landmarks, w, h)
        if head_pose_warning:
            active_warnings.append(head_pose_warning)
    else:
        active_warnings.append("No Person Detected!")

    # --- DISPLAY & LOG WARNINGS ---
    for i, warning in enumerate(active_warnings):
        color = (255, 0, 255) if ("AUDIO" in warning or "KEYBOARD" in warning) else (0, 0, 255)
        if "Calibrating" in warning: color = (255, 255, 0)
        cv2.putText(frame, f"WARNING: {warning}", (20, 50 + (i * 35)), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    # --- LOGGING LOGIC: INSTANT VS COOLDOWN ---
    high_priority = [w for w in active_warnings if "AUDIO" in w or "KEYBOARD" in w]
    critical_visual = [w for w in active_warnings if "AUDIO" not in w and "KEYBOARD" not in w and "Calibrating" not in w]

    # 1. Instant Log for Hardware/Audio (Ensures every keystroke is caught)
    if high_priority:
        log_message = " | ".join(high_priority)
        logging.info(log_message)
        print(f"INSTANT LOG: {log_message}")

    # 2. Cooldown Log for Visuals (Prevents log bloat from constant head/eye movement)
    if critical_visual and (current_time - last_logged_time > log_cooldown):
        log_message = " | ".join(critical_visual)
        logging.info(log_message)
        print(f"COOLDOWN LOG: {log_message}")
        last_logged_time = current_time

    cv2.imshow('AI Exam Proctoring', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# --- SHUTDOWN RESOURCES ---
audio_tracker.stop() 
keyboard_tracker.stop() 
cap.release()
cv2.destroyAllWindows()

# --- 5. END SESSION & CALCULATE DURATION ---
session_end_time = time.time()
duration_seconds = int(session_end_time - session_start_time)
mins, secs = divmod(duration_seconds, 60)
hours, mins = divmod(mins, 60)
duration_str = f"{hours}h {mins}m {secs}s" if hours > 0 else f"{mins} minutes, {secs} seconds"

logging.info(f"*** SECTION END: SESSION {section_number} | DURATION: {duration_str} ***")
logging.info("") 

print(f"\nSystem successfully shut down. Session {section_number} logged.")