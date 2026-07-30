import requests
from bs4 import BeautifulSoup
from utils.logger import logger

def fetch_headline():
    """Silently fetches the top news headline from the web."""
    try:
        # 1. THE REQUEST: Go to the website. 
        # timeout=5 means "if the Wi-Fi is bad, give up after 5 seconds instead of freezing forever."
        url = "https://lite.cnn.com/"  # We use the 'lite' version because it has very clean, basic HTML
        response = requests.get(url, timeout=5)
        
        # This tells Python to raise an error if the website is down (e.g., Error 404)
        response.raise_for_status() 

        # 2. THE TRANSLATOR: Turn the messy HTML into a BeautifulSoup object
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 3. THE EXTRACTION: Find the first list item (<li>) on the page, which holds the top headline
        first_headline = soup.find('li').text
        
        logger.info("Successfully fetched the top headline from CNN Lite.")
        return f"The top headline right now is: {first_headline}"

    except Exception as e:
        # If the Wi-Fi is off, or the site is down, we land safely here.
        logger.error(f"Failed to fetch webpage. Error: {e}")
        return "I am having trouble connecting to the internet right now."