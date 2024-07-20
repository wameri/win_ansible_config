
# Windows feature

turn on Windows subsystem for linux
wsl --update
wsl --install

# Install with winget

```
winget update --all
winget install 
    Vscode
    Canonical.Ubuntu.2204
    Debian.Debian
    whitewaterfoundry.fedora-remix-for-wsl
    Docker.DockerDesktop
    DominikReichl.KeePass
    Microsoft.msmpisdk  
    Microsoft.PowerShell             
    --id Starship.Starship
    chrisant996.Clink 
    7zip.7zip
    cURL.cURL
    Neovim.Neovim
    OpenJS.NodeJS
    dbrgn.tealdeer
    LLVM.LLVM
    Google.Chrome 

```
# install scoop
Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression

# Scoop programs: 
    1. Ffmpeg
    2. Ninja
    
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
    %LocalAppData%\clink\starship.lua with the following contents: C:\Users\ezraameri\AppData\Local\clinkstarship.lua
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
sudo apt install 
thunar
python3-pip 
python3-venv

git config --global credential.helper "/mnt/c/Program\ Files/Git/mingw64/bin/git-credential-manager.exe"

python3 -m venv dev_env
source dev_env/bin/activate

code . 

install vscode extenstion in wsl 
```


