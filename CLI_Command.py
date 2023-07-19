import argparse
import os

from Util.Utils import download_by_month,unzip_and_delete_all
from Util.traverse_folder import traverse_folder_month_infer,traverse_folder_month_parse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='cli_command')
    parser.add_argument("--mode")
    parser.add_argument("--log_path")
    parser.add_argument("--month",help="Which month's data do you want to download, e.g., 2020-01 ")
    parser.add_argument("--download_save_dir")
    parser.add_argument("--month_dir",help="the directory to store the data organizes by month")
    parser.add_argument("--save_dir")
    parser.add_argument("--au_token")

    ## args for constructing
    args = parser.parse_args()

    mode = args.mode

    if mode=="infer_type":
        print("Start to infer types -------")
        month_dir = args.month_dir
        log_path = args.log_path
        traverse_folder_month_infer(month_dir,log_path)
    elif mode == "download_events":
        download_month=args.month
        infos=download_month.split('-')
        year = infos[0]
        month = infos[1]
        download_save_dir = args.download_save_dir
        download_by_month(year,month,download_save_dir)
        unzip_and_delete_all(download_save_dir)

    elif mode == "mine_basic_information":
        month_dir = args.month_dir
        log_file = args.log_path
        traverse_folder_month_parse(month_dir,log_file)
        pass
    elif mode == "":
        pass
