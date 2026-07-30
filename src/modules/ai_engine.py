import os
# pyrefly: ignore [missing-import]
from google import genai
# pyrefly: ignore [missing-import]
from google.genai import types
from utils.logger import logger
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv

# Import tools to be exposed to Gemini
from modules.system_controller import open_web_browser, open_local_path, play_youtube_music
from modules.system_monitor import check_ram
from modules.web_fetcher import fetch_headline

load_dotenv()

class AIEngine:
    def __init__(self):
        """Initializes the connection to the Gemini API."""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            
            if not api_key:
                logger.error("GEMINI_API_KEY not found in environment variables.")
                self.client = None
                return

            self.client = genai.Client()
            logger.info("Successfully connected to the Google Gemini API.")
            
        except Exception as e:
            logger.error(f"Failed to initialize Gemini API. Error: {e}")
            self.client = None

    def generate_response(self, contents):
        """
        Sends the contents to Gemini with Tools registered and automatic calling disabled.
        
        Args:
            contents: A string prompt, or a list of contents representing conversation history.
            
        Returns:
            The raw response object from the Gemini API, or None if the call fails.
        """
        if not self.client:
            logger.error("Gemini client not initialized.")
            return None

        try:
            response = self.client.models.generate_content(
                model='gemini-3.5-flash-lite',
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=(
                        "You are Jarvis, a concise voice assistant. "
                        "Keep all responses short, natural, and conversational (maximum 2 to 3 sentences). "
                        "Do NOT use markdown, bold text, bullet points, lists, or special symbols."
                    ),
                    # Register tools
                    tools=[open_web_browser, open_local_path, play_youtube_music, check_ram, fetch_headline],
                    # Disable automatic function calling so we execute tools manually in main.py
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
                )
            )
            return response
            
        except Exception as e:
            logger.error(f"AI API call failed. Error: {e}")
            return None

ai_core = AIEngine()