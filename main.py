import argparse
import sys
import os
import getpass
from twitter_scraper import TwitterScraper
import time
import pandas as pd
import shutil
import zipfile


try:
    from dotenv import load_dotenv

    print("Loading .env file")
    load_dotenv()
    print("Loaded .env file\n")
except Exception as e:
    print(f"Error loading .env file: {e}")
    sys.exit(1)


def zip_package(search_account_name):
    current_dir = os.getcwd()
    # 定义follower 目录路径, 将follower相关信息文件移动到follower目录
    follower_dir = os.path.join(current_dir, 'follower')
    if not os.path.exists(follower_dir):
        os.makedirs(follower_dir)

    for filename in os.listdir(current_dir):
        # 检查文件是否以 .xlsx 结尾且不是 output.xlsx
        if filename.endswith('.xlsx') and filename != f'{search_account_name}.xlsx':
            # 构建文件的完整路径
            file_path = os.path.join(current_dir, filename)
            # 构建目标路径，即 follower 目录下的文件路径
            target_path = os.path.join(follower_dir, filename)
            try:
                # 移动文件
                shutil.move(file_path, target_path)
                print(f"已将 {filename} 移动到 {follower_dir}")
            except Exception as e:
                print(f"移动 {filename} 时出错: {e}")

    # 将获取的文件压缩为zip文件
    output_file = os.path.join(current_dir, f'{search_account_name}.xlsx')
    # 定义压缩文件的名称和路径
    zip_file_path = os.path.join(current_dir, f'{search_account_name}.zip')

    # 创建一个 ZipFile 对象，以写入模式打开
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # 检查 output.xlsx 文件是否存在，如果存在则添加到压缩文件中
        if os.path.exists(output_file):
            zipf.write(output_file, os.path.basename(output_file))
        # 检查 follower 目录是否存在，如果存在则遍历该目录下的所有文件和子目录并添加到压缩文件中
        if os.path.exists(follower_dir):
            for root, dirs, files in os.walk(follower_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    # 计算相对路径，以便在压缩文件中保持目录结构
                    arcname = os.path.relpath(file_path, current_dir)
                    zipf.write(file_path, arcname)

    print(f"已成功将 output.xlsx 文件和 follower 目录压缩为 {zip_file_path}")


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
            scraper.back()
            scraper.back()
            scraper.back()
            scraper.back()
            scraper.back()

            # 获取关注者的被关注用户和关注用户
            current_dir = os.getcwd()
            file_path = os.path.join(current_dir, f'{scraper.get_search_account_name()}.xlsx')

            if not os.path.exists(file_path):
                print("\nNo file exist.")
                scraper.quit()
            
            # 读取 Excel 文件
            excel_file = pd.ExcelFile(f'{scraper.get_search_account_name()}.xlsx')

            # 获取指定工作表中的数据
            try:
                df = excel_file.parse('follower')
                # 检查 `accountname` 列是否存在
                if 'accountname' in df.columns:
                    # 获取 `accountname` 列的数据
                    accountnames = df['accountname']
                    # 遍历并打印每一个值
                    for acoountname in accountnames:
                        print(f'\n Search user: {acoountname}.')
                        scraper.search(acoountname, False)
                        scraper.back()
                        scraper.back()
                        scraper.back()
                        scraper.back()
                        scraper.back()
                else:
                    print("在 'follower'工作表中没有找到 'accountname' 列。")
                    scraper.quit()
            except ValueError:
                print("Excel文件中不存在名为 'follower' 的工作表。")
                scraper.quit()
            
            scraper.quit()
            
            # to package
            zip_package(scraper.get_search_account_name())

        except KeyboardInterrupt:
            print("\nScript Interrupted by user. Exiting...")
            sys.exit(1)
    
    sys.exit(1)


if __name__ == "__main__":
    main()
