#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import logging
from datetime import datetime
from apps_config import APPS

# Setup logging
log_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'omnisetup.log')
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        logging.StreamHandler()
    ]
)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def is_admin():
    if os.name == 'nt':
        try:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except:
            return False
    else:
        return os.geteuid() == 0

def run_command(cmd, shell=True):
    try:
        logging.info(f"Running: {cmd}")
        result = subprocess.run(cmd, shell=shell, check=True, capture_output=True, text=True)
        if result.stdout:
            logging.info(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e}")
        if e.stderr:
            logging.error(e.stderr)
        return False

def check_python_windows():
    try:
        result = subprocess.run(['python', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except:
        return False

def install_python_windows():
    print("\nPython not found. Installing Python...")
    logging.info("Installing Python via winget")
    if run_command('winget install --id Python.Python.3.12 --silent --accept-package-agreements --accept-source-agreements'):
        print("Python installed successfully. Please restart this script.")
        logging.info("Python installation completed")
        sys.exit(0)
    else:
        print("Failed to install Python. Please install manually from https://www.python.org/")
        logging.error("Python installation failed")
        sys.exit(1)

def get_current_branch():
    try:
        result = subprocess.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except:
        return None

def get_available_branches():
    try:
        subprocess.run(['git', 'fetch', '--all'], capture_output=True, check=True)
        result = subprocess.run(['git', 'branch', '-r'], 
                              capture_output=True, text=True, check=True)
        branches = []
        for line in result.stdout.split('\n'):
            line = line.strip()
            if line and 'origin/' in line and '->' not in line:
                branch = line.replace('origin/', '')
                branches.append(branch)
        return branches
    except:
        return ['main']

def switch_branch(branch):
    try:
        logging.info(f"Switching to branch: {branch}")
        subprocess.run(['git', 'checkout', branch], check=True, capture_output=True)
        subprocess.run(['git', 'pull'], check=True, capture_output=True)
        return True
    except:
        return False

def check_for_updates():
    current = get_current_branch()
    if not current:
        logging.warning("Not a git repository, skipping branch check")
        return
    
    print(f"\nCurrent branch: {current}")
    branches = get_available_branches()
    
    if len(branches) > 1:
        print("\nAvailable branches:")
        for i, branch in enumerate(branches, 1):
            marker = " (current)" if branch == current else ""
            print(f"{i}. {branch}{marker}")
        
        choice = input("\nSwitch branch? (Enter number or press Enter to continue): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(branches):
            new_branch = branches[int(choice) - 1]
            if new_branch != current:
                if switch_branch(new_branch):
                    print(f"Switched to {new_branch}. Restarting...")
                    logging.info(f"Switched to branch: {new_branch}")
                    os.execv(sys.executable, [sys.executable] + sys.argv)
                else:
                    print("Failed to switch branch")
                    logging.error("Branch switch failed")

def install_windows_debloat():
    print("\n=== Windows Debloat ===")
    print("1. Chris Titus Tech Debloat")
    print("2. Windows10Debloater")
    choice = input("\nChoose option (1-2): ").strip()
    
    if choice == "1":
        print("\nRunning Chris Titus Tech Windows Utility...")
        logging.info("Starting Chris Titus Tech debloat")
        cmd = 'powershell -Command "irm christitus.com/win | iex"'
        run_command(cmd)
    elif choice == "2":
        print("\nRunning Windows10Debloater...")
        logging.info("Starting Windows10Debloater")
        cmd = 'powershell -Command "iwr -useb https://git.io/debloat|iex"'
        run_command(cmd)
    else:
        print("Invalid option")
        logging.warning(f"Invalid debloat option: {choice}")

def install_windows_runtimes():
    print("\n=== Installing Visual C++ & .NET Framework ===")
    logging.info("Starting Windows runtimes installation")
    
    print("Installing Visual C++ Redistributables...")
    vcredist_urls = [
        "https://aka.ms/vs/17/release/vc_redist.x64.exe",
        "https://aka.ms/vs/17/release/vc_redist.x86.exe"
    ]
    for url in vcredist_urls:
        run_command(f'powershell -Command "Invoke-WebRequest -Uri {url} -OutFile vcredist.exe; Start-Process vcredist.exe -ArgumentList \'/install\',\'/quiet\',\'/norestart\' -Wait; Remove-Item vcredist.exe"')
    
    print("Installing .NET Framework...")
    run_command('winget install Microsoft.DotNet.Framework.DeveloperPack_4 --silent --accept-package-agreements --accept-source-agreements')
    
    logging.info("Windows runtimes installation completed")

def install_linux_de():
    print("\n=== Desktop Environment Installation ===")
    print("1. KDE Plasma")
    print("2. XFCE")
    choice = input("\nChoose DE (1-2): ").strip()
    
    try:
        distro = platform.freedesktop_os_release().get('ID', '').lower()
    except:
        distro = ''
    
    logging.info(f"Installing DE on {distro}")
    
    if 'ubuntu' in distro or 'debian' in distro:
        if choice == "1":
            print("\nInstalling KDE Plasma...")
            run_command("sudo apt update && sudo apt install -y kde-plasma-desktop")
        elif choice == "2":
            print("\nInstalling XFCE...")
            run_command("sudo apt update && sudo apt install -y xfce4")
        else:
            print("Invalid option")
            return
    elif 'fedora' in distro or 'rhel' in distro:
        if choice == "1":
            print("\nInstalling KDE Plasma...")
            run_command("sudo dnf install -y @kde-desktop-environment")
        elif choice == "2":
            print("\nInstalling XFCE...")
            run_command("sudo dnf install -y @xfce-desktop-environment")
        else:
            print("Invalid option")
            return
    elif 'arch' in distro:
        if choice == "1":
            print("\nInstalling KDE Plasma...")
            run_command("sudo pacman -S --noconfirm plasma-meta")
        elif choice == "2":
            print("\nInstalling XFCE...")
            run_command("sudo pacman -S --noconfirm xfce4")
        else:
            print("Invalid option")
            return
    else:
        print(f"Unsupported distribution: {distro}")
        logging.error(f"Unsupported distribution: {distro}")
        return
    
    logging.info("DE installation completed")

def get_app_list():
    """Returns the application list for both platforms"""
    return APPS

def install_apps():
    print("\n=== Installing Applications ===")
    logging.info("Starting application installation")
    
    apps = get_app_list()
    
    if os.name == 'nt':
        print("\nUsing winget to install applications...")
        for name, pkg in apps['windows'].items():
            print(f"Installing {name}...")
            run_command(f'winget install --id {pkg} --silent --accept-package-agreements --accept-source-agreements')
    else:
        try:
            distro = platform.freedesktop_os_release().get('ID', '').lower()
        except:
            distro = ''
        
        if 'ubuntu' in distro or 'debian' in distro:
            print("\nUsing apt to install applications...")
            run_command("sudo apt update")
            for name, pkg in apps['linux'].items():
                print(f"Installing {name}...")
                run_command(f"sudo apt install -y {pkg}")
        elif 'fedora' in distro:
            print("\nUsing dnf to install applications...")
            for name, pkg in apps['linux'].items():
                print(f"Installing {name}...")
                run_command(f"sudo dnf install -y {pkg}")
        elif 'arch' in distro:
            print("\nUsing pacman to install applications...")
            for name, pkg in apps['linux'].items():
                print(f"Installing {name}...")
                run_command(f"sudo pacman -S --noconfirm {pkg}")
        else:
            print(f"Unsupported distribution: {distro}")
            logging.error(f"Unsupported distribution: {distro}")
            return
    
    logging.info("Application installation completed")

def main_menu():
    clear_screen()
    system = platform.system()
    print("=" * 50)
    print("         OMNISETUP - Universal Setup Tool")
    print("=" * 50)
    print(f"Platform: {system} ({platform.release()})")
    print("=" * 50)
    
    if system == "Windows":
        print("\n1. Debloat Windows")
        print("2. Install Visual C++ & .NET Framework")
        print("3. Install Applications")
        print("4. Quit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            install_windows_debloat()
        elif choice == "2":
            install_windows_runtimes()
        elif choice == "3":
            install_apps()
        elif choice == "4":
            logging.info("User quit")
            sys.exit(0)
        else:
            print("Invalid option")
            logging.warning(f"Invalid menu option: {choice}")
    
    elif system == "Linux":
        print("\n1. Install Desktop Environment (KDE/XFCE)")
        print("2. Install Applications")
        print("3. Quit")
        
        choice = input("\nSelect option (1-3): ").strip()
        
        if choice == "1":
            install_linux_de()
        elif choice == "2":
            install_apps()
        elif choice == "3":
            logging.info("User quit")
            sys.exit(0)
        else:
            print("Invalid option")
            logging.warning(f"Invalid menu option: {choice}")
    
    input("\nPress Enter to continue...")
    main_menu()

if __name__ == "__main__":
    logging.info("=" * 50)
    logging.info("OmniSetup started")
    logging.info(f"Platform: {platform.system()} {platform.release()}")
    logging.info("=" * 50)
    
    # Check for Python on Windows
    if os.name == 'nt' and not check_python_windows():
        install_python_windows()
    
    # Check for updates/branch selection
    check_for_updates()
    
    if not is_admin():
        print("\nWarning: Running without administrator/root privileges.")
        print("Some operations may fail.")
        logging.warning("Running without admin privileges")
        input("Press Enter to continue anyway...")
    
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\nExiting...")
        logging.info("User interrupted (Ctrl+C)")
        sys.exit(0)
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\nError: {e}")
        print(f"Check log file: {log_file}")
        sys.exit(1)
