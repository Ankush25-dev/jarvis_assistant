import psutil
from utils.logger import logger

def check_ram():
    """Checks the system's available RAM and returns a readable string."""
    try:
        # psutil.virtual_memory() returns a tuple of memory stats
        memory_info = psutil.virtual_memory()
        
        # The memory is in bytes. We divide by (1024^3) to convert it to Gigabytes.
        # We use round(..., 2) to keep it to two decimal places.
        available_gb = round(memory_info.available / (1024 ** 3), 2)
        total_gb = round(memory_info.total / (1024 ** 3), 2)
        
        logger.info(f"Checked RAM: {available_gb}GB free out of {total_gb}GB")
        
        return f"You have {available_gb} GB of free RAM available out of {total_gb} GB."
        
    except Exception as e:
        logger.error(f"Failed to check RAM. Error: {e}")
        return "I am unable to access the system memory statistics right now."