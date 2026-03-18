#!/bin/bash

BRANCH="${INSTALLER_BRANCH:-main}"
BASE_URL="https://raw.githubusercontent.com/Jessiebrig/OmniSetup/$BRANCH"

mkdir -p omnisetup && cd omnisetup

# Always check and download missing files
echo "Checking for required files..."

DOWNLOAD_NEEDED=0

[ ! -f "omnisetup.py" ] && DOWNLOAD_NEEDED=1
[ ! -f "omnisetup_gui.py" ] && DOWNLOAD_NEEDED=1
[ ! -f "apps_config.py" ] && DOWNLOAD_NEEDED=1

if [ $DOWNLOAD_NEEDED -eq 1 ]; then
    echo "Downloading OmniSetup files from branch: $BRANCH"

    if command -v curl &> /dev/null; then
        curl -fsSL "$BASE_URL/omnisetup.py" -o omnisetup.py || { echo "Failed to download omnisetup.py"; exit 1; }
        curl -fsSL "$BASE_URL/omnisetup_gui.py" -o omnisetup_gui.py || { echo "Failed to download omnisetup_gui.py"; exit 1; }
        curl -fsSL "$BASE_URL/apps_config.py" -o apps_config.py || { echo "Failed to download apps_config.py"; exit 1; }
    elif command -v wget &> /dev/null; then
        wget -q "$BASE_URL/omnisetup.py" -O omnisetup.py || { echo "Failed to download omnisetup.py"; exit 1; }
        wget -q "$BASE_URL/omnisetup_gui.py" -O omnisetup_gui.py || { echo "Failed to download omnisetup_gui.py"; exit 1; }
        wget -q "$BASE_URL/apps_config.py" -O apps_config.py || { echo "Failed to download apps_config.py"; exit 1; }
    else
        echo "Neither curl nor wget found. Please install one of them."
        exit 1
    fi

    echo "Download complete!"
else
    echo "All files present."
fi

# Verify files exist
if [ ! -f "omnisetup.py" ]; then
    echo "Error: omnisetup.py not found after download!"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    if command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3
    elif command -v dnf &> /dev/null; then
        sudo dnf install -y python3
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python3
    else
        echo "Could not detect package manager. Please install Python 3 manually."
        exit 1
    fi
fi

# Check if display is available (GUI possible)
if [ -n "$DISPLAY" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    if ! python3 -c "import tkinter" &> /dev/null; then
        echo "Python tkinter is not installed. Installing..."
        if command -v apt &> /dev/null; then
            sudo apt install -y python3-tk
        elif command -v dnf &> /dev/null; then
            sudo dnf install -y python3-tkinter
        elif command -v pacman &> /dev/null; then
            sudo pacman -S --noconfirm tk
        fi
    fi
    echo "Starting GUI..."
    python3 omnisetup_gui.py
else
    echo "No display detected. Using CLI mode..."
    python3 omnisetup.py < /dev/tty
fi
