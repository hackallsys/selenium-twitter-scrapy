import sys
import os
import time
from fake_headers import Headers

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    WebDriverException,
)

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService

from webdriver_manager.chrome import ChromeDriverManager

TWITTER_LOGIN_URL = "https://www.biying.com"


class TwitterScraper:
    def __init__(self, username, password):
        print("Initializing Twitter Scraper...")

        self.username = username
        self.password = password

        self.driver = self._get_driver()

    def _get_driver(self):
        print("Setup WebDriver...")
        header = Headers().generate()["User-Agent"]

        # browser_option = EdgeOptions()
        browser_option = ChromeOptions()

        browser_option.add_argument("--no-sandbox")
        browser_option.add_argument("--disable-dev-shm-usage")
        browser_option.add_argument("--ignore-certificate-errors")
        browser_option.add_argument("--disable-gpu")
        browser_option.add_argument("--log-level=3")
        browser_option.add_argument("--disable-notifications")
        browser_option.add_argument("--disable-popup-blocking")
        browser_option.add_argument("--user-agent={}".format(header))

        try:
            print("Initializing ChromeDriver...")
            driver = webdriver.Chrome(
                options=browser_option,
            )

            print("WebDriver Setup Complete")
            return driver
        except WebDriverException:
            try:
                print("Downloading ChromeDriver...")
                chromedriver_path = ChromeDriverManager().install()
                chrome_service = ChromeService(
                    executable_path=chromedriver_path)

                print("Initializing ChromeDriver...")
                driver = webdriver.Chrome(
                    service=chrome_service,
                    options=browser_option,
                )

                print("WebDriver Setup Complete")
                return driver
            except Exception as e:
                print(f"Error setting up WebDriver: {e}")
                sys.exit(1)

    def login(self):
        """
        login twitter
        """
        print()
        print("Logging in to Twitter...")

        self.driver.get(TWITTER_LOGIN_URL)
        time.sleep(3)

    def go_to_home(self):
        """
        return to twitter home page
        """
        self.driver.get("https://x.com/home")
        time.sleep(3)
        pass
