# Import our new custom logger
from utils.logger import logger

# --- MODULES (The Spokes) ---

def get_time():
    return "The time is currently 12:00 PM (Simulated)."

def open_browser():
    return "Opening your web browser now (Simulated)."

# --- CORE SYSTEM (The Hub) ---

def main():
    logger.info("Jarvis system initializing...")
    print("Available commands: 'time', 'browser', 'exit'.\n")

    command_router = {
        "time": get_time,
        "browser": open_browser
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