import speech_recognition as sr

class AudioTracker:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Your specific list of flagged keywords
        self.suspicious_keywords = [
            "answer", "google", "help", "what is", "chatgpt", 
            "gpt", "gemini", "ai", "option number", "which option"
        ]
        
        self.current_warnings = []
        
        # Briefly calibrate to the room's ambient noise
        print("Calibrating microphone for background noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
        # Start listening in the background (non-blocking)
        # This automatically calls self._callback whenever a phrase finishes
        self.stop_listening = self.recognizer.listen_in_background(
            self.microphone, self._callback
        )
        print("Audio tracking initialized.")

    def _callback(self, recognizer, audio):
        """This function runs invisibly in the background when audio is detected."""
        try:
            # We use Google's free web API here for fast, lightweight transcription.
            transcript = recognizer.recognize_google(audio).lower()
            
            # Check if any of the keywords exist in the transcript
            found_keywords = [kw for kw in self.suspicious_keywords if kw in transcript]
            
            if found_keywords:
                # Format a warning with the exact transcript
                warning_msg = f"AUDIO FLAG: Heard '{', '.join(found_keywords)}' (Transcript: '{transcript}')"
                self.current_warnings.append(warning_msg)
                
        except sr.UnknownValueError:
            # Audio wasn't clear enough to understand
            pass 
        except sr.RequestError:
            # Could not reach the API
            pass

    def get_warnings(self):
        """Pulls the latest audio warnings into the main loop and clears the queue."""
        warnings = self.current_warnings.copy()
        self.current_warnings.clear()
        return warnings

    def stop(self):
        """Safely shuts down the microphone thread."""
        self.stop_listening(wait_for_stop=False)