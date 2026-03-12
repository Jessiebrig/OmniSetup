#!/bin/bash

BASE_URL="https://raw.githubusercontent.com/Jessiebrig/OmniSetup/refs/heads/main"

# Always check and download missing files
echo "Checking for required files..."

DOWNLOAD_NEEDED=0

if [ ! -f "omnisetup.py" ]; then
    DOWNLOAD_NEEDED=1
fi

if [ ! -f "omnisetup_gui.py" ]; then
    DOWNLOAD_NEEDED=1
fi

if [ ! -f "apps_config.py" ]; then
    DOWNLOAD_NEEDED=1
fi

if [ $DOWNLOAD_NEEDED -eq 1 ]; then
    echo "Downloading OmniSetup files..."
    
    # Try curl first, fallback to wget
    if command -v curl &> /dev/null; then
        curl -fsSL -O "$BASE_URL/omnisetup.py" || { echo "Failed to download omnisetup.py"; exit 1; }
        curl -fsSL -O "$BASE_URL/omnisetup_gui.py" || { echo "Failed to download omnisetup_gui.py"; exit 1; }
        curl -fsSL -O "$BASE_URL/apps_config.py" || { echo "Failed to download apps_config.py"; exit 1; }
    elif command -v wget &> /dev/null; then
        wget -q "$BASE_URL/omnisetup.py" || { echo "Failed to download omnisetup.py"; exit 1; }
        wget -q "$BASE_URL/omnisetup_gui.py" || { echo "Failed to download omnisetup_gui.py"; exit 1; }
        wget -q "$BASE_URL/apps_config.py" || { echo "Failed to download apps_config.py"; exit 1; }
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
    # Display available, try GUI
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
    # No display, use CLI
    echo "No display detected. Using CLI mode..."
    python3 omnisetup.py
fi
