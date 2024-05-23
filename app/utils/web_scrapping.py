import time
import os
from pathlib import Path
from selenium.common import WebDriverException, NoSuchElementException, StaleElementReferenceException, \
    JavascriptException
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromeService
from urllib.request import urlretrieve
from pathlib import Path
from selenium.webdriver.remote.webelement import WebElement
from urllib.error import URLError, HTTPError, ContentTooShortError
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from app.utils.logging import setup_logging
setup_logging()

def initiate_chromedriver(webdriver_path=None, headless=False):
    """
    Initiates a Chrome WebDriver instance.

    Args:
        webdriver_path (str): Path to the ChromeDriver executable.
        headless (bool, optional): Run Chrome in headless mode (no GUI). Defaults to False.

    Returns:
        WebDriver: A WebDriver instance.
    """
    options=webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    try:
        if headless:
            options.add_argument("--headless=new")  # Use headless=new for better performance
        if webdriver_path is not None:
            service= Service(executable_path=webdriver_path,options=options)
        else:
            service= ChromeService(ChromeDriverManager().install(),options=options)
        driver = webdriver.Chrome(service=service, options=options)
        logging.info("WebDriver initiated successfully.")
        maximize_window(driver=driver)
        return driver
    except WebDriverException as e:
        logging.error(f"Error occurred while initiating the driver: {e}")
        return None

def open_page_url(driver, url):
    """
    Opens a URL in the WebDriver instance.

    Args:
        driver (WebDriver): A WebDriver instance.
        url (str): The URL to open.
    """
    try:
        driver.get(url)
        logging.info(f"Opened page URL: {url}")
        sleep(3)
    except WebDriverException as e:
        logging.error(f"Error occurred while opening the webpage: {e}")

def maximize_window(driver):
    """
    Maximizes the browser window.

    Args:
        driver (WebDriver): A WebDriver instance.
    """
    try:
        driver.maximize_window()
        logging.info("Browser window maximized successfully.")
    except WebDriverException as e:
        logging.error(f"Error maximizing browser window: {e}")


def find_elements(driver, by, value):
    """
    Finds elements on the page.

    Args:
        driver (WebDriver): A WebDriver instance.
        by (str): How to find elements (e.g., "ID", "NAME", "XPATH", "CSS_SELECTOR").
        value (str): The value to match (e.g., an ID, name, or XPath expression).

    Returns:
        list: A list of WebElement objects.
    """
    try:
        if by == "ID":
            elements = driver.find_elements(By.ID, value)
        elif by == "NAME":
            elements = driver.find_elements(By.NAME, value)
        elif by == "XPATH":
            elements = driver.find_elements(By.XPATH, value)
        elif by == "CSS_SELECTOR":
            elements = driver.find_elements(By.CSS_SELECTOR)
        else:
            raise ValueError(f"Invalid locator type: {by}")

        logging.info(f"Found {len(elements)} elements using '{by}' locator with value '{value}'")
        return elements

    except NoSuchElementException:
        logging.warning(f"No elements found using '{by}' locator with value '{value}'")
        return []  # Return an empty list if no elements are found

    except ValueError as e:
        logging.error(f"Invalid locator type: {e}")
        raise  # Re-raise the ValueError to indicate incorrect usage

def find_element(driver, by, value):
    """
        Finds a single element on the page.

        Args:
            driver (WebDriver): A WebDriver instance.
            by (str): How to find the element (e.g., "ID", "NAME", "XPATH", "CSS_SELECTOR").
            value (str): The value to match (e.g., an ID, name, or XPath expression).

        Returns:
            WebElement: The first WebElement object that matches the locator, or None if none is found.
    """

    try:
        if by == "ID":
            element = driver.find_element(By.ID, value)
        elif by == "NAME":
            element = driver.find_element(By.NAME, value)
        elif by == "XPATH":
            element = driver.find_element(By.XPATH, value)
        elif by == "CSS_SELECTOR":
            element = driver.find_element(By.CSS_SELECTOR, value)
        else:
            raise ValueError(f"Invalid locator type: {by}")

        logging.info(f"Found element using '{by}' locator with value '{value}'")
        return element

    except NoSuchElementException:
        logging.warning(f"No element found using '{by}' locator with value '{value}'")
        return None  # Return None if no element is found

    except ValueError as e:
        logging.error(f"Invalid locator type: {e}")
        raise  # Re-raise the ValueError to indicate incorrect usage

def scroll_into_view(driver, element):
    """
       Scrolls the given element into view.

       Args:
           driver (WebDriver): A WebDriver instance.
           element (WebElement): The element to scroll into view.
       """

    try:
        driver.execute_script("arguments[0].scrollIntoView();", element)
        logging.info(f"Scrolled element into view: {element.tag_name} with text '{element.text}'")  # Log success
    except StaleElementReferenceException:
        logging.warning("Element is no longer attached to the DOM. Cannot scroll.")
        # You might want to try to re-find the element or handle this situation differently
    except JavascriptException as e:
        logging.error(f"JavaScript error while scrolling: {e}")
        # Consider retrying or alternative scrolling mechanisms if the error is intermittent


def download_file(driver, query,filename=None):
    """
       Downloads a file from a URL

       Args:
           driver(WebDriver): A WebDriver Instance
           filename (str, optional): The filename to save as. Defaults to None (use the original filename).
       """
    images = find_elements(driver=driver, by="XPATH", value="//div[@jsname='dTDiAc']//div[@jsname='qQjpJ']//img")
    downloadsFolder = get_downloads_folder()
    mydict={}
    img_data=[]
    for image in images:
        scroll_into_view(driver=driver, element=image)
        url = get_element_attribute(element=image, attribute_name="src")
        if url is None:
            continue
        try:
            urlretrieve(url=url, filename=os.path.join(downloadsFolder,
                                                       f"{'_'.join(query.split(' '))}_{images.index(image)}.jpg"))
            logging.info(f"Successfully downloaded file from '{url}' and saved as {'_'.join(query.split(' '))}_{images.index(image)}.jpg}}")
            mydict={"Index":images.index(image),"url":url}
            img_data.append(mydict)
            logging.info(f"Appended the created dictonary record into {img_data}")
        except HTTPError as e:
            logging.error(f"HTTP Error {e.code}: {e.reason} while downloading '{url}'")
        except URLError as e:
            logging.error(f"URL Error: {e.reason} while downloading '{url}'")
        except ContentTooShortError as e:
            logging.error(f"ContentTooShortError: {e} while downloading '{url}'")
        except FileNotFoundError as e:
            logging.error(f"FileNotFoundError: {e} while downloading '{url}'")
        except Exception as e:  # Catch any other unexpected exceptions
            logging.error(f"An unexpected error occurred while downloading '{url}': {e}")
    return img_data

def get_downloads_folder():
    """
    Gets or creates (if not exists) the "downloads" folder within the project's root directory,
    with logging and exception handling.

    Returns:
        str: The absolute path to the "downloads" folder.
    """
    try:
        # Get the absolute path of the project's root directory
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        # Create the 'logs' directory if it doesn't exist
        downloads_folder = os.path.join(project_root, 'downloads')
        os.makedirs(downloads_folder, exist_ok=True)

        if not Path(downloads_folder).exists():
            os.makedirs(downloads_folder)
            logging.info(f"Created 'downloads' folder at {downloads_folder}")
        else:
            logging.info(f"Using existing 'downloads' folder at {downloads_folder}")

        return str(downloads_folder)

    except OSError as e:
        logging.error(f"Error getting or creating 'downloads' folder: {e}")
        # You can choose to raise an exception here or return None,
        # depending on how you want to handle the error.
        raise  # Example: Raise the exception to stop the script.

    except Exception as e:  # Catch any other unexpected exceptions
        logging.error(f"An unexpected error occurred: {e}")
        raise

def get_element_attribute(element, attribute_name):
    """
    Gets the value of a specified attribute from a WebElement.

    Args:
        element (WebElement): The WebElement object to extract the attribute from.
        attribute_name (str): The name of the attribute to retrieve (e.g., "href", "class", "src").

    Returns:
        str or None: The value of the attribute, or None if the attribute doesn't exist or an error occurs.
    """
    try:
        if not isinstance(element, WebElement):
            raise TypeError("The 'element' argument must be a WebElement object.")

        attribute_value = element.get_attribute(attribute_name)
        logging.info(f"Retrieved attribute '{attribute_name}' with value '{attribute_value}'")
        return attribute_value

    except StaleElementReferenceException:
        logging.warning(
            f"StaleElementReferenceException: Element is no longer attached to the DOM. Could not get attribute '{attribute_name}'")
        return None  # Return None to indicate the attribute could not be retrieved

    except Exception as e:
        logging.error(f"An unexpected error occurred while getting attribute '{attribute_name}': {e}")
        return None  # Return None to indicate the attribute could not be retrieved


def sleep(seconds):
    """
    Pauses the execution for a specified number of seconds.

    Args:
        seconds (int or float): The number of seconds to sleep.
    """
    time.sleep(seconds)


def quit_driver(driver):
    """
    Quits the WebDriver instance, closing all associated windows and logging the outcome.

    Args:
        driver (WebDriver): The WebDriver instance to quit.
    """
    try:
        driver.quit()
        logging.info("WebDriver quit successfully.")
    except WebDriverException as e:
        logging.error(f"Error occurred while quitting the WebDriver: {e}")

def scrape_google_images(query:str):
    URL = f"https://www.google.com/search?q={'+'.join(query.split(' '))}&sca_esv=cf0d20e87d8c130d&biw=1229&bih=120&udm=2&sxsrf=ADLYWIJ2qrdQMDUhuHy6lJKqcunQve6UNw%3A1716096304503&ei=MI1JZpihHvf44-EPjNOE8AU&ved=0ahUKEwiY-YT1_JiGAxV3_DgGHYwpAV4Q4dUDCBA&oq=Lionel+Messi&gs_lp=Egxnd3Mtd2l6LXNlcnAiDExpb25lbCBNZXNzaTINEAAYgAQYsQMYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBTIKEAAYgAQYQxiKBUj0DFAAWABwAXgAkAEAmAEAoAEAqgEAuAEMyAEAmAIBoAIGmAMAiAYBkgcBMaAHAA&sclient=gws-wiz-serp"
    driver=initiate_chromedriver(headless=True)
    open_page_url(driver,URL)
    img_data=download_file(driver=driver,query=query)
    quit_driver(driver=driver)
    return img_data
