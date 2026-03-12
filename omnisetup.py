#!/usr/bin/env python3
import os
import sys
import platform
import subprocess
import logging
from datetime import datetime
from apps_config import APPS
from hardware_detect import get_hardware_info

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
        print("The GUI will open. Close it when done to continue.")
        logging.info("Starting Chris Titus Tech debloat")
        cmd = 'powershell -ExecutionPolicy Bypass -Command "irm christitus.com/win | iex"'
        subprocess.run(cmd, shell=True)
        print("Chris Titus Tech completed.")
    elif choice == "2":
        print("\nRunning Windows10Debloater...")
        print("The GUI will open. Close it when done to continue.")
        logging.info("Starting Windows10Debloater")
        cmd = 'powershell -ExecutionPolicy Bypass -Command "iwr -useb https://git.io/debloat|iex"'
        subprocess.run(cmd, shell=True)
        print("Windows10Debloater completed.")
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

def install_power_management():
    print("\n=== Power Management Installation ===")
    
    # Detect hardware
    hw_info = get_hardware_info()
    cpu_vendor = hw_info['cpu_vendor']
    has_nvidia = hw_info['has_nvidia']
    
    print(f"\nDetected: {cpu_vendor.upper()} CPU" + (" + NVIDIA GPU" if has_nvidia else ""))
    print("\n--- Basic Options ---")
    print("1. auto-cpufreq (Automatic, recommended)")
    print("2. TLP (Advanced features)")
    
    option_num = 3
    cpu_tool_option = None
    nvidia_tool1_option = None
    nvidia_tool2_option = None
    combo1_option = None
    combo2_option = None
    
    # CPU-specific tool
    print("\n--- CPU-Specific Tools ---")
    if cpu_vendor == 'intel':
        print(f"{option_num}. thermald (Intel thermal management)")
        cpu_tool_option = option_num
        cpu_tool_name = "thermald"
        cpu_tool_pkg = "thermald"
        option_num += 1
    elif cpu_vendor == 'amd':
        print(f"{option_num}. ryzenadj (AMD Ryzen tuning)")
        cpu_tool_option = option_num
        cpu_tool_name = "ryzenadj"
        cpu_tool_pkg = "ryzenadj"
        option_num += 1
    
    # NVIDIA tools
    if has_nvidia:
        print("\n--- NVIDIA GPU Tools ---")
        print(f"{option_num}. envycontrol (NVIDIA GPU switching)")
        nvidia_tool1_option = option_num
        option_num += 1
        print(f"{option_num}. optimus-manager (Advanced NVIDIA switching)")
        nvidia_tool2_option = option_num
        option_num += 1
    
    # Combo options
    if cpu_tool_option or has_nvidia:
        print("\n--- Recommended Combinations ---")
        combo_parts = []
        if cpu_tool_option:
            combo_parts.append(cpu_tool_name)
        if has_nvidia:
            combo_parts.append("envycontrol")
        
        if combo_parts:
            print(f"{option_num}. auto-cpufreq + {' + '.join(combo_parts)}")
            combo1_option = option_num
            option_num += 1
            
            combo_parts_adv = []
            if cpu_tool_option:
                combo_parts_adv.append(cpu_tool_name)
            if has_nvidia:
                combo_parts_adv.append("optimus-manager")
            
            print(f"{option_num}. TLP + {' + '.join(combo_parts_adv)}")
            combo2_option = option_num
            option_num += 1
    
    choice = input("\nSelect option: ").strip()
    
    try:
        distro = platform.freedesktop_os_release().get('ID', '').lower()
    except:
        distro = ''
    
    if choice == "1":
        print("\nInstalling auto-cpufreq...")
        _install_power_tool("auto-cpufreq", distro)
    elif choice == "2":
        print("\nInstalling TLP...")
        _install_power_tool("tlp", distro)
    elif cpu_tool_option and choice == str(cpu_tool_option):
        print(f"\nInstalling {cpu_tool_name}...")
        _install_power_tool(cpu_tool_pkg, distro)
    elif nvidia_tool1_option and choice == str(nvidia_tool1_option):
        print("\nInstalling envycontrol...")
        _install_power_tool("envycontrol", distro)
    elif nvidia_tool2_option and choice == str(nvidia_tool2_option):
        print("\nInstalling optimus-manager...")
        _install_power_tool("optimus-manager", distro)
    elif combo1_option and choice == str(combo1_option):
        print("\nInstalling recommended combo...")
        _install_power_tool("auto-cpufreq", distro)
        if cpu_tool_option:
            _install_power_tool(cpu_tool_pkg, distro)
        if has_nvidia:
            _install_power_tool("envycontrol", distro)
    elif combo2_option and choice == str(combo2_option):
        print("\nInstalling advanced combo...")
        _install_power_tool("tlp", distro)
        if cpu_tool_option:
            _install_power_tool(cpu_tool_pkg, distro)
        if has_nvidia:
            _install_power_tool("optimus-manager", distro)
    else:
        print("Invalid option")
        return
    
    logging.info("Power management installation completed")

def _install_power_tool(tool, distro):
    """Helper function to install power management tools"""
    if 'ubuntu' in distro or 'debian' in distro:
        if tool == "auto-cpufreq":
            run_command("sudo apt update && sudo apt install -y auto-cpufreq")
            run_command("sudo auto-cpufreq --install")
        elif tool == "tlp":
            run_command("sudo apt update && sudo apt install -y tlp tlp-rdw")
            run_command("sudo systemctl enable tlp")
        elif tool == "thermald":
            run_command("sudo apt update && sudo apt install -y thermald")
            run_command("sudo systemctl enable thermald")
        elif tool == "ryzenadj":
            print("Note: ryzenadj requires manual installation from GitHub")
            print("Visit: https://github.com/FlyGoat/RyzenAdj")
        elif tool == "envycontrol":
            run_command("sudo apt update && sudo apt install -y python3-pip")
            run_command("pip3 install envycontrol")
        elif tool == "optimus-manager":
            print("Note: optimus-manager is primarily for Arch-based distros")
            print("Consider using envycontrol instead")
    elif 'fedora' in distro or 'rhel' in distro:
        if tool == "auto-cpufreq":
            run_command("sudo dnf install -y auto-cpufreq")
            run_command("sudo auto-cpufreq --install")
        elif tool == "tlp":
            run_command("sudo dnf install -y tlp tlp-rdw")
            run_command("sudo systemctl enable tlp")
        elif tool == "thermald":
            run_command("sudo dnf install -y thermald")
            run_command("sudo systemctl enable thermald")
        elif tool == "ryzenadj":
            print("Note: ryzenadj requires manual installation from GitHub")
        elif tool == "envycontrol":
            run_command("pip3 install envycontrol")
        elif tool == "optimus-manager":
            print("Note: optimus-manager is primarily for Arch-based distros")
    elif 'arch' in distro:
        if tool == "auto-cpufreq":
            run_command("sudo pacman -S --noconfirm auto-cpufreq")
            run_command("sudo systemctl enable --now auto-cpufreq")
        elif tool == "tlp":
            run_command("sudo pacman -S --noconfirm tlp")
            run_command("sudo systemctl enable tlp")
        elif tool == "thermald":
            run_command("sudo pacman -S --noconfirm thermald")
            run_command("sudo systemctl enable thermald")
        elif tool == "ryzenadj":
            run_command("yay -S --noconfirm ryzenadj-git")
        elif tool == "envycontrol":
            run_command("yay -S --noconfirm envycontrol")
        elif tool == "optimus-manager":
            run_command("yay -S --noconfirm optimus-manager")
            run_command("sudo systemctl enable optimus-manager")

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
        print("2. Install Power Management")
        print("3. Install Applications")
        print("4. Quit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == "1":
            install_linux_de()
        elif choice == "2":
            install_power_management()
        elif choice == "3":
            install_apps()
        elif choice == "4":
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
