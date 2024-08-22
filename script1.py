import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class WebDriverManager:
    """
    A class to manage WebDriver operations, ensuring clean and modular code structure.
    """

    def __init__(self, options=None):
        """
        Initializes the WebDriver with optional Chrome options.

        Args:
            options (Options, optional): Chrome options to customize WebDriver. Defaults to None.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver = self._initialize_driver(options)

    def _initialize_driver(self, options):
        """
        Private method to initialize the WebDriver.

        Args:
            options (Options): Chrome options to customize WebDriver.

        Returns:
            WebDriver: An instance of the WebDriver.
        """
        try:
            chrome_options = options or self._default_options()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("WebDriver initialized successfully.")
            return driver
        except Exception as e:
            self.logger.error("Error initializing WebDriver: %s", e)
            raise

    def _default_options(self):
        """
        Sets default Chrome options.

        Returns:
            Options: Default Chrome options.
        """
        chrome_options = Options()
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.logger.info("Default Chrome options set.")
        return chrome_options

    def open_url(self, url):
        """
        Opens a specified URL in the browser.

        Args:
            url (str): The URL to open.
        """
        try:
            if not isinstance(url, str) or not url.startswith('http'):
                raise ValueError("Invalid URL provided")
            self.driver.get(url)
            self.logger.info("Opened URL: %s", url)
        except Exception as e:
            self.logger.error("Error opening URL: %s", e)
            raise

    def wait(self, seconds):
        """
        Implicitly waits for the specified number of seconds.

        Args:
            seconds (int): Number of seconds to wait.
        """
        try:
            if not isinstance(seconds, (int, float)) or seconds < 0:
                raise ValueError("Wait time must be a non-negative number")
            self.driver.implicitly_wait(seconds)
            self.logger.info("Implicit wait for %s seconds.", seconds)
        except Exception as e:
            self.logger.error("Error during wait: %s", e)
            raise

    def quit_driver(self):
        """
        Quits the WebDriver, closing all associated windows.
        """
        try:
            self.driver.quit()
            self.logger.info("WebDriver quit successfully.")
        except Exception as e:
            self.logger.error("Error quitting WebDriver: %s", e)
            raise

    def execute_script(self, script, *args):
        """
        Executes a JavaScript script in the context of the current page.

        Args:
            script (str): The script to execute.
            *args: Arguments to pass to the script.

        Returns:
            The script's return value.
        """
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.info("Executed script: %s", script)
            return result
        except Exception as e:
            self.logger.error("Error executing script: %s", e)
            raise

class BrowserAutomation:
    """
    A class to encapsulate browser automation tasks, enhancing reusability and maintainability.
    """

    def __init__(self, driver_manager):
        """
        Initializes the BrowserAutomation with a WebDriverManager instance.

        Args:
            driver_manager (WebDriverManager): An instance of WebDriverManager to manage browser actions.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver_manager = driver_manager

    def perform_google_search(self, query):
        """
        Performs a Google search with the given query.

        Args:
            query (str): The search query to be entered into Google's search bar.
        """
        try:
            search_url = f"https://www.google.com/search?q={query}"
            self.driver_manager.open_url(search_url)
            self.logger.info("Performed Google search for query: %s", query)
        except Exception as e:
            self.logger.error("Error performing Google search: %s", e)
            raise

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the current page.
        """
        try:
            self.driver_manager.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            self.logger.info("Scrolled to bottom of the page.")
        except Exception as e:
            self.logger.error("Error scrolling to bottom: %s", e)
            raise

def main():
    """
    The main function to execute the browser automation tasks.
    """
    logger = logging.getLogger("Main")
    logger.info("Starting browser automation...")

    chrome_options = Options()
    driver_manager = WebDriverManager(options=chrome_options)
    browser_automation = BrowserAutomation(driver_manager)

    try:
        browser_automation.perform_google_search('OpenAI')
        driver_manager.wait(5)
        browser_automation.scroll_to_bottom()
    except Exception as e:
        logger.error("An error occurred during browser automation: %s", e)
    finally:
        driver_manager.quit_driver()
        logger.info("Browser automation completed.")

if __name__ == "__main__":
    main()
