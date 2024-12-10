import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

class BrowserHelpers:
    def __init__(self):
        # Set Chrome options
        logging.info("Initializing WebDriver with Chrome options.")
        chrome_options = Options()
        chrome_options.add_argument("--disable-usb")  # Suppress USB-related errors
        self.driver = webdriver.Chrome(options=chrome_options)
        logging.info("WebDriver initialized successfully.")
        
        # Maximize browser window to full screen
        logging.info("Maximizing browser window to full screen.")
        self.driver.maximize_window()
        logging.info("Browser window maximized successfully.")

    def open_browser(self, url):
        logging.info(f"Opening browser and navigating to URL: {url}")
        self.driver.get(url)
        logging.info(f"Browser opened and navigated to {url}.")

    def wait_for_page_load(self, locator_type, locator_value, timeout=10):
        """Wait for a specific element to be present on the page to ensure it is fully loaded."""
        logging.info(f"Waiting for page to load. Locator: {locator_type}='{locator_value}', Timeout: {timeout}s.")
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((locator_type, locator_value))
        )
        logging.info(f"Page loaded. Element located: {locator_type}='{locator_value}'.")

    def scroll_to_element(self, element):
        """Scroll the page to bring the element into view."""
        logging.info(f"Scrolling to element: {element.tag_name}")
        self.driver.execute_script("arguments[0].scrollIntoView({ behavior: 'smooth', block: 'center' });", element)
        logging.info("Scrolled to element successfully.")

    def wait_for_element(self, locator_type, locator_value, timeout=15):
        """Wait for an element to be clickable and visible, and scroll to it."""
        logging.info(f"Waiting for element to be clickable. Locator: {locator_type}='{locator_value}', Timeout: {timeout}s.")
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((locator_type, locator_value))
        )
        self.scroll_to_element(element)  # Ensure the element is in view
        logging.info(f"Element is clickable: {locator_type}='{locator_value}'.")
        return element

    def find_element(self, locator_type, locator_value):
        """Find an element on the page and scroll to it."""
        logging.info(f"Finding element. Locator: {locator_type}='{locator_value}'.")
        element = self.driver.find_element(locator_type, locator_value)
        self.scroll_to_element(element)  # Ensure the element is in view
        logging.info(f"Element found: {locator_type}='{locator_value}'.")
        return element

    def find_elements(self, locator_type, locator_value):
        """Find multiple elements on the page."""
        logging.info(f"Finding elements. Locator: {locator_type}='{locator_value}'.")
        elements = self.driver.find_elements(locator_type, locator_value)
        logging.info(f"Found {len(elements)} elements for locator: {locator_type}='{locator_value}'.")
        return elements

    def send_keys(self, locator_type, locator_value, text):
        """Send keys to an input field, ensuring it is in view."""
        logging.info(f"Sending keys to element. Locator: {locator_type}='{locator_value}', Text: '{text}'.")
        element = self.wait_for_element(locator_type, locator_value)
        element.clear()
        element.send_keys(text)
        logging.info(f"Keys sent to element: {locator_type}='{locator_value}'.")

    def click(self, locator_type, locator_value):
        """Click an element, ensuring it is in view."""
        logging.info(f"Clicking element. Locator: {locator_type}='{locator_value}'.")
        element = self.wait_for_element(locator_type, locator_value)
        element.click()
        logging.info(f"Element clicked: {locator_type}='{locator_value}'.")

    def quit_browser(self):
        """Close the browser."""
        logging.info("Closing the browser.")
        self.driver.quit()
        logging.info("Browser closed.")
