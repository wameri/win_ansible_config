
# Windows feature

turn on Windows subsystem for linux
enable win for developer: https://learn.microsoft.com/en-us/windows/apps/get-started/enable-your-device-for-development
wsl --update
wsl --install

# Install with winget

```
winget update --all
winget install {configs[winget_packages]}
    
```

# install scoop
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

    
# choco packages:
    1. TODO 

# keepass pluging
    Download https://github.com/pfn/keepasshttp
    1. Copy to C:\Program Files (x86)\KeePass2x\Plugins

# clink setup 

    Usage at: GitHub - chrisant996/clink: Bash's powerful command line editing in cmd.exe

# Setup starship 

    Bash: Add the following to the end of ~/.bashrc: C:\Users\ezraameri\.bash_profile
    eval"$(starship init bash)"
    ```
    Cmd: 
    %LocalAppData%\clink\starship.lua with the following contents: C:\Users\ezraameri\AppData\Local\clink\starship.lua
    load(io.popen('starship init cmd'):read("*a"))()
    
    Powershell:
    Add the following to the end of your PowerShell configuration (find it by running $PROFILE): 
    C:\Users\ezraameri\onedrive_ezraameri\OneDrive - Microsoft\Documents\PowerShell\Microsoft.PowerShell_profile.ps1
    Invoke-Expression(&starship init powershell)
    
    Starship config file: C:\Users\ezraameri\.config\starship.toml
    Config from here: Configuration | Starship
    ```

# Nvim

config file in C:\Users\ezraameri\AppData\Local\nvim\init.nvim

powershell
```
iwr -useb https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim |`
    ni "$(@($env:XDG_DATA_HOME, $env:LOCALAPPDATA)[$null -eq $env:XDG_DATA_HOME])/nvim-data/site/autoload/plug.vim" -Force

:PlugInstall to install the plugins
:PlugUpdate to install or update the plugins
:PlugDiff to review the changes from the last update
```

# wsl setup

```
sudo apt install thunar python3-pip python3-venv -y

git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"

python3 -m venv dev_env
source dev_env/bin/activate

code . 

install vscode extenstion in wsl 
```



# docker 

```
 Settings > Resources > WSL Integration.
 select ubuntu
```


# git lfs

do this then add and commit the files
```
 git lfs install
 git lfs track "*.jpg"
 git lfs track "*.png"
 git lfs pull
 
```

# visual studio 

1. install visvim
2. install theme catpuchin

# fonts 

[github nerdfonts](https://github.com/ryanoasis/nerd-fonts/tags)
[comic sans](https://github.com/xtevenx/ComicMonoNF)

# conda 

## install 

update path 
%LOCALAPPDATA%/miniconda3
%LOCALAPPDATA%/miniconda3/scripts
%LOCALAPPDATA%/miniconda3/library/bin

```
conda update conda
Conda init cmd.exe
Conda init powershell

```

hit: "modified      HKEY_CURRENT_USER\Software\Microsoft\Command Processor\AutoRun"

## uninstall 

```
conda install anaconda-clean
anaconda-clean
uninstall 
fix command prompt issue
C:\Windows\System32\reg.exe DELETE "HKCU\Software\Microsoft\Command Processor" /v AutoRun /f
```
