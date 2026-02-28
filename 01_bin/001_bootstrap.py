import subprocess
try:
    import yaml
except Exception as e:
    subprocess.check_output("winget install Anaconda.Miniconda3")
    subprocess.check_output("python -m pip install pyyaml")
    import yaml

from argparse import ArgumentParser as AP

def run_command(cmd_txt, split=True, shell=True):
    cmd = cmd_txt
    if split:
        cmd = cmd.split()

    print(f'Running command:', cmd)
    try:
        out_txt = subprocess.check_output(cmd, shell=True)
        for line in out_txt.decode("utf-8").split("\n"):
            print(line)
    except Exception as e:
        print('Error', e)


def main(args):

    config = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)
    # Windows feature

    ## turn on Windows subsystem for linux
    ## enable win for developer: https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development

    cmd_update_wsl = "wsl --update"
    run_command(cmd_update_wsl)
    cmd_install_wsl = "wsl --install -n "
    run_command(cmd_install_wsl)

    # Install with winget

    cmd_update_winget = "winget update --all"
    run_command(cmd_update_winget)

    config = yaml.load(open(args.config, 'r'), Loader=yaml.FullLoader)

    for pkg in config["winget_packages"]:
        name = pkg['name']
        state = pkg['state']
        if state != "install":
            continue
        cmd_winget_pkg = f'winget install {name}'
        run_command(cmd_winget_pkg)

    # example 'scoop bucket add nerd-fonts'
    for scoop_bucket in config["scoop_buckets"]:
        name = scoop_bucket["name"]
        state = scoop_bucket["state"]
        if state != "install":
            continue
        cmd_scoop_bucket = f"scoop bucket add {name}"
        run_command(cmd_scoop_bucket)

    for scoop_pkg in config["scoop_packages"]:
        name = scoop_pkg["name"]
        state = scoop_pkg["state"]
        if state != "install":
            continue
        cmd_scoop_pkg = f"scoop install {name}"
        run_command(cmd_scoop_pkg)


def parse_args():
    parser = AP()
    parser.add_argument("--config", type=str, default="000_configs.yaml")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
