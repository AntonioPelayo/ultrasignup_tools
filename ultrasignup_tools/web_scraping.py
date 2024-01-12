import requests
from bs4 import BeautifulSoup

def get_wepbage_soup(url):
    """
    Get the soup object for the webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        BeautifulSoup: The soup object.
    """
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    return soup