# FROM mcr.microsoft.com/devcontainers/python:3.12-bookworm
# 
# # sets the cuda variables for CUDA support in docker
# ENV NVIDIA_VISIBLE_DEVICES 
# ENV NVIDIA_DRIVER_CAPABILITIES 
# 
# # Installs Poetry, Mypy, Ruff and Monkeytype
# RUN pipx install poetry && pipx install mypy && pipx install ruff && pipx install MonkeyType
# 
# # copies the requirements file from the project root to the container and installs it
# # copy "noop.txt" so the COPY instruction does not fail if no requirements.txt exists.
# COPY requirements.txt* .devcontainer/noop.txt /tmp/pip-tmp/
# RUN if [ -f "/tmp/pip-tmp/requirements.txt" ]; then pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt; fi \
#     && rm -rf /tmp/pip-tmp
#     
# FROM mcr.microsoft.com/azureml/openmpi4.1.0-ubuntu22.04
# RUN apt-get update -y
# RUN apt-get install -y libzbar0 libgl1
# RUN wget -q https://challenge.blob.core.windows.net/video-call-mos/ffmpeg-git-amd64-static.tar.xz
# RUN tar xf ffmpeg-git-amd64-static.tar.xz
# RUN mv ffmpeg-git-*-amd64-static/ffmpeg ffmpeg-git-*-amd64-static/ffprobe /usr/local/bin/
# RUN whereis ffmpeg
# RUN wget -q -O azcopy_v10.tar.gz https://aka.ms/downloadazcopy-v10-linux && tar -xf azcopy_v10.tar.gz --strip-components=1
# RUN mv azcopy /usr/local/bin/
# RUN whereis azcopy




FROM alpine:edge

RUN  apk add zsh git lazygit neovim ripgrep alpine-sdk --update
RUN  apk add bat fd htop neofetch tmux ripgrep starship --update
RUN  apk add zsh-autosuggestions zsh-history-substring-search zsh-syntax-highlighting --update
# RUN apk add zsh-vi-mode-git --update

WORKDIR /root


CMD ["zsh"]

