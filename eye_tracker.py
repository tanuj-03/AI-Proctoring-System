def track_eye(blendshapes):
    """Checks if the candidate is looking away (left, right, or up)."""
    def get_blendshape(name):
        for category in blendshapes:
            if category.category_name == name:
                return category.score
        return 0.0

    look_left = get_blendshape('eyeLookOutLeft') > 0.5 
    look_right = get_blendshape('eyeLookInLeft') > 0.5
    look_up = get_blendshape('eyeLookUpLeft') > 0.4
    
    if look_left or look_right or look_up:
        return "Suspicious Eye Movement (Looking away)"
    return None