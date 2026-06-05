class MouthTracker:
    def __init__(self):
        self.frames_processed = 0
        self.baseline_mouth_scores = []
        self.baseline_mouth = 0.0

    def detect_mouth_opening(self, blendshapes):
        """Calculates distance between lips and checks against baseline."""
        def get_blendshape(name):
            for category in blendshapes:
                if category.category_name == name:
                    return category.score
            return 0.0

        jaw_open = get_blendshape('jawOpen')
        
        # Calibration phase (first 30 frames)
        if self.frames_processed < 30:
            self.baseline_mouth_scores.append(jaw_open)
            self.frames_processed += 1
            return "Calibrating baseline mouth position..."
        
        # Calculate baseline once
        if self.baseline_mouth == 0:
            self.baseline_mouth = sum(self.baseline_mouth_scores) / len(self.baseline_mouth_scores)
        
        # Check against baseline
        if jaw_open > self.baseline_mouth + 0.15:
            return "Talking / Mouth Open Detected"
            
        return None