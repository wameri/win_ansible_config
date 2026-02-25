"""
Git configuration management script for Windows.

This script implements the same logic as the macOS Ansible git_config role
(20.05_mac_ansible_config/roles/12_git_config/tasks/main.yml).

Main features:
1. Initialize git repositories for git config tracking
   - Creates temp directories for each config file
   - Initializes git repos in those directories
   - Creates empty config files if they don't exist
   - Symlinks the actual config file to .git/config in the temp repo

2. Set git config values
   - Reads git_global_config and git_user_global_config from YAML
   - Sets or removes config values using git config commands
   - Supports both 'present' and 'absent' states

3. Add includeIf sections to ~/.gitconfig
   - Reads git_include_if_configs from YAML
   - Adds includeIf blocks to allow conditional config inclusion
   - Manages blocks with markers similar to Ansible's blockinfile

4. Clean up temporary directories
   - Removes temp directories created during initialization

5. Optional bulk git operations (disabled by default)
   - Clone git repositories
   - Configure user.email and user.name
   - Commit, pull, and push changes

Usage:
    python 002_git_tools.py --config 000_configs.yaml
    python 002_git_tools.py --config 000_configs.yaml --enable_bulk_operations --git_pull

Configuration files:
    - 000_configs.yaml: Main configuration
    - 001_local_configs.yaml: Local overrides (optional)

Required YAML keys:
    - git_global_config_paths: List of config file paths to track
    - git_user_global_config_paths: User-specific config paths (optional)
    - git_global_config: List of config items to set
    - git_user_global_config: User-specific config items (optional)
    - git_include_if_configs: List of includeIf sections (optional)

Note: On Windows, symlink creation may require:
    - Administrator privileges, OR
    - Windows Developer Mode enabled (Windows 10+)
"""

import os
import re
import sys
import shutil
import shlex
import subprocess
import time
import random

import yaml
import datetime

from argparse import ArgumentParser as AP


def run_cmd(cmd, shell=True, cur_dir=None, check_error=True):
    try:
        print("Running command: ", cmd)
        cur_dir = os.path.abspath(cur_dir if cur_dir else ".")
        print("Current dir: ", cur_dir)
        if sys.platform == "darwin":
            out_txt = subprocess.check_output(shlex.split(cmd), cwd=cur_dir if cur_dir else ".")
        else:
            out_txt = subprocess.check_output(cmd, shell=shell, cwd=cur_dir if cur_dir else ".")

        for line in out_txt.decode("utf-8").split("\n"):
            print(line)
        return True
    except subprocess.CalledProcessError as e:
        if check_error:
            print(f"Error: {e}")
        return False


def git_init_configs(config=None, local_config=None):
    """
    Initialize git repositories for config tracking.
    Similar to Ansible tasks: ensure directory exists, git init, touch config, remove .git/config, symlink
    """
    parent_dir = os.path.abspath(".")

    # Collect all config paths from both global and user configs
    paths = []
    if "git_global_config_paths" in config:
        paths += config["git_global_config_paths"]
    if "git_global_config_paths" in local_config:
        paths += local_config["git_global_config_paths"]
    if "git_user_global_config_paths" in config:
        paths += config["git_user_global_config_paths"]
    if "git_user_global_config_paths" in local_config:
        paths += local_config["git_user_global_config_paths"]

    print(f"git init configs paths: {paths}")

    paths = list(set(paths))  # Remove duplicates
    for config_path in paths:
        # Expand home directory
        config_path_expanded = os.path.expanduser(config_path)

        # Create directory for the config file in current directory (temp location)
        # Use full path (e.g., "~/.my_gitconfig") so all temp dirs nest under "./~/"
        # This matches the Ansible role pattern: "./{{item}}" and allows
        # cleanup of "./~" to remove everything
        temp_dir = os.path.join(parent_dir, config_path)

        # Create directory if it doesn't exist
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir, exist_ok=True)
            print(f"Created directory: {temp_dir}")

        # Initialize git repository
        run_cmd("git init", cur_dir=temp_dir)

        # Touch/create the config file if it doesn't exist
        if not os.path.exists(config_path_expanded):
            # Create parent directories if they don't exist
            os.makedirs(os.path.dirname(config_path_expanded), exist_ok=True)
            # Create empty file
            open(config_path_expanded, "a").close()
            print(f"Created config file: {config_path_expanded}")

        # Remove the default .git/config
        git_config_path = os.path.join(temp_dir, ".git", "config")
        if os.path.exists(git_config_path):
            os.remove(git_config_path)
            print(f"Removed: {git_config_path}")

        # Create symlink from config file to .git/config
        # On Windows, we need to use mklink which requires admin or developer mode
        link_target = os.path.join(temp_dir, ".git", "config")
        if sys.platform == "win32":
            # Use Windows mklink command
            # Note: This may require admin privileges or Windows Developer Mode enabled
            cmd_link = f'mklink "{link_target}" "{config_path_expanded}"'
            subprocess.call(cmd_link, shell=True)
        else:
            os.symlink(config_path_expanded, link_target)
        print(f"Created symlink: {link_target} -> {config_path_expanded}")

    print("git init configs completed")


def git_config_set(config=None, local_config=None):
    """
    Set Git config values in specific config files.
    Similar to Ansible's git_config module.
    """
    parent_dir = os.path.abspath(".")

    # Collect all config items
    config_items = []
    if "git_global_config" in config:
        config_items += config["git_global_config"]
    if "git_global_config" in local_config:
        config_items += local_config["git_global_config"]
    if "git_user_global_config" in config:
        config_items += config["git_user_global_config"]
    if "git_user_global_config" in local_config:
        config_items += local_config["git_user_global_config"]

    print(f"Setting {len(config_items)} git config items")

    for item in config_items:
        name = item.get("name")
        value = item.get("value", "")
        state = item.get("state", "present")
        raw_path = item.get("path", "~/.gitconfig")
        path = os.path.expanduser(raw_path)

        # Get the temp directory for this config file (must match git_init_configs path)
        # Use raw_path (e.g., "~/.gitconfig") not the expanded absolute path,
        # so os.path.join produces "<parent_dir>/~/.gitconfig" (the temp dir)
        temp_dir = os.path.join(parent_dir, raw_path)

        if state == "present":
            # Set the config value
            cmd = f'git config --local {name} "{value}"'
            print(f"Setting {name}={value} in {path}")
            run_cmd(cmd, cur_dir=temp_dir, check_error=False)
        elif state == "absent":
            # Remove the config value
            cmd = f"git config --local --unset {name}"
            print(f"Removing {name} from {path}")
            run_cmd(cmd, cur_dir=temp_dir, check_error=False)

    print("git config set completed")


def git_clean_temp_dirs():
    """
    Clean up temporary git directories created during config initialization.
    Similar to Ansible's cleanup task for the temp directory.
    """
    parent_dir = os.path.abspath(".")
    temp_tilde = os.path.join(parent_dir, "~")

    if os.path.exists(temp_tilde):
        shutil.rmtree(temp_tilde)
        print(f"Cleaned up temp directory: {temp_tilde}")


def git_add_includeif(config=None, local_config=None):
    """
    Add includeIf sections to ~/.gitconfig.
    Similar to Ansible's blockinfile task.
    """
    include_if_configs = []
    if "git_include_if_configs" in config:
        include_if_configs += config["git_include_if_configs"]
    if "git_include_if_configs" in local_config:
        include_if_configs += local_config["git_include_if_configs"]

    if not include_if_configs:
        print("No includeIf configs to add")
        return

    gitconfig_path = os.path.expanduser("~/.gitconfig")

    # Read existing gitconfig
    if os.path.exists(gitconfig_path):
        with open(gitconfig_path, "r") as f:
            content = f.read()
    else:
        content = ""

    # Build the includeIf block
    marker_start = "# BEGIN ANSIBLE MANAGED BLOCK"
    marker_end = "# END ANSIBLE MANAGED BLOCK"

    # Remove existing managed block if present
    if marker_start in content:
        start_idx = content.find(marker_start)
        end_idx = content.find(marker_end)
        if end_idx != -1:
            # Remove the old block including the end marker line
            end_line_idx = content.find("\n", end_idx)
            if end_line_idx != -1:
                content = content[:start_idx] + content[end_line_idx + 1 :]
            else:
                content = content[:start_idx]

    # Build new block
    block_lines = [marker_start]
    for item in include_if_configs:
        gitdir = os.path.expanduser(item.get("gitdir", ""))
        path = os.path.expanduser(item.get("path", ""))
        gitdir = gitdir.replace("\\", "/")  # Ensure forward slashes for gitdir
        path = path.replace("\\", "/")  # Ensure forward slashes for path
        # Convert MSYS2-style paths (/c/data/...) to Windows-native (C:/data/...)
        # Git for Windows needs native paths for includeIf gitdir: matching
        if sys.platform == "win32":
            gitdir = re.sub(r"^/([a-zA-Z])/", lambda m: m.group(1).upper() + ":/", gitdir)
        # Ensure trailing slash for gitdir glob matching
        if not gitdir.endswith("/"):
            gitdir += "/"
        block_lines.append(f'[includeIf "gitdir:{gitdir}"]')
        block_lines.append(f"    path = {path}")
    block_lines.append(marker_end)

    new_block = "\n".join(block_lines) + "\n"

    # Append the new block
    if not content.endswith("\n") and content:
        content += "\n"
    content += new_block

    # Write back
    with open(gitconfig_path, "w") as f:
        f.write(content)

    print(f"Added includeIf sections to {gitconfig_path}")


def main(args):
    config = yaml.load(open(args.config, "r"), Loader=yaml.FullLoader)
    local_config = (
        yaml.load(open(args.local_config, "r"), Loader=yaml.FullLoader) if os.path.exists(args.local_config) else {}
    )

    print("=" * 80)
    print("Step 1: Initialize git config directories")
    print("=" * 80)
    git_init_configs(config, local_config)

    print("\n" + "=" * 80)
    print("Step 2: Set git config values")
    print("=" * 80)
    git_config_set(config, local_config)

    print("\n" + "=" * 80)
    print("Step 3: Add includeIf sections to ~/.gitconfig")
    print("=" * 80)
    git_add_includeif(config, local_config)

    print("\n" + "=" * 80)
    print("Step 4: Clean up temporary directories")
    print("=" * 80)
    git_clean_temp_dirs()

    print("\n" + "=" * 80)
    print("Git configuration completed successfully!")
    print("=" * 80)

    # The following code is disabled (was after return statement)
    # Uncomment and modify if you want to enable git repo cloning and bulk operations
    if args.enable_bulk_operations:
        bulk_git_operations(args, config, local_config)


def bulk_git_operations(args, config, local_config):
    """
    Bulk git operations: clone repos, configure them, and optionally commit/pull/push.
    This is the code that was originally after the return statement in main().
    """
    print("\n" + "=" * 80)
    print("Running bulk git operations")
    print("=" * 80)

    parrent_dir = os.path.abspath("..")
    other_git_repos = {
        "20.02_win_dotfiles": "https://github.com/wameri/win_dotfiles.git",
        "20.04_mac_dotfiles": "https://github.com/wameri/mac_dotfiles.git",
        "20.05_mac_ansible_config": "https://github.com/wameri/mac_ansible_config.git",
        "20.01_my_wiki": "https://github.com/wameri/wiki.git",
    }
    for git_repo_name, git_repo_url in other_git_repos.items():
        repo_dir = os.path.join(parrent_dir, git_repo_name)
        if os.path.exists(os.path.join(repo_dir, ".git")):
            continue

        dirty_files = ""
        if os.path.exists(repo_dir):
            dirty_files = repo_dir + "_" + time.strftime("%Y%m%d-%H%M%S")
            shutil.move(repo_dir, dirty_files)
        cmd_clone = f"git clone {git_repo_url} {git_repo_name}"
        run_cmd(cmd_clone, cur_dir=parrent_dir)
        if dirty_files:
            for file in os.listdir(dirty_files):
                file_path = os.path.join(dirty_files, file)
                shutil.move(file_path, repo_dir)
            shutil.rmtree(dirty_files)

    for dirname in os.listdir(parrent_dir):
        work_dir = os.path.join(parrent_dir, dirname)
        if os.path.isdir(work_dir):

            if ".git" not in os.listdir(work_dir):
                break
            print("git dir: ", dirname)
            process_dir(work_dir)


def process_dir(cur_dir):

    git_config_email = "git config --local user.email work.ameri@gmail.com"
    run_cmd(git_config_email, cur_dir=cur_dir)
    git_config_name = "git config --local user.name Ezra Ameri"
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
    parser.add_argument(
        "--enable_bulk_operations",
        action="store_true",
        default=False,
        help="Enable bulk git operations (clone, commit, pull, push)",
    )
    parser.add_argument("--git_commit", action="store_true", default=False, help="Commit changes in all git repos")
    parser.add_argument("--git_pull", action="store_true", default=False, help="Pull changes in all git repos")
    parser.add_argument("--git_push", action="store_true", default=False, help="Push changes in all git repos")
    parser.add_argument("--config", type=str, default="000_configs.yaml", help="Path to main config file")
    parser.add_argument(
        "--local_config", type=str, default="001_local_configs.yaml", help="Path to local config override file"
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args)
