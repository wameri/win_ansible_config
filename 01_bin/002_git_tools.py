import os
import sys
import shutil
import subprocess
import time
import random

# import yaml
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
    other_git_repos = {
        "20.02_win_dotfiles":"https://github.com/wameri/win_dotfiles.git",
        "20.04_mac_dotfiles":"https://github.com/wameri/mac_dotfiles.git",
        "20.05_mac_ansible_config":"https://github.com/wameri/mac_ansible_config.git",
        "20.01_my_wiki":"https://github.com/wameri/wiki.git",
    }
    for git_repo_name , git_repo_url in other_git_repos.items():
        repo_dir = os.path.join(parrent_dir, git_repo_name)
        if os.path.exists(repo_dir):
            continue
        cmd_clone = f'git clone {git_repo_url} {git_repo_name}'
        run_cmd(cmd_clone, cur_dir=parrent_dir)
        

    for dirname in os.listdir(parrent_dir):
        work_dir = os.path.join(parrent_dir, dirname)
        if os.path.isdir(work_dir):

            if ".git" not in os.listdir(work_dir):
                break
            print("git dir: ", dirname)
            process_dir(work_dir)


def process_dir(cur_dir):

    git_config_email = "git config --local user.email 'work.ameri@gmail.com'"
    run_cmd(git_config_email, cur_dir=cur_dir)
    git_config_name = "git config --local user.name 'Ezra Ameri'"
    run_cmd(git_config_name, cur_dir=cur_dir)

    if args.git_commit:
        git_add_cmd = "git add ."
        run_cmd(git_add_cmd, cur_dir=cur_dir)

        time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        git_commit_cmd = f'git commit -m "auto_{time}"'
        run_cmd(git_commit_cmd, cur_dir=cur_dir)

    if args.git_pull:
        git_pull_cmd = "git pull --rebase"
        run_cmd(git_pull_cmd, cur_dir=cur_dir)

    if args.git_push:
        git_add_cmd = "git add ."
        run_cmd(git_add_cmd, cur_dir=cur_dir)

        time = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
        git_commit_cmd = f'git commit -m "auto_{time}"'
        run_cmd(git_commit_cmd, cur_dir=cur_dir)

        git_push_cmd = "git push"
        run_cmd(git_push_cmd, cur_dir=cur_dir)


def parse_args():
    parser = AP()
    parser.add_argument("--git_commit", type=bool, default=False)
    parser.add_argument("--git_pull", type=bool, default=True)
    parser.add_argument("--git_push", type=bool, default=True)
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
