# pyrefly: ignore [missing-import]
from google.genai import types
from utils.logger import logger
from utils.speaker import speaker
from utils.listener import listen_for_command
from modules.ai_engine import ai_core

# Import tools for mapping
from modules.system_controller import open_web_browser, open_local_path, play_youtube_music
from modules.system_monitor import check_ram
from modules.web_fetcher import fetch_headline

# Map tool names to actual python functions
tool_map = {
    "open_web_browser": open_web_browser,
    "open_local_path": open_local_path,
    "play_youtube_music": play_youtube_music,
    "check_ram": check_ram,
    "fetch_headline": fetch_headline
}


def main():
    logger.info("Jarvis system initializing (AI Core Active)...")
    
    welcome_msg = "Jarvis system online. AI Brain connected. How can I help you?"
    print(f"Jarvis: {welcome_msg}\n")
    # wait=True ensures he finishes the welcome message before listening
    speaker.speak(welcome_msg, wait=True)

    while True:
        # 1. Listen (Ears)
        user_input = listen_for_command()

        if not user_input:
            continue
            
        print(f"You said: {user_input}")

        # Clean punctuation out of the speech text
        clean_input = user_input.strip(".,!? ").lower()

        # Shutdown check
        exit_keywords = ['exit', 'quit', 'shut down', 'shutdown', 'stop']
        if any(keyword in clean_input for keyword in exit_keywords):
            shutdown_msg = "Shutting down systems. Goodbye!"
            logger.info(shutdown_msg)
            print(f"Jarvis: {shutdown_msg}")
            # wait=True ensures he finishes his goodbye before the script dies
            speaker.speak(shutdown_msg, wait=True)
            break 

        # 2. Think (AI Brain)
        print("Jarvis: Thinking...")
        response = ai_core.generate_response(user_input)
        
        if not response:
            error_msg = "I'm having trouble connecting to my AI core."
            print(f"Jarvis: {error_msg}\n")
            speaker.speak(error_msg, wait=True)
            continue

        # Check for function calls
        if response.function_calls:
            function_call = response.function_calls[0]
            func_name = function_call.name
            func_args = function_call.args
            
            logger.info(f"Gemini requested tool call: {func_name} with arguments: {func_args}")
            print(f"Jarvis: Running tool '{func_name}'...")
            
            # Execute the function
            if func_name in tool_map:
                try:
                    # Execute with arguments unpacked from Gemini's call
                    result = tool_map[func_name](**func_args)
                except Exception as e:
                    logger.error(f"Error executing tool {func_name}: {e}")
                    result = f"Error executing tool {func_name}: {e}"
            else:
                result = f"Error: Tool '{func_name}' is not registered."
                logger.error(result)
                
            print(f"Tool result: {result}")
            
            # Prepare the function response to send back to the model
            function_response_part = types.Part.from_function_response(
                name=func_name,
                response={'result': result}
            )
            
            # Send the history + tool response back to Gemini to get the conversational answer
            final_response = ai_core.generate_response([
                types.Content(role='user', parts=[types.Part.from_text(text=user_input)]),
                response.candidates[0].content,
                types.Content(role='tool', parts=[function_response_part])
            ])
            
            if final_response and final_response.text:
                answer = final_response.text
            else:
                answer = "I executed the tool but was unable to generate a response."
        else:
            answer = response.text if response.text else "I didn't receive a response from my AI engine."

        # 3. Speak (Mouth)
        print(f"Jarvis: {answer}\n")
        # wait=True ensures he finishes speaking before the mic turns back on
        speaker.speak(answer, wait=True)

if __name__ == "__main__":
    main()