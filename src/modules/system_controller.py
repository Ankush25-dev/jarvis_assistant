import subprocess
from utils.logger import logger

def open_browser():
    """Opens the default web browser (Firefox on Fedora) in the background."""
    try:
        # subprocess.Popen runs the command in a NON-BLOCKING way.
        # It's like typing 'firefox' in the terminal and pressing enter.
        subprocess.Popen(['firefox'])
        
        logger.info("Successfully launched Firefox via subprocess.")
        return "Opening Firefox now."
    
    except Exception as e:
        # If Firefox isn't installed or something breaks, we catch the error here
        logger.error(f"Failed to open browser. Error: {e}")
        return "I encountered an error trying to open the browser."