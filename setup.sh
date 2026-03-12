#!/bin/bash

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
