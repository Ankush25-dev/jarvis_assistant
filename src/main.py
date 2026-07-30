# --- MODULES (The Spokes) ---
# For now, these are just "dummy" functions. Later, they will do real work.

def get_time():
    return "Jarvis: The time is currently 12:00 PM (Simulated)."

def open_browser():
    return "Jarvis: Opening your web browser now (Simulated)."

# --- CORE SYSTEM (The Hub) ---

def main():
    print("Jarvis system initializing...")
    print("Available commands: 'time', 'browser', 'exit'.\n")

    # The Strategy Pattern (Command Router)
    # The KEY is the user's text. The VALUE is the function to run.
    # Notice there are no () after get_time or open_browser!
    command_router = {
        "time": get_time,
        "browser": open_browser
    }

    while True:
        # 1. READ & SANITIZE: Get text, make it lowercase, and remove extra spaces
        user_input = input("You: ").lower().strip()

        # 2. EVALUATE: Check for system shutdown
        if user_input in ['exit', 'quit']:
            print("Jarvis: Shutting down systems. Goodbye!")
            break 

        # 3. ROUTE: Check if the command exists in our dictionary
        if user_input in command_router:
            # Grab the function out of the dictionary
            action_function = command_router[user_input]
            
            # Execute the function by adding () and save what it returns
            response = action_function()
            
            # 4. PRINT: Output the result
            print(response + "\n")
        
        else:
            print(f"Jarvis: I don't have a module to handle '{user_input}' yet.\n")

if __name__ == "__main__":
    main()