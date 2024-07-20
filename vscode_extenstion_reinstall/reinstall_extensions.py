import os
import sys
import shutil
import subprocess
import time

extension_fn = "list_of_extenstions.txt"
team_clients = ["code"] # ["code-insiders", "code"]
cmd_list = f"code-insiders  --list-extensions"


def get_list_of_extensions():
    if os.path.exists(extension_fn):
        now = f"{time.time()}"
        shutil.move(extension_fn, f"{extension_fn}_{now}" + "bak.txt")

    if not os.path.exists(extension_fn):
        print("creating_file", extension_fn)
        lines = set()
        for client in team_clients:
            cmd_list_ext = f"{client} --list-extensions"
            out_txt = subprocess.check_output(cmd_list_ext.split(), shell=True)
            for line in out_txt.decode("utf-8").split("\n"):
                if line == "":
                    continue
                lines.add(line)

        with open(extension_fn, "w") as f:
            for line in lines:
                f.write(f"{line}\n")


def uninstall_extensions():
    with open(extension_fn, "r") as f:
        for line in f.readlines():

            for client in team_clients:
                cmd_uninstall = f"{client} --uninstall-extension"
                cmd_uninstall_one = f"{cmd_uninstall} {line}"
                try:

                    out_txt = subprocess.check_output(cmd_uninstall_one.split(), shell=True)
                    print("command", cmd_uninstall_one)
                    print("output", out_txt.decode("utf-8"))
                except Exception as e:
                    print('error: ', e)

def install_extensions():
    with open(extension_fn, "r") as f:
        for line in f.readlines():

            for client in team_clients:
                cmd_install = f"{client} --install-extension"
                cmd_install_one = f"{cmd_install} {line}"
                out_txt = subprocess.check_output(cmd_install_one.split(), shell=True)
                print("command", cmd_install_one)
                print("output", out_txt.decode("utf-8"))


if __name__ == "__main__":
    uninstall_extensions()
    install_extensions()
