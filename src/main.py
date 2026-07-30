from utils.logger import logger
from utils.speaker import speaker  # <-- NEW IMPORT

# --- IMPORT REAL MODULES ---
from modules.system_controller import open_browser
from modules.system_monitor import check_ram
from modules.web_fetcher import fetch_headline

# --- MOCK MODULES ---
def get_time():
    return "The time is currently 12:00 PM (Simulated)."

# --- CORE SYSTEM (The Hub) ---

def main():
    logger.info("Jarvis system initializing...")
    
    welcome_msg = "Jarvis system initializing. All modules online."
    print(f"Jarvis: {welcome_msg}\n")
    print("Available commands: 'time', 'browser', 'ram', 'news', 'exit'.\n")
    
    # Speak the welcome message!
    speaker.speak(welcome_msg)

    command_router = {
        "time": get_time,
        "browser": open_browser,
        "ram": check_ram,
        "news": fetch_headline
    }

    while True:
        user_input = input("You: ").lower().strip()

        if user_input in ['exit', 'quit']:
            shutdown_msg = "Shutting down systems. Goodbye!"
            logger.info(shutdown_msg)
            print(f"Jarvis: {shutdown_msg}")
            speaker.speak(shutdown_msg)
            break 

        if user_input in command_router:
            action_function = command_router[user_input]
            response = action_function()
            logger.info(f"Executed command: {user_input}")
            
            # Print AND Speak the response
            print(f"Jarvis: {response}\n")
            speaker.speak(response)
        
        else:
            unknown_msg = "I don't have a module to handle that command yet."
            logger.warning(f"Unknown command attempted: '{user_input}'")
            print(f"Jarvis: {unknown_msg}\n")
            speaker.speak(unknown_msg)

if __name__ == "__main__":
    main()