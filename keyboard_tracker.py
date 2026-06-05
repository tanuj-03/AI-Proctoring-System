from pynput import keyboard

class KeyboardTracker:
    def __init__(self):
        """
        Initializes the keyboard listener in a separate background thread
        so it doesn't interfere with the main camera loop.
        """
        self.current_warnings = []
        # Start the listener in a non-blocking background thread
        self.listener = keyboard.Listener(on_press=self._on_press)
        self.listener.start()

    def _on_press(self, key):
        """
        Callback function that triggers every time a key is pressed.
        Captures the specific key name for logging.
        """
        try:
            # Check if the key is a standard character (a, b, c, 1, 2, 3)
            if hasattr(key, 'char') and key.char is not None:
                key_name = key.char
            else:
                # Handle special keys (e.g., Key.ctrl_l, Key.enter, Key.shift)
                # We strip the "Key." prefix to make the logs cleaner
                key_name = str(key).replace("Key.", "")
            
            # Add the specific button press to our warning queue
            self.current_warnings.append(f"KEYBOARD FLAG: Key '{key_name}' pressed")
            
        except Exception:
            # Prevent the listener from crashing if a weird system key is pressed
            pass

    def get_warnings(self):
        """
        Returns the list of key presses captured since the last check
        and clears the queue to prevent duplicate logs.
        """
        warnings = self.current_warnings.copy()
        self.current_warnings.clear()
        return warnings

    def stop(self):
        """
        Safely shuts down the keyboard listener when the main program exits.
        """
        self.listener.stop()