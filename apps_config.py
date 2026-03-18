"""
OmniSetup Application Configuration
Single source of truth for all applications and categories
"""

# cross_platform: shown on both Windows and Linux
# windows_only: shown only on Windows
# install_method: 'winget', 'apt', 'deb', 'repo'
# pkg: package name or URL template (use {arch} for architecture)

APPS = {
    'cross_platform': {
        'Brave Browser': {
            'winget': 'Brave.Brave',
            'linux': {
                'method': 'repo',
                'repo_cmds': [
                    'sudo curl -fsSLo /usr/share/keyrings/brave-browser-archive-keyring.gpg https://brave-browser-apt-release.s3.brave.com/brave-browser-archive-keyring.gpg',
                    'echo "deb [signed-by=/usr/share/keyrings/brave-browser-archive-keyring.gpg] https://brave-browser-apt-release.s3.brave.com/ stable main" | sudo tee /etc/apt/sources.list.d/brave-browser.list',
                    'sudo apt update && sudo apt install -y brave-browser'
                ],
                'dnf_cmds': [
                    'sudo dnf install -y dnf-plugins-core',
                    'sudo dnf config-manager --add-repo https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo',
                    'sudo dnf install -y brave-browser'
                ],
                'pacman_cmds': [
                    'yay -S --noconfirm brave-bin'
                ]
            }
        },
        'Google Chrome': {
            'winget': 'Google.Chrome',
            'linux': {
                'method': 'deb',
                'deb_url': 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb',
                'dnf_cmds': [
                    'sudo dnf install -y https://dl.google.com/linux/direct/google-chrome-stable_current_x86_64.rpm'
                ],
                'pacman_cmds': [
                    'yay -S --noconfirm google-chrome'
                ]
            }
        },
        'Mozilla Firefox': {
            'winget': 'Mozilla.Firefox',
            'linux': {
                'method': 'apt',
                'apt_pkg': 'firefox',
                'dnf_pkg': 'firefox',
                'pacman_pkg': 'firefox'
            }
        },
        'Slack': {
            'winget': 'SlackTechnologies.Slack',
            'linux': {
                'method': 'deb',
                'deb_url': 'https://downloads.slack-edge.com/desktop-releases/linux/x64/4.41.105/slack-desktop-4.41.105-amd64.deb',
                'dnf_cmds': [
                    'sudo dnf install -y https://downloads.slack-edge.com/desktop-releases/linux/x64/4.41.105/slack-4.41.105-0.1.el8.x86_64.rpm'
                ],
                'pacman_cmds': [
                    'yay -S --noconfirm slack-desktop'
                ]
            }
        },
        'Telegram': {
            'winget': 'Telegram.TelegramDesktop',
            'linux': {
                'method': 'apt',
                'apt_pkg': 'telegram-desktop',
                'dnf_pkg': 'telegram-desktop',
                'pacman_pkg': 'telegram-desktop'
            }
        },
        'Zoom': {
            'winget': 'Zoom.Zoom',
            'linux': {
                'method': 'deb',
                'deb_url': 'https://zoom.us/client/latest/zoom_amd64.deb',
                'dnf_cmds': [
                    'sudo dnf install -y https://zoom.us/client/latest/zoom_x86_64.rpm'
                ],
                'pacman_cmds': [
                    'yay -S --noconfirm zoom'
                ]
            }
        },
        'VLC Media Player': {
            'winget': 'VideoLAN.VLC',
            'linux': {
                'method': 'apt',
                'apt_pkg': 'vlc',
                'dnf_pkg': 'vlc',
                'pacman_pkg': 'vlc'
            }
        },
        'Visual Studio Code': {
            'winget': 'Microsoft.VisualStudioCode',
            'linux': {
                'method': 'repo',
                'repo_cmds': [
                    'sudo apt install -y wget gpg',
                    'wget -qO- https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /tmp/packages.microsoft.gpg',
                    'sudo install -D -o root -g root -m 644 /tmp/packages.microsoft.gpg /etc/apt/keyrings/packages.microsoft.gpg',
                    'echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list',
                    'sudo apt update && sudo apt install -y code'
                ],
                'dnf_cmds': [
                    'sudo rpm --import https://packages.microsoft.com/keys/microsoft.asc',
                    'echo -e "[code]\nname=Visual Studio Code\nbaseurl=https://packages.microsoft.com/yumrepos/vscode\nenabled=1\ngpgcheck=1\ngpgkey=https://packages.microsoft.com/keys/microsoft.asc" | sudo tee /etc/yum.repos.d/vscode.repo',
                    'sudo dnf install -y code'
                ],
                'pacman_cmds': [
                    'yay -S --noconfirm visual-studio-code-bin'
                ]
            }
        },
        'Python': {
            'winget': 'Python.Python.3.12',
            'linux': {
                'method': 'apt',
                'apt_pkg': 'python3',
                'dnf_pkg': 'python3',
                'pacman_pkg': 'python'
            }
        },
    },
    'windows_only': {
        'Lightshot': 'Skillbrains.Lightshot',
        'Google Drive': 'Google.GoogleDrive',
        'Notepad++': 'Notepad++.Notepad++'
    }
}

# Categories for README organization
CATEGORIES = {
    'Browsers': ['Brave Browser', 'Google Chrome', 'Mozilla Firefox'],
    'Communication': ['Slack', 'Telegram', 'Zoom'],
    'Media & Utilities': ['VLC Media Player', 'Lightshot', 'Google Drive'],
    'Development': ['Python', 'Visual Studio Code', 'Notepad++']
}
