import requests
from bs4 import BeautifulSoup
from selenium import webdriver

def load_dynamic_page(url):
    """
    Use Selenium to get the soup object for the webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        BeautifulSoup: The soup object.
    """
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.close()

    return soup

def get_webpage_soup(url):
    """
    Get the soup object for the webpage.

    Args:
        url (str): The URL of the webpage.

    Returns:
        BeautifulSoup: The soup object.
    """
    if 'results_participant' in url:
        soup = load_dynamic_page(url)
    else:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

    return soup

def save_soup(soup, path='soup.html'):
    """
    Save the soup object to a temporary HTML file.

    Args:
        soup (BeautifulSoup): The soup object.

    Returns:
        None
    """
    with open(path, 'w') as f:
        f.write(str(soup))

def tag_exists(soup, tag, attribute, identifier):
    """
    Check if the tag exists in the soup object.

    Args:
        soup (BeautifulSoup): The soup object.
        tag (str): The tag type.
        attribute (str): The tag attribute.
        identifier (str): The tag identifier.

    Returns:
        bool: True if the tag exists, False otherwise.
    """
    return soup.find(tag, {attribute: identifier}) is not None
