from utils.logger import logger

# --- IMPORT REAL MODULES ---
from modules.system_controller import open_browser
from modules.system_monitor import check_ram  
from modules.web_fetcher import fetch_headline  # <-- NEW IMPORT

# --- MOCK MODULES (To be replaced later) ---
def get_time():
    return "The time is currently 12:00 PM (Simulated)."

# --- CORE SYSTEM (The Hub) ---

def main():
    logger.info("Jarvis system initializing...")
    print("Available commands: 'time', 'browser', 'ram', 'exit'.\n") # Updated print

    command_router = {
        "time": get_time,
        "browser": open_browser,
        "ram": check_ram,  
        "news": fetch_headline
    }

    while True:
        user_input = input("You: ").lower().strip()

        if user_input in ['exit', 'quit']:
            logger.info("Shutting down systems. Goodbye!")
            break 

        if user_input in command_router:
            action_function = command_router[user_input]
            response = action_function()
            logger.info(f"Executed command: {user_input}")
            print(f"Jarvis: {response}\n")
        
        else:
            logger.warning(f"Unknown command attempted: '{user_input}'")
            print(f"Jarvis: I don't have a module to handle '{user_input}' yet.\n")

if __name__ == "__main__":
    main()