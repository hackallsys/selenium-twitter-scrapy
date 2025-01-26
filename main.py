import argparse
import sys
import os
import getpass
from twitter_scraper import TwitterScraper
import time


try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Twiter Friends List Lookup Tool')
    parser.add_argument('--user', type=str,
                        default=os.getenv("TWITTER_USERNAME"), help='Your twitter username.')
    parser.add_argument('--password', type=str,
                        default=os.getenv("TWITTER_PASSWORD"), help='Your twitter password')
    parser.add_argument('--account', type=str,
                        default=os.getenv("TWITTER_ACCOUNT"), help='Your twitter account')
    parser.add_argument('--search-user', type=str, help='User Name to be searched')

    args = parser.parse_args()
    return args


def main():
    args = parse_arguments()

    banner = R"""
=======================================================
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
+         ____________                                +
+        < Twitter Scrapy! >                          +
+         ------------                                +
+                \   ^__^                             +
+                 \  (oo)\_______                     +
+                    (__)\       )\/\                 +
+                        ||----w |                    +
+                        ||     ||                    +
+                                                     +
+        A simple tool to find twiter friend list.    +
+       [-------->   Write No Bugs 0_0   <--------]   +	
+              GitHub: hackallsys | justtodo          +
+          <================================>         +
+                                                     +
+++++++++++++++++++++++++++++++++++++++++++++++++++++++
=======================================================
    """
    print(banner)

    USER_UNAME = args.user
    USER_PASSWORD = args.password
    USER_ACCOUNT = args.account
    SEARCH_USER_NAME = args.search_user

    if USER_UNAME is None:
        USER_UNAME = input("Twitter Username: ")

    if USER_PASSWORD is None:
        USER_PASSWORD = getpass.getpass("Enter Password: ")

    if USER_ACCOUNT is None:
        USER_ACCOUNT = input("Enter Account: ")

    if SEARCH_USER_NAME is None:
        SEARCH_USER_NAME = input("Enter User name to be searched: ")

    print()

    if USER_UNAME is not None and USER_PASSWORD is not None:
        try:
            scraper = TwitterScraper(USER_UNAME, USER_PASSWORD, USER_ACCOUNT)

            print("Please closing vpn")
            time.sleep(10)
            verify_code = scraper.get_verify_code()
            print("Please opening vpn")
            time.sleep(10)
            scraper.login(verify_code)
            scraper.search(SEARCH_USER_NAME)
        except KeyboardInterrupt:
            print("\nScript Interrupted by user. Exiting...")
            sys.exit(1)
    
    sys.exit(1)


if __name__ == "__main__":
    main()
