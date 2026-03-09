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
- **Install Applications** in one go

### Applications Installed
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

### Windows (PowerShell as Administrator)

**Important:** Run PowerShell as Administrator. If this is your first time running PowerShell scripts, you may need to enable script execution:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then run the installation:

```powershell
git clone https://github.com/YOUR_USERNAME/OmniSetup.git && cd OmniSetup && .\setup.ps1
```

### Linux (Terminal as Root/Sudo)

```bash
git clone https://github.com/YOUR_USERNAME/OmniSetup.git && cd OmniSetup && chmod +x setup.sh && ./setup.sh
```

## Quick Start

If you've already cloned the repository, run:

### Windows (CMD)
```cmd
setup.bat
```

### Windows (PowerShell)
```powershell
.\setup.ps1
```

### Linux (Terminal)
```bash
./setup.sh
```

## Requirements

- **Python 3.6+** (auto-installed on Windows if missing, usually pre-installed on Linux)
- **Administrator/Root privileges** for system modifications

## Linux Installation Notes

For the cleanest installation experience, it's recommended to install on a fresh Linux system **without a desktop environment** (server/minimal install). This ensures:
- No conflicting desktop environments
- Clean package dependencies
- Optimal performance
- No pre-installed bloatware

## Notes

- On Windows, some operations require running as Administrator
- On Linux, you may need to enter your sudo password
- The script will detect your platform automatically
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
