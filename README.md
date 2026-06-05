# AI-Driven Exam Proctoring System

## 1. Project Description

This project is a comprehensive, multi-modal AI Proctoring solution designed to maintain exam integrity in remote environments. By combining Computer Vision, Audio Analysis, and Hardware Monitoring, the system creates a robust "Digital Invigilator." It identifies suspicious behaviors - such as looking away, using a mobile phone, talking, or unauthorized keyboard usage - and generates a detailed, time-stamped PDF report for every session.

---

## 2. Prerequisites

To run this repository, you need:

- Python 3.10+
- A working Webcam
- A working Microphone

**Install dependencies via:**

```bash
pip install opencv-python mediapipe ultralytics speechrecognition pyaudio pynput fpdf2
```

> **AI Models:** The system automatically downloads the necessary `face_landmarker.task` and `yolov8n.pt` files upon the first run.

---

## 3. Features

- **Visual Face Analysis** - Detects multiple people, eye-gaze direction, and head pose orientation.
- **Mouth / Speech Tracking** - Calibrates to the user's face to detect mouth opening (talking) and uses Speech-to-Text to flag keywords like "ChatGPT" or "Google."
- **Object Detection** - Uses YOLOv8 to identify and flag mobile phones in the video feed.
- **Hardware Monitoring** - A background listener captures and logs every keyboard stroke (e.g., `Key 'ctrl' pressed`) in real-time.
- **Smart Logging** - Visual flags use a 3-second cooldown to keep logs clean, while Hardware/Audio flags are logged instantly for accuracy.
- **PDF Exporter** - A dedicated tool to convert text-based session logs into professional, wrapped-text PDF reports.

---

## 4. File Structure

| File | Description |
|------|-------------|
| `main.py` | Central hub orchestrating the camera loop and logging logic |
| `multiple_face_detection.py` | Module for multi-face visual analysis |
| `eye_tracker.py` | Eye-gaze detection module |
| `mouth_opening_detector.py` | Mouth opening / talking detection |
| `head_pose_estimation.py` | Head orientation analysis |
| `mobile_phone_detector.py` | Integrates YOLOv8 for object detection |
| `audio_transcriber.py` | Background speech-to-text and keyword flagging |
| `keyboard_tracker.py` | Background thread for capturing hardware keypresses |
| `export_pdf.py` | Converts session-specific logs into formatted PDF files |
| `suspicious_events.log` | Persistent storage for all flagged activities |

---

## 5. System Architecture

The system utilizes a **Modular Asynchronous Architecture**:

1. **Primary Thread** - Runs the OpenCV camera feed and MediaPipe Face Landmarking at high FPS.
2. **Background Threads** - Audio transcription and Keyboard listening run on separate threads to prevent the video feed from lagging.
3. **Data Aggregation** - The `main.py` orchestrator pulls data from all modules, filters them based on priority (Instant vs. Cooldown), and writes to a shared log file.
4. **Reporting Layer** - The PDF exporter reads the log file, parses specific sections using session markers, and applies a text-wrapping algorithm to generate clean documents.

---

## Built By
- **[Vijay Dayakaran](https://www.linkedin.com/in/vijay-dayakaran/)**
