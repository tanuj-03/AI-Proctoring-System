def check_multiple_faces(face_count):
    """Returns a warning string if multiple faces are detected, else None."""
    if face_count > 1:
        return f"Multiple Persons Detected! Count: {face_count}"
    return None