import subprocess
import webbrowser
import os
import urllib.parse
import urllib.request
import re
from utils.logger import logger

def open_web_browser(url: str = "https://www.google.com") -> str:
    """
    Opens the default web browser to a specific URL.

    Args:
        url (str): The URL to open in the browser (e.g. 'https://www.google.com').
    """
    try:
        # Ensure url starts with http:// or https:// so webbrowser treats it correctly
        if not url.startswith(("http://", "https://")):
            url = "https://" + url
            
        webbrowser.open(url)
        logger.info(f"Successfully opened browser to URL: {url}")
        return f"Opening web browser to {url} now."
    except Exception as e:
        logger.error(f"Failed to open web browser. Error: {e}")
        return f"I encountered an error trying to open the web browser to {url}."

def open_local_path(path: str) -> str:
    """
    Opens a specific local file or directory on the system.

    Args:
        path (str): The absolute or relative path to the local file or directory.
    """
    try:
        # Expand user directory (e.g., '~' to '/home/user')
        expanded_path = os.path.expanduser(path)
        resolved_path = os.path.abspath(expanded_path)
        
        if not os.path.exists(resolved_path):
            logger.warning(f"Attempted to open non-existent local path: {resolved_path}")
            return f"The path {path} does not exist on this system."
            
        # Use xdg-open to open it with Fedora's default file manager or app
        subprocess.Popen(['xdg-open', resolved_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        logger.info(f"Successfully opened local path: {resolved_path}")
        return f"Opening local path {path} now."
    except Exception as e:
        logger.error(f"Failed to open local path. Error: {e}")
        return f"I encountered an error trying to open local path {path}."

def play_youtube_music(search_query: str) -> str:
    """
    Searches for a song, artist, or music track on YouTube and plays the first video result.

    Args:
        search_query (str): The name of the song, artist, or music to play (e.g. 'shape of you').
    """
    try:
        query_encoded = urllib.parse.quote(search_query)
        url = f"https://www.youtube.com/results?search_query={query_encoded}"
        
        # Add a custom User-Agent to avoid YouTube blocking requests
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            
        video_ids = re.findall(r"watch\?v=([a-zA-Z0-9_-]{11})", html)
        
        if video_ids:
            # Open the first video directly with autoplay parameter
            first_video_url = f"https://www.youtube.com/watch?v={video_ids[0]}&autoplay=1"
            webbrowser.open(first_video_url)
            logger.info(f"Successfully playing YouTube music for query '{search_query}': {first_video_url}")
            return f"Playing '{search_query}' on YouTube now."
        else:
            # Fallback to opening the search page
            webbrowser.open(url)
            logger.info(f"No direct video found. Opened search results page for '{search_query}'.")
            return f"Opening YouTube search results for '{search_query}'."
            
    except Exception as e:
        logger.error(f"Failed to play YouTube music. Error: {e}")
        # Fallback to search query results page directly via webbrowser
        try:
            fallback_url = f"https://www.youtube.com/results?search_query={urllib.parse.quote(search_query)}"
            webbrowser.open(fallback_url)
            return f"Opening YouTube search for '{search_query}' due to an error."
        except Exception:
            return "I encountered an error trying to play YouTube music."