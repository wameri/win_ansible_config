import os
import sys
import shutil
import subprocess
import time
import random

import yaml
import datetime

from argparse import ArgumentParser as AP


def run_cmd(cmd, shell=True, cur_dir="."):
    try:
        out_txt = subprocess.check_output(cmd, shell=True, cwd=cur_dir)
        for line in out_txt.decode("utf-8").split("\n"):
            print(line)
    except subprocess.CalledProcessError as e:
        print(e)


def main(args):
    if args.git_pull:
        cur_dir = os.path.abspath(".")
        git_pull_cmd = ["git pull"]
        run_cmd(git_pull_cmd, cur_dir=cur_dir)

    if args.git_push:
        cur_dir = os.path.abspath(".")
        git_add_cmd = "git add ."
        run_cmd(git_add_cmd)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        git_commit_cmd = f"git commit -m 'auto {time}'"
        run_cmd(git_commit_cmd)

        git_push_cmd = "git push"
        run_cmd(git_push_cmd)


def parse_args():
    parser = AP()
    parser.add_argument("--git_pull", type=bool, default=True)
    parser.add_argument("--git_push", type=bool, default=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
