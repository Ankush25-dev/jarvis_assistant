# pyrefly: ignore [missing-import]
import speech_recognition as sr
from utils.logger import logger

def listen_for_command():
    """Listens to the microphone and converts spoken words to text."""
    # Initialize the recognizer
    recognizer = sr.Recognizer()
    
    with sr.Microphone() as source:
        print("\nJarvis: Adjusting for background noise... please wait.")
        # This listens to the room for 1 second to figure out how loud your AC/fan is
        recognizer.adjust_for_ambient_noise(source, duration=1)
        
        print("Jarvis: Listening! (Speak now...)")
        try:
            # Listen to the microphone. 
            # timeout: gives up if you don't say anything for 5 seconds.
            # phrase_time_limit: stops listening after 5 seconds of speaking.
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            
            print("Jarvis: Processing...")
            
            # Send the audio to Google's free API to translate it to text
            text = recognizer.recognize_google(audio)
            
            logger.info(f"Microphone captured: '{text}'")
            return text.lower().strip()
            
        except sr.WaitTimeoutError:
            # You didn't say anything
            return ""
        except sr.UnknownValueError:
            # You spoke, but the AI couldn't understand the words
            logger.warning("Speech recognition could not understand audio.")
            print("Jarvis: I didn't quite catch that.")
            return ""
        except sr.RequestError as e:
            # Wi-Fi is down or Google's API blocked us
            logger.error(f"Could not request results from Speech Recognition service; {e}")
            print("Jarvis: My speech recognition service is currently offline.")
            return ""
        except Exception as e:
            logger.error(f"Unexpected microphone error: {e}")
            return ""