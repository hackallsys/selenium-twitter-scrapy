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
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from webdriver_manager.chrome import ChromeDriverManager

TWITTER_LOGIN_URL = "https://x.com/i/flow/login"
WAITTING_TIME_SECOND = 10


class TwitterScraper:
    def __init__(self, username, password, account):
        print("Initializing Twitter Scraper...")

        self.username = username
        self.password = password
        self.account = account

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

        try:
            self.driver.maximize_window()
            self.driver.get(TWITTER_LOGIN_URL)
            time.sleep(3)

            self._input_username()
            self._input_unusual_activity()
            self._input_password()

        except Exception as e:
            print()
            print(f"Login Failed: {e}")
            sys.exit(1)

    def _input_username(self):
        """
        input username
        """
        input_attempt = 0

        while True:
            try:
                username = self.driver.find_element(By.XPATH, "//input[@autocomplete='username']")
                username.send_keys(self.username)
                time.sleep(WAITTING_TIME_SECOND)
                username.send_keys(Keys.RETURN)
                time.sleep(WAITTING_TIME_SECOND // 2)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    print(
                        """There was an error inputting the username.

It may be due to the following:
- Internet connection is unstable
- Username is incorrect
- Twitter is experiencing unusual activity"""
                    )
                    self.driver.quit()
                    sys.exit(1)
                else:
                    print("Re-attempting to input username...")
                    time.sleep(2)

    def _input_password(self):
        input_attempt = 0

        while True:
            try:
                password = self.driver.find_element(By.XPATH, "//input[@autocomplete='current-password']")

                password.send_keys(self.password)
                time.sleep(WAITTING_TIME_SECOND)
                password.send_keys(Keys.RETURN)
                time.sleep(WAITTING_TIME_SECOND // 2)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    print()
                    print(
                        """There was an error inputting the password.

It may be due to the following:
- Internet connection is unstable
- Password is incorrect
- Twitter is experiencing unusual activity"""
                    )
                    self.driver.quit()
                    sys.exit(1)
                else:
                    print("Re-attempting to input password...")
                    time.sleep(2)
    
    def _input_unusual_activity(self):
        input_attempt = 0

        while True:
            try:
                unusual_activity = self.driver.find_element(By.XPATH, "//input[@data-testid='ocfEnterTextTextInput']")
                unusual_activity.send_keys(self.account)
                time.sleep(WAITTING_TIME_SECOND)
                unusual_activity.send_keys(Keys.RETURN)
                time.sleep(WAITTING_TIME_SECOND // 2)
                break
            except NoSuchElementException:
                input_attempt += 1
                if input_attempt >= 3:
                    break

    def go_to_home(self):
        """
        return to twitter home page
        """
        self.driver.get("https://x.com/home")
        time.sleep(3)
        pass
