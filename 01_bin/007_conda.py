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

    for env in config['conda_envs']: 
        name = env['name']
        requiments = env['requirements']
        if name != 'base':
            conda_env = f"conda create -n {name}"
            subprocess.run(conda_env, shell=True)
        pip_install = f"conda activate {name} && pip install  --upgrade -r {requiments}"
        # out_txt = subprocess.run(pip_install, shell=True)
        out_txt = subprocess.check_output(pip_install.split(), shell=True)
        for line in out_txt.decode("utf-8").split("\n"):
            print(line)
        new_requirements = f"{name}_requirements.txt"
        pip_freeze = f"conda activate {name} && pip freeze > {new_requirements}"
        out_txt = subprocess.run(pip_freeze, shell=True)
        print(f"Conda environment {name} has been created.")
        lines = []
        with open(new_requirements, "r") as f:
            for line in f.readlines():
                if "@ file://" in line:
                    continue
                lines.append(line.split("==")[0])

        with open(new_requirements, "w") as f:
            f.write("\n".join(lines))


def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    return parser.parse_args()


if __name__ == "__main__":    
    args = parse_args()
    main(args)
