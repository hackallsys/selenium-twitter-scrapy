import argparse
import sys
import os
import getpass


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
    parser.add_argument('-u', '--user', type=str,
                        default=os.getenv("TWITTER_USERNAME"), help='Your twitter username.')
    parser.add_argument('-p', '--password', type=str,
                        default=os.getenv("TWITTER_PASSWORD"), help='Your twitter password')

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

    if USER_UNAME is None:
        USER_UNAME = input("Twitter Username: ")

    if USER_PASSWORD is None:
        USER_PASSWORD = getpass.getpass("Enter Password: ")

    print()


if __name__ == "__main__":
    main()
