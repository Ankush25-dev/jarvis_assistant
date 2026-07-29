def main():
    # Greet the user when the program starts
    print("Jarvis system initializing...")
    print("Type 'exit' or 'quit' to shut down.\n")

    # This is the "Pulse" - an infinite loop keeping Jarvis alive
    while True:
        # 1. READ: Get text input from the user
        user_input = input("You: ")

        # 2. EVALUATE: Check if the user wants to shut down
        if user_input.lower() in ['exit', 'quit']:
            print("Jarvis: Shutting down systems. Goodbye!")
            break  # This command kills the infinite loop

        # 3. PRINT: Respond to the user
        print(f"Jarvis: You said '{user_input}', but my brain isn't connected yet!\n")

# This checks if we are running main.py directly
if __name__ == "__main__":
    main()