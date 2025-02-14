import os
import sys
import shutil
import subprocess
import time

import yaml

from argparse import ArgumentParser as AP

team_clients = ["code"]


def main(args):

    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    if args.update_list == "True":

        existing_extensions = set([i.lower() for i in config["vscode_extensions"]])

        new_ones = set()
        for client in team_clients:
            cmd_list_ext = f"{client} --list-extensions"
            if sys.platform == "darwin":
                out_txt = subprocess.check_output(cmd_list_ext.split())
            else:
                out_txt = subprocess.check_output(cmd_list_ext.split(), shell=True)

            for line in out_txt.decode("utf-8").split("\n"):
                if line == "":
                    continue
                if "ezra ameri" in line.lower():
                    continue

                new_ones.add(line.lower())
        updated_extensions = sorted(list(existing_extensions.union(new_ones)))
        config["vscode_extensions"] = updated_extensions
        with open(args.config, "w") as f:
            yaml.dump(config, f)

    if args.install == "True":
        for client in team_clients:
            for extension in config["vscode_extensions"]:
                print(extension)
                if args.clean_install == "True":
                    cmd_uninstall = f"{client} --uninstall-extension"
                    cmd_uninstall_one = f"{cmd_uninstall} {extension}"
                    try:
                        out_txt = subprocess.check_output(cmd_uninstall_one.split(), shell=True)
                        print("command", cmd_uninstall_one)
                        print("output", out_txt.decode("utf-8"))
                    except Exception as e:
                        print("error: ", e)

                cmd_install = f"{client} --install-extension"
                cmd_install_one = f"{cmd_install} {extension}"
                try:
                    out_txt = subprocess.check_output(cmd_install_one.split(), shell=True)
                    print("command", cmd_install_one)
                    print("output", out_txt.decode("utf-8"))
                except Exception as e:
                    print("error: ", e)


def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    parser.add_argument("--install", type=str, default="True")
    parser.add_argument("--clean_install", type=str, default="False")
    parser.add_argument("--update_list", type=str, default="True")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    main(args)
    # run from command prompt in windows dev.
