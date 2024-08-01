import os
import sys
import shutil
import subprocess
import time

import yaml

from argparse import ArgumentParser as AP

team_clients = ["code"] # ["code-insiders", "code"]

def main(config):
    for client in team_clients:
        for extension in config["vscode_extenstions"]:
            print(extension)
            cmd_uninstall = f"{client} --uninstall-extension"
            cmd_uninstall_one = f"{cmd_uninstall} {extension}"
            try:
                out_txt = subprocess.check_output(cmd_uninstall_one.split(), shell=True)
                print("command", cmd_uninstall_one)
                print("output", out_txt.decode("utf-8"))
            except Exception as e:
                print('error: ', e)
            cmd_install = f"{client} --install-extension"
            cmd_install_one = f"{cmd_install} {extension}"
            try:
                out_txt = subprocess.check_output(cmd_install_one.split(), shell=True)
                print("command", cmd_install_one)
                print("output", out_txt.decode("utf-8"))
            except Exception as e:
                print('error: ', e)
        
        cmd_list_ext = f"{client} --list-extensions"
        out_txt = subprocess.check_output(cmd_list_ext.split(), shell=True)
        lines = []
        for line in out_txt.decode("utf-8").split("\n"):
            if line == "":
                continue
            lines.append(line)
        print(lines)


 

def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    return parser.parse_args()


if __name__ == "__main__":    
    args = parse_args()
    config = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)
    main(config)

