import logging
import os

def setup_logger():
    # 1. Create a logs directory if it doesn't exist
    log_dir = "data/logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 2. Set up the basic configuration for our logger
    log_file = os.path.join(log_dir, "jarvis.log")
    
    # 3. Configure the format of the log message
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file), # Saves to a file
            logging.StreamHandler()        # Also prints to the terminal
        ]
    )
    
    return logging.getLogger("JarvisLogger")

# Create a single instance of the logger to be used everywhere
logger = setup_logger()