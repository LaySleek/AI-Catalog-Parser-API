#!/bin/bash
set -e

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

########################################
# Dependencies
########################################
source "$ROOT_DIR/lib/sudo.sh"
source "$ROOT_DIR/lib/logging.sh"

########################################
# Environment
########################################
export DEBIAN_FRONTEND=noninteractive

########################################
# Utility Functions
########################################

pkg_installed() {
    dpkg -s "$1" &>/dev/null
}

install_packages() {
    local packages=()
    for pkg in "$@"; do
        if ! pkg_installed "$pkg"; then
            packages+=("$pkg")
        fi
    done

    if [ ${#packages[@]} -gt 0 ]; then
        info "Installing packages: ${packages[*]}"
        sudo apt-get install -y "${packages[@]}"
    else
        info "Packages already installed"
    fi
}

command_exists() {
    command -v "$1" >/dev/null 2>&1
}

########################################
# Installation Functions
########################################

########################################
# Docker
########################################

install_docker() {

    if command_exists docker; then
        info "Docker already installed"
        return
    fi

    info "Installing Docker"

    # Add Docker's official GPG key:
    sudo apt-get update
    
    install_packages \
        ca-certificates \
        curl

    sudo install -m 0755 -d /etc/apt/keyrings
    sudo curl -fsSL https://download.docker.com/linux/ubuntu/gpg -o /etc/apt/keyrings/docker.asc
    sudo chmod a+r /etc/apt/keyrings/docker.asc

    # Add the repository to Apt sources:
    sudo tee /etc/apt/sources.list.d/docker.sources <<EOF
Types: deb
URIs: https://download.docker.com/linux/ubuntu
Suites: $(. /etc/os-release && echo "${UBUNTU_CODENAME:-$VERSION_CODENAME}")
Components: stable
Signed-By: /etc/apt/keyrings/docker.asc
EOF

    sudo apt-get update

    install_packages \
        docker-ce \
        docker-ce-cli \
        containerd.io \
        docker-buildx-plugin \
        docker-compose-plugin

    if ! getent group docker >/dev/null; then
        sudo groupadd docker
    fi
    sudo usermod -aG docker $USER

    success "Docker installation completed"
}

########################################
# CUDA Toolkit
########################################

install_cuda() {

    if command_exists nvidia-smi; then
        info "CUDA Toolkit already installed"
        return
    fi

    info "Installing CUDA Toolkit 13.3"

    local tmp
    tmp=$(mktemp -d)
    pushd "$tmp" >/dev/null

    source /etc/os-release
    UBUNTU_VERSION="${VERSION_ID//./}"

    wget https://developer.download.nvidia.com/compute/cuda/repos/${UBUNTU_VERSION}/x86_64/cuda-keyring_1.1-1_all.deb
    sudo dpkg -i cuda-keyring_1.1-1_all.deb
    sudo apt-get update
    sudo apt-get -y install cuda-toolkit-13-3

    popd >/dev/null
    rm -rf "$tmp"

    install_packages nvidia-open

    success "CUDA Toolkit installed"
}

########################################
# NVIDIA Container Toolkit
########################################

install_nvidia_container_toolkit() {

    if pkg_installed nvidia-container-toolkit; then
        info "NVIDIA Container Toolkit already installed"
        return
    fi

    info "Installing NVIDIA Container Toolkit"

    sudo apt-get update
    
    install_packages \
        ca-certificates \
        curl \
        gnupg2

    curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey \
        | sudo gpg --dearmor -o \
        /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

    curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list \
        | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' \
        | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

    sudo apt-get update

    NVIDIA_CONTAINER_TOOLKIT_VERSION=1.19.1-1

    install_packages \
        nvidia-container-toolkit=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
        nvidia-container-toolkit-base=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
        libnvidia-container-tools=${NVIDIA_CONTAINER_TOOLKIT_VERSION} \
        libnvidia-container1=${NVIDIA_CONTAINER_TOOLKIT_VERSION}

    sudo nvidia-ctk runtime configure --runtime=docker
    sudo systemctl restart docker

    success "NVIDIA Container Toolkit installed"
}

########################################
# Docker cgroup
########################################

configure_docker_cgroup() {

    local daemon_file="/etc/docker/daemon.json"

    info "Configuring Docker cgroup driver"

    # Ensure jq is installed
    if ! command_exists jq; then
        install_packages jq
    fi

    # Create daemon.json if it does not exist
    if [ ! -f "$daemon_file" ]; then
        sudo mkdir -p /etc/docker
        echo '{}' | sudo tee "$daemon_file" >/dev/null
    fi

    # Check if the required cgroup driver is already configured
    if jq -e '
        has("exec-opts") and
        (.["exec-opts"] | index("native.cgroupdriver=cgroupfs"))
    ' "$daemon_file" >/dev/null; then
        info "cgroupfs already configured"
        return
    fi

    local tmp
    tmp=$(mktemp)

    # Create exec-opts in daemon.js
    jq --indent 2 '
        if has("exec-opts") then
            .["exec-opts"] |= ( . + ["native.cgroupdriver=cgroupfs"] | unique )
        else
            . + { "exec-opts": ["native.cgroupdriver=cgroupfs"] }
        end
    ' "$daemon_file" > "$tmp"

    sudo mv "$tmp" "$daemon_file"

    sudo systemctl restart docker

    success "daemon.json updated with cgroupfs"
}
########################################
# Execution
########################################

step "Initializing the environment..."
require_sudo

install_docker
install_cuda
install_nvidia_container_toolkit
configure_docker_cgroup

success "The environment has been initialized."