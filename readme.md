
# Bootstrap

1. winget install Google.Chrome
2. clone this repo
3. install anaconda

```shell
winget install Anaconda.Miniconda3 
```

4.install yaml in anaconda prompt base env

```shell
pip install PyYAML
```

5.update conda in windows path

- "%LOCALAPPDATA%/miniconda3"
- "%LOCALAPPDATA%/miniconda3/scripts"
- "%LOCALAPPDATA%/miniconda3/library/bin"

6.init terminals

```shell
conda update conda
Conda init cmd.exe
Conda init powershell
```

In case of error for cmd prompt
hit: "modified      HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun"

7.install scoop

  ```shell
  Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
  ```

8.python scripts

8.1 bootstrap.py
8.2 git tools
8.3 link dotfiles
8.4 vscode
8.5 custom themes
8.6 flatten fonts
8.7 conda

# llvm

add to system environment path C:\Program Files\LLVM\bin

# Nvim

config file in C:\Users\ezraameri\AppData\Local\nvim\init.nvim

if Plug does not exist run

```powershell
iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim |`
    ni "$(@($env:XDG_DATA_HOME, $env:LOCALAPPDATA)[$null -eq $env:XDG_DATA_HOME])/nvim-data/site/autoload/plug.vim" -Force
```

```vim
:PlugInstall to install the plugins
:PlugUpdate to install or update the plugins
:PlugDiff to review the changes from the last update
```

# git lfs

do this then add and commit the files

```shell
 git lfs install
 git lfs track "*.jpg"
 git lfs track "*.png"
 git lfs track "*.deskthemepack"
 git lfs pull
```

# visual studio

1. install visvim
2. install theme catpuchin
3. install noctis(vscode porting)
4. TODO convert vscode theme to vs: <https://github.com/microsoft/theme-converter-for-vs>

# wsl setup

```wsl
sudo apt install thunar python3-pip python3-venv -y

git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"

python3 -m venv dev_env
source dev_env/bin/activate

code . 

install vscode extenstion in wsl 
```

# docker

- Settings > Resources > WSL Integration.
- select ubuntu

# First time only for dotfiles

## clink setup

Usage at: [clink github](https://chrisant996.github.io/clink/clink.html)

## Setup starship

```bash
    # end of file
    #~/.bashrc: 
    #C:\Users\ezraameri\.bash_profile
    eval"$(starship init bash)"
```

```cmd
    // %LocalAppData%\clink\starship.lua 
    // C:\Users\ezraameri\AppData\Local\clink\starship.lua
    load(io.popen('starship init cmd'):read("*a"))()
```

```powershell
    // Add the following to the end of your PowerShell configuration (find it by running $PROFILE): 
    // C:\Users\ezraameri\onedrive_ezraameri\OneDrive - Microsoft\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    Invoke-Expression(&starship init powershell)
```

starthip config file: C:\Users\ezraameri\.config\starship.toml

# conda uninstall

```cmd
conda install anaconda-clean
anaconda-clean
uninstall 
fix command prompt issue
C:\Windows\System32\reg.exe DELETE "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f
```

# fonts

[github nerdfonts](https://github.com/ryanoasis/nerd-fonts/tags)
[comic sans](https://github.com/xtevenx/ComicMonoNF)

# keepass pluging

Download <https://github.com/pfn/keepasshttp>

1. Copy to C:\Program Files (x86)\KeePass2x\Plugins

# choco packages

TODO.
