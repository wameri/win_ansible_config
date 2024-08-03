import os
import sys
import shutil
import subprocess
import time
import random

import yaml

from argparse import ArgumentParser as AP

def main(args):

    config = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)
    dotfiles_dir = config["dotfiles_configs"]["dotfiles_dir"]
    for dotfile in config["dotfiles_links"]:
        source = os.path.join(dotfiles_dir, dotfile["source"])
        if not os.path.exists(source):
            print(f"source {source} does not exist")
            continue
        target = dotfile["target"] if  not dotfile["target"].startswith("~") else os.path.expanduser(dotfile["target"])
        if os.path.exists(target):
            print(f"target {target} already exists")
            backup_dir = os.path.join(dotfiles_dir, "backup")
            os.makedirs(backup_dir, exist_ok=True)
            backup_fn = os.path.join(backup_dir, os.path.basename(target + str(random.randint(0, 10000000))))
            shutil.move(target, backup_fn) 

        # symlink
        os.symlink(source, target)    


def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    return parser.parse_args()


if __name__ == "__main__":    
    args = parse_args()
    main(args)
