import subprocess
import re
import sys
import select
import threading
import os
# pyrefly: ignore [missing-import]
import speech_recognition as sr
# pyrefly: ignore [missing-import]
from gtts import gTTS
from utils.logger import logger

def contains_hindi(text: str) -> bool:
    """Checks if a string contains Hindi (Devanagari) characters."""
    return bool(re.search(r'[\u0900-\u097F]', text))

def clean_text_for_speech(text: str) -> str:
    """Strips out markdown symbols, URLs, and extra spaces for clear TTS."""
    text = text.replace("Jarvis:", "").strip()
    
    # Remove URLs
    text = re.sub(r'https?://\S+|www\.\S+', '', text)
    
    # Remove Markdown characters
    text = re.sub(r'[*#`_~>\[\]\(\)\{\}\+\-\=]', '', text)
    
    # Replace multiple whitespaces/newlines with a single space
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

class Speaker:
    def __init__(self):
        """Initializes the gTTS speech engine."""
        self.current_process = None
        self.temp_file = "data/temp_speech.mp3"
        
        # Ensure the data directory exists
        os.makedirs(os.path.dirname(self.temp_file), exist_ok=True)
        
        logger.info("gTTS Text-to-Speech engine initialized successfully.")

    def _voice_interrupt_worker(self, stop_event: threading.Event):
        """Listens to the microphone for interrupt phrases and stops playback if heard."""
        recognizer = sr.Recognizer()
        # Set static energy threshold to respond quickly
        recognizer.energy_threshold = 300
        recognizer.dynamic_energy_threshold = False

        try:
            with sr.Microphone() as source:
                # Loop until the stop event is set or the process finishes
                while not stop_event.is_set() and self.current_process and self.current_process.poll() is None:
                    try:
                        # Listen for a very short duration (1.5s limit) to respond quickly
                        audio = recognizer.listen(source, timeout=0.5, phrase_time_limit=1.5)
                        
                        # Use Google Speech Recognition to transcribe
                        text = recognizer.recognize_google(audio).lower().strip()
                        
                        # Check for interruption keywords
                        interrupt_keywords = ["stop", "wait", "hold on", "quiet", "shh", "shush", "pause"]
                        if any(kw in text for kw in interrupt_keywords):
                            logger.info(f"Voice interruption triggered by phrase: '{text}'")
                            self.stop()
                            print("\n[Jarvis speech interrupted by voice]")
                            break
                            
                    except sr.WaitTimeoutError:
                        continue
                    except (sr.UnknownValueError, sr.RequestError):
                        continue
                    except Exception as e:
                        logger.error(f"Error inside voice interrupt loop: {e}")
                        break
        except Exception as e:
            logger.error(f"Failed to initialize microphone in voice interrupter: {e}")

    def speak(self, text: str, wait: bool = True):
        """Converts text to speech cleanly using gTTS and ffplay."""
        self.stop()

        clean_text = clean_text_for_speech(text)
        if not clean_text:
            return

        try:
            # Detect language: use Hindi ('hi') if Hindi characters are present, otherwise English ('en')
            lang = 'hi' if contains_hindi(clean_text) else 'en'
            
            # Generate speech audio using gTTS
            tts = gTTS(text=clean_text, lang=lang)
            tts.save(self.temp_file)
            
            # Play the audio using ffplay (non-blocking subprocess)
            self.current_process = subprocess.Popen(
                ["ffplay", "-nodisp", "-autoexit", "-loglevel", "quiet", self.temp_file],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            
            if self.current_process:
                # Start voice interruption background thread
                stop_event = threading.Event()
                interrupt_thread = threading.Thread(
                    target=self._voice_interrupt_worker,
                    args=(stop_event,),
                    daemon=True
                )
                interrupt_thread.start()
                
                try:
                    if wait:
                        # Poll process while listening for an instant Enter key interrupt
                        while self.current_process.poll() is None:
                            # Check if the user pressed Enter in the active terminal
                            rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
                            if rlist:
                                sys.stdin.readline()  # Consume the keypress
                                self.stop()
                                print("\n[Jarvis speech interrupted by keyboard]")
                                break
                finally:
                    # Clean up the background thread
                    stop_event.set()
                    # Join quickly so we don't hold up execution
                    interrupt_thread.join(timeout=0.2)

        except Exception as e:
            logger.error(f"Failed to execute TTS playback: {e}")

    def stop(self):
        """Instantly terminates any ongoing speech process."""
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=0.2)
            except Exception:
                try:
                    self.current_process.kill()
                except Exception as e:
                    logger.error(f"Error stopping speech process: {e}")
            finally:
                self.current_process = None
                
        # Try to remove the temp file to avoid leaving stale state
        if os.path.exists(self.temp_file):
            try:
                os.remove(self.temp_file)
            except Exception:
                pass

speaker = Speaker()