import os
import sys
import shutil
import subprocess
import time
import random

import yaml
import datetime

from argparse import ArgumentParser as AP


def run_cmd(cmd, shell=True, cur_dir=None):
    try:
        print("Running command: ", cmd)
        cur_dir = os.path.abspath(cur_dir if cur_dir else ".")
        print("Current dir: ", cur_dir)
        if sys.platform == "darwin":
            out_txt = subprocess.check_output(cmd.split(), cwd=cur_dir if cur_dir else ".")
        else:
            out_txt = subprocess.check_output(cmd.split(), shell=shell, cwd=cur_dir if cur_dir else ".")

        for line in out_txt.decode("utf-8").split("\n"):
            print(line)
    except subprocess.CalledProcessError as e:
        print(e)


def main(args):

    parrent_dir = os.path.abspath("..")
    for dirname in os.listdir(parrent_dir):
        work_dir = os.path.join(parrent_dir, dirname)
        if os.path.isdir(work_dir):

            if ".git" not in os.listdir(work_dir):
                break
            print("git dir: ", dirname)
            process_dir(work_dir)


def process_dir(cur_dir):

    if args.git_commit:
        git_add_cmd = "git add ."
        run_cmd(git_add_cmd, cur_dir=cur_dir)

        time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        git_commit_cmd = f'git commit -m "auto_{time}"'
        run_cmd(git_commit_cmd, cur_dir=cur_dir)

    if args.git_pull:
        git_pull_cmd = "git pull"
        run_cmd(git_pull_cmd, cur_dir=cur_dir)

    if args.git_push:
        git_add_cmd = "git add ."
        run_cmd(git_add_cmd, cur_dir=cur_dir)

        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        git_commit_cmd = f'git commit -m "auto {time}"'
        run_cmd(git_commit_cmd, cur_dir=cur_dir)

        git_push_cmd = "git push"
        run_cmd(git_push_cmd, cur_dir=cur_dir)


def parse_args():
    parser = AP()
    parser.add_argument("--git_commit", type=bool, default=True)
    parser.add_argument("--git_pull", type=bool, default=True)
    parser.add_argument("--git_push", type=bool, default=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
