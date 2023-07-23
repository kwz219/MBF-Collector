import argparse
import os
import time

from Runner_CMD import setupLogger, process_json_file
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
    parser.add_argument("--jar_path",help="the location of jar")

    args = parser.parse_args()

    mode = args.mode

    if mode=="infer_fault_type":
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
        jsons_dir = args.download_save_dir
        au_token = args.au_token
        save_root_dir = args.month_dir

        files = os.listdir(jsons_dir)
        for file in files:
            if file.endswith(".gz"):
                file_path = os.path.join(jsons_dir, file)
                os.system("gunzip " + file_path)
                time.sleep(2)
                log_path = os.path.join(save_root_dir, file.replace(".json.gz", ".crawl.log"))
                if os.path.exists(log_path):
                    continue
                save_dir = os.path.join(save_root_dir, file.replace(".json.gz", ""))
                os.mkdir(save_dir)
                push_save_dir = os.path.join(save_dir, "PushEvent")
                pr_save_dir = os.path.join(save_dir, "PREvent")
                if not os.path.exists(push_save_dir):
                    os.mkdir(push_save_dir)
                if not os.path.exists(pr_save_dir):
                    os.mkdir(pr_save_dir)
                logger = setupLogger(log_path)
                process_json_file(file_path.replace(".gz", ""), logger, au_token, push_save_dir, pr_save_dir)
                if os.path.exists(file.replace(".gz", "")):
                    os.system("rm " + file.replace(".gz", ""))

    elif mode == "parse_contextual_pairs":
        month_dir = args.month_dir
        log_file = args.log_path
        parse_jar_file = args.jar_path
        traverse_folder_month_parse(month_dir,log_file,parse_jar_file)
    elif mode == "export_data":
        pass
    else:
        print("Not Valid Commands")
