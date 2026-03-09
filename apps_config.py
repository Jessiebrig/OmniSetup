"""
OmniSetup Application Configuration
Single source of truth for all applications and categories
"""

# Application packages for each platform
APPS = {
    'windows': {
        'Brave Browser': 'Brave.Brave',
        'Google Chrome': 'Google.Chrome',
        'Mozilla Firefox': 'Mozilla.Firefox',
        'Slack': 'SlackTechnologies.Slack',
        'Telegram': 'Telegram.TelegramDesktop',
        'Zoom': 'Zoom.Zoom',
        'VLC Media Player': 'VideoLAN.VLC',
        'Lightshot': 'Skillbrains.Lightshot',
        'Google Drive': 'Google.GoogleDrive',
        'Python': 'Python.Python.3.12',
        'Visual Studio Code': 'Microsoft.VisualStudioCode',
        'Notepad++': 'Notepad++.Notepad++'
    },
    'linux': {
        'Brave Browser': 'brave-browser',
        'Google Chrome': 'google-chrome-stable',
        'Mozilla Firefox': 'firefox',
        'Slack': 'slack',
        'Telegram': 'telegram-desktop',
        'Zoom': 'zoom',
        'VLC Media Player': 'vlc',
        'Python': 'python3',
        'Visual Studio Code': 'code'
    }
}

# Categories for README organization
CATEGORIES = {
    'Browsers': [
        'Brave Browser',
        'Google Chrome',
        'Mozilla Firefox'
    ],
    'Communication': [
        'Slack',
        'Telegram',
        'Zoom'
    ],
    'Media & Utilities': [
        'VLC Media Player',
        'Lightshot',
        'Google Drive'
    ],
    'Development': [
        'Python',
        'Visual Studio Code',
        'Notepad++'
    ]
}

# Platform-specific apps (for marking in README)
WINDOWS_ONLY = ['Lightshot', 'Google Drive', 'Notepad++']
LINUX_ONLY = []
