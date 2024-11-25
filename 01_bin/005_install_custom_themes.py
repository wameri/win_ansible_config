import os
import sys
import shutil
import subprocess
import time
import random

import yaml

from argparse import ArgumentParser as AP


def main():
    if sys.platform == "darwin":
        extension_dir = os.path.expanduser("~/.vscode/extensions")
    elif sys.platform == "win32" and os.path.exists("C:\\.tools\\.vscode\\extensions"):
        extension_dir = os.path.expanduser("C:\\.tools\\.vscode\extensions")
    elif sys.platform == "win32" and os.path.expanduser("~\\.vscode\\extensions"):
        extension_dir = os.path.expanduser("~\\.vscode\\extensions")
    source_dir = os.path.abspath("04_vscode_theme")
    for dn in os.listdir(source_dir):
        theme_dir = os.path.join(source_dir, dn)
        if os.path.isdir(theme_dir):
            theme_name = dn
            target_dir = os.path.join(extension_dir, theme_name)
            if os.path.exists(target_dir) and not os.path.islink(target_dir):
                shutil.rmtree(target_dir)
            elif os.path.exists(target_dir):
                os.remove(target_dir)
            os.symlink(theme_dir, target_dir)
            print(f"Installed theme: {theme_name}")


if __name__ == "__main__":
    main()
