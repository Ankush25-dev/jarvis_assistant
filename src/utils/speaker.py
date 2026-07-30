# pyrefly: ignore [missing-import]
import pyttsx3
from utils.logger import logger

class Speaker:
    def __init__(self):
        """Initializes the offline Text-to-Speech engine."""
        try:
            self.engine = pyttsx3.init()
            
            # --- NEW VOICE SELECTION CODE ---
            # Get the list of all available voices on your Fedora system
            voices = self.engine.getProperty('voices')
            
            # Change the number in the brackets to swap voices.
            # [0] is usually the default male.
            # [1] or [2] is usually a female voice or a different accent.
            if len(voices) > 1:
                self.engine.setProperty('voice', voices[4].id) 
            # --------------------------------
            
            # Set speaking speed (Rate). 175 is natural, lower is slower.
            self.engine.setProperty('rate', 170)
            
            # Set volume level (0.0 to 1.0)
            self.engine.setProperty('volume', 1.0)
            
            logger.info("Text-to-Speech engine initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize TTS engine. Error: {e}")
            self.engine = None
    def speak(self, text: str):
        """Converts text to audible speech."""
        if not self.engine:
            logger.warning("TTS engine not available. Skipping speech.")
            return

        try:
            # Clean up the response for cleaner speech (remove newlines or extra text markers)
            clean_text = text.replace("Jarvis:", "").strip()
            
            # Queue the text to be spoken
            self.engine.say(clean_text)
            
            # Process and play the audio (Blocking briefly while speaking)
            self.engine.runAndWait()
            
        except Exception as e:
            logger.error(f"Error while attempting to speak: {e}")

# Create a single instance that the whole app can share
speaker = Speaker()