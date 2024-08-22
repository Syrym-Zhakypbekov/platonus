import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class WebDriverManager:
    def __init__(self, options=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver = self._initialize_driver(options)

    def _initialize_driver(self, options):
        try:
            chrome_options = options or self._default_options()
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
            self.logger.info("WebDriver initialized successfully.")
            return driver
        except Exception as e:
            self.logger.error("Error initializing WebDriver: %s", e)
            raise

    def _default_options(self):
        chrome_options = Options()
        user_data_dir = "C:\\chrome_data"
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        chrome_options.add_argument("--remote-debugging-port=9222")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        self.logger.info("Default Chrome options set with user data directory and port.")
        return chrome_options

    def open_url(self, url):
        try:
            if not isinstance(url, str) or not url.startswith('http'):
                raise ValueError("Invalid URL provided")
            self.driver.get(url)
            self.logger.info("Opened URL: %s", url)
        except Exception as e:
            self.logger.error("Error opening URL: %s", e)
            raise

    def quit_driver(self):
        try:
            self.driver.quit()
            self.logger.info("WebDriver quit successfully.")
        except Exception as e:
            self.logger.error("Error quitting WebDriver: %s", e)
            raise

    def execute_script(self, script, *args):
        try:
            result = self.driver.execute_script(script, *args)
            self.logger.info("Executed script: %s", script)
            return result
        except Exception as e:
            self.logger.error("Error executing script: %s", e)
            raise

class BrowserAutomation:
    def __init__(self, driver_manager):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver_manager = driver_manager

    def login_platonus(self, login, password):
        try:
            url = "https://platonus.iitu.edu.kz/"
            self.driver_manager.open_url(url)

            WebDriverWait(self.driver_manager.driver, 10).until(
                EC.presence_of_element_located((By.ID, "login_input"))
            ).send_keys(login)
            self.logger.info("Entered login.")

            WebDriverWait(self.driver_manager.driver, 10).until(
                EC.presence_of_element_located((By.ID, "pass_input"))
            ).send_keys(password)
            self.logger.info("Entered password.")

            WebDriverWait(self.driver_manager.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "Submit1"))
            ).click()
            self.logger.info("Clicked login button.")

            WebDriverWait(self.driver_manager.driver, 10).until(
                EC.url_contains("/dashboard")
            )
            self.logger.info("Login successful, navigated to dashboard.")
        except Exception as e:
            self.logger.error("Error logging in to Platonus: %s", e)
            raise

def main():
    logger = logging.getLogger("Main")
    logger.info("Starting browser automation...")

    chrome_options = Options()
    driver_manager = WebDriverManager(options=chrome_options)
    browser_automation = BrowserAutomation(driver_manager)

    try:
        browser_automation.login_platonus('s.zhakypbekov@iitu.edu.kz', 'Temp2022$')
    except Exception as e:
        logger.error("An error occurred during browser automation: %s", e)
    finally:
        driver_manager.quit_driver()
        logger.info("Browser automation completed.")

if __name__ == "__main__":
    main()
