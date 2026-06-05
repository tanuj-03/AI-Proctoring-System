import cv2
import numpy as np

def estimate_head_pose(landmarks, frame_width, frame_height):
    """Calculates where the head is pointing using 3D matrix math."""
    image_points = np.array([
        (landmarks[1].x * frame_width, landmarks[1].y * frame_height),     # Nose
        (landmarks[152].x * frame_width, landmarks[152].y * frame_height), # Chin
        (landmarks[33].x * frame_width, landmarks[33].y * frame_height),   # Left Eye
        (landmarks[263].x * frame_width, landmarks[263].y * frame_height), # Right Eye
        (landmarks[61].x * frame_width, landmarks[61].y * frame_height),   # Left Mouth
        (landmarks[291].x * frame_width, landmarks[291].y * frame_height)  # Right Mouth
    ], dtype="double")

    # Generic 3D face model points
    model_points = np.array([
        (0.0, 0.0, 0.0), (0.0, -330.0, -65.0), (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0), (-150.0, -150.0, -125.0), (150.0, -150.0, -125.0)
    ])

    camera_matrix = np.array([[frame_width, 0, frame_width / 2], [0, frame_width, frame_height / 2], [0, 0, 1]], dtype="double")
    dist_coeffs = np.zeros((4, 1))

    _, rotation_vector, _ = cv2.solvePnP(model_points, image_points, camera_matrix, dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
    rmat, _ = cv2.Rodrigues(rotation_vector)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

    pitch = angles[0] * 360 # Looking up/down
    yaw = angles[1] * 360   # Looking left/right
    
    if abs(pitch) > 15 or abs(yaw) > 20:
        return "Head Turned Away"
    return None