#!/bin/bash
python3 omnisetup_gui.py || {
    echo "Python 3 is not installed"
    echo "Please install Python 3 using your package manager"
    exit 1
}
