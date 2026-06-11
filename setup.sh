#!/bin/bash

BASE_URL="https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main"

echo "Checking for required files..."

DOWNLOAD_NEEDED=0
for f in omnisetup.py omnisetup_gui.py apps_config.py; do
    [ ! -f "$f" ] && DOWNLOAD_NEEDED=1
done

if [ $DOWNLOAD_NEEDED -eq 1 ]; then
    echo "Downloading OmniSetup files..."
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

# Check Python 3
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is not installed. Installing..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3
    elif command -v apt &> /dev/null; then
        sudo apt update && sudo apt install -y python3
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm python3
    else
        echo "Could not detect package manager. Please install Python 3 manually."
        exit 1
    fi
fi

# Check tkinter
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "Installing python3-tkinter..."
    if command -v dnf &> /dev/null; then
        sudo dnf install -y python3-tkinter
    elif command -v apt &> /dev/null; then
        sudo apt install -y python3-tk
    elif command -v pacman &> /dev/null; then
        sudo pacman -S --noconfirm tk
    fi
fi

echo "Starting OmniSetup..."
python3 omnisetup_gui.py
