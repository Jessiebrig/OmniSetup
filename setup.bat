@echo off
python omnisetup.py
if errorlevel 1 (
    echo Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
)
