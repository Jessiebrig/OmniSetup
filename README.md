# OmniSetup

Universal setup tool for fresh Windows and Linux installations. One command to rule them all.

## Features

### Windows
- **Install Visual C++ Redistributables & .NET Framework**
- **Debloat Windows 10/11** - Runs third-party debloat tools:
  - [Chris Titus Tech's Windows Utility](https://github.com/ChrisTitusTech/winutil)
  - [Windows10Debloater](https://github.com/Sycnex/Windows10Debloater)
- **Install Applications** in one go

### Linux
- **Install Desktop Environments** (KDE Plasma or XFCE)
- **Install Power Management Tools** - Hardware-aware optimization:
  - auto-cpufreq (Automatic CPU optimization)
  - TLP (Comprehensive power management)
  - thermald (Intel thermal management)
  - ryzenadj (AMD Ryzen tuning)
  - envycontrol (NVIDIA GPU switching)
  - optimus-manager (Advanced NVIDIA management)
- **Install Applications** in one go

### Applications Installed

**Browsers:**
- Brave Browser
- Google Chrome
- Mozilla Firefox

**Communication:**
- Slack
- Telegram
- Zoom

**Media & Utilities:**
- VLC Media Player
- Lightshot (Windows only)
- Google Drive (Windows only)

**Development:**
- Python
- Visual Studio Code
- Notepad++ (Windows only)
## One-Line Installation

Clones the repository and automatically runs the setup script:

### Windows (CMD or PowerShell as Administrator)

```cmd
git clone https://github.com/Jessiebrig/OmniSetup.git && cd OmniSetup && setup.cmd
```

### Linux (Terminal as Root/Sudo)

```bash
git clone https://github.com/Jessiebrig/OmniSetup.git && cd OmniSetup && chmod +x setup.sh && ./setup.sh
```

## Quick Start

If you've already cloned the repository, run:

### Windows
```cmd
setup.cmd
```

### Linux
```bash
./setup.sh
```

## Requirements

- **Git** (for cloning repository and branch selection, auto-installed on Windows if missing)
- **Python 3.8+** (latest version auto-installed on Windows if missing, usually pre-installed on Linux)
- **Administrator/Root privileges** for system modifications

## Linux Installation Notes

For the cleanest installation experience, it's recommended to install on a fresh Linux system **without a desktop environment** (server/minimal install). This ensures:
- No conflicting desktop environments
- Clean package dependencies
- Optimal performance
- No pre-installed bloatware

### Git Not Installed?

On minimal Debian installations, Git is not included by default. After enabling networking, install Git first:

```bash
sudo apt update
sudo apt install git -y
```

### Network Not Working on Fresh Debian CLI Install?

On minimal Debian installations, networking may not start automatically. Before running OmniSetup, you need to enable your network connection:

**For Wired/Ethernet Connection:**

1. Find your network interface name:
```bash
ip a
```
Look for interface like `enp1s0`, `eth0`, `ens33` (not `lo`)

2. Bring the interface up and configure:
```bash
sudo ip link set enp1s0 up
sudo dhcpcd enp1s0
```
(Replace `enp1s0` with your actual interface name)

3. Test connection:
```bash
ping -c 3 google.com
ping -c 3 github.com
```

**For WiFi Connection:**

1. Find your WiFi interface:
```bash
ip a
```
Look for interface like `wlan0`, `wlp2s0`

2. Connect to your network:
```bash
sudo ip link set wlan0 up
wpa_passphrase "YourNetworkName" "YourPassword" | sudo tee /etc/wpa_supplicant.conf
sudo wpa_supplicant -B -i wlan0 -c /etc/wpa_supplicant.conf
sudo dhcpcd wlan0
```
(Replace `wlan0` with your actual interface name)

3. Test connection:
```bash
ping -c 3 google.com
```

Once networking is active, you can clone and run OmniSetup!

## Power Management Explained

OmniSetup automatically detects your hardware (CPU vendor and GPU) and offers relevant power optimization tools:

### CPU Power Management
- **auto-cpufreq**: Automatically adjusts CPU frequency based on usage and battery state. Set it and forget it.
- **TLP**: Advanced power management with more configuration options. Controls CPU, disk, USB, and more.

### CPU-Specific Tools
- **thermald** (Intel): Prevents thermal throttling on Intel CPUs by managing temperature thresholds.
- **ryzenadj** (AMD): Fine-tune power limits and performance on AMD Ryzen processors.

### NVIDIA GPU Management (Laptops Only)

If you have a laptop with NVIDIA GPU (Optimus/hybrid graphics), GPU switching tools are essential:

**The Problem:**
- By default, NVIDIA GPU runs constantly, draining battery 2-3x faster
- Laptop runs hot and loud even during simple tasks

**The Solution:**
- **envycontrol**: Simple GPU mode switching (Integrated/Hybrid/NVIDIA)
  - Integrated mode: Use Intel/AMD iGPU only (best battery life)
  - Hybrid mode: Automatic switching based on application
  - NVIDIA mode: Always use NVIDIA GPU (best performance)

- **optimus-manager**: Advanced switching with more control (Arch-based distros)
  - Similar to envycontrol but with additional configuration options

**What gets installed:**
- The tool itself (Python package or system package)
- Systemd services (for auto-cpufreq, TLP, thermald, optimus-manager)
- Configuration files in appropriate locations

**After installation:**
- Most tools start automatically on boot
- GPU switching requires logout/reboot to take effect
- Use `envycontrol -s integrated` to switch to battery-saving mode
- Use `envycontrol -s nvidia` to switch to performance mode

## Notes

- OmniSetup uses a graphical interface (GUI) for easy checkbox-based selection
- On Windows, some operations require running as Administrator
- On Linux, you may need to enter your sudo password
- The script will detect your platform and hardware automatically
- Not all applications are available on all Linux distributions
- Installation logs are saved to `omnisetup.log` in the project directory
- Branch selection available on startup for testing experimental features

## About

This script was created for personal convenience during frequent fresh installations. Currently being refined and expanded with more features for general use. Contributions and suggestions are welcome!

## License

MIT License - Feel free to modify and distribute

## Support OmniSetup

If OmniSetup has saved you time and made your fresh installations easier, consider supporting its continued development:

[Buy me a coffee](https://ko-fi.com/jessiebrig) - Help fuel late-night coding sessions and new features!

[PayPal](https://paypal.me/jessiebrig) - Direct support via PayPal

Your support helps keep OmniSetup free and continuously improving. Every contribution, no matter how small, makes a difference!

---

*One command to set them all up.*
