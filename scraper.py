import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(
        description='Twiter Friends List Lookup Tool')
    parser.add_argument('-u', '--user', type=str, help='username')
    parser.add_argument('-p', '--passwd', type=str, help='password')

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


if __name__ == "__main__":
    main()
