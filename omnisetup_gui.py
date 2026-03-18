#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import platform
import threading
import sys
import os
import subprocess
import shutil

# Theme colors
BG_COLOR = "#1a1a2e"
FG_COLOR = "#e0e0e0"
ACCENT_COLOR = "#4a9eff"
FRAME_BG = "#16213e"

# Import from main script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omnisetup import (
    install_windows_debloat, 
    install_windows_runtimes, 
    install_linux_de,
    install_power_management,
    run_command,
    install_linux_app,
    get_app_list,
    get_hardware_info,
    logging
)

def check_git_installed():
    """Check if Git is installed"""
    try:
        subprocess.run(['git', '--version'], capture_output=True, check=True)
        return True
    except:
        return False

def install_git_windows():
    """Install Git on Windows using winget"""
    print("Git not found. Installing Git...")
    try:
        subprocess.run(
            'winget install --id Git.Git --silent --accept-package-agreements --accept-source-agreements',
            shell=True,
            check=True
        )
        print("Git installed successfully.")
        return True
    except:
        print("Failed to install Git. Please install manually from https://git-scm.com/")
        return False

class OmniSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniSetup - Universal Setup Tool")
        self.root.minsize(400, 500)
        
        self.system = platform.system()
        
        # Get shared app list
        self.apps = get_app_list()
        
        # Get hardware info for Linux
        if self.system == "Linux":
            self.hw_info = get_hardware_info()
        else:
            self.hw_info = None
        
        self.checkboxes = {}
        self.setup_ui()
    
    def setup_ui(self):
        # Buttons pinned at bottom first so they're always visible
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        ttk.Button(button_frame, text="Install Selected", command=self.install_selected).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Select All Apps", command=self.select_all_apps).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Deselect All Apps", command=self.deselect_all_apps).pack(side=tk.LEFT, padx=5)

        # Header row with title centered + toggle button at right
        header_frame = tk.Frame(self.root)
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        self.dark_mode = tk.BooleanVar(value=False)
        self.theme_btn = tk.Button(header_frame, text="☀ Light Mode", command=self.toggle_theme,
            bg="#4a9eff", fg="white", relief=tk.FLAT, padx=8, cursor="hand2")
        self.theme_btn.pack(side=tk.RIGHT)

        tk.Label(header_frame, text=f"OmniSetup - {self.system}", font=("Arial", 16, "bold")).pack(expand=True)

        # Scrollable main area
        container = ttk.Frame(self.root)
        container.pack(fill=tk.BOTH, expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        main_frame = ttk.Frame(canvas, padding="10")

        main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=main_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(canvas.find_all()[0], width=e.width))

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Platform-specific options
        if self.system == "Windows":
            self.setup_windows_options(main_frame)
        elif self.system == "Linux":
            self.setup_linux_options(main_frame)

        # Applications section
        self.setup_apps_section(main_frame)

        # Log output
        tk.Label(main_frame, text="Output Log:", font=("Arial", 10, "bold")).pack(anchor=tk.W, pady=(10, 5))
        self.log_text = scrolledtext.ScrolledText(main_frame, height=8, state='disabled', bg="#000000", fg="#00ff00", insertbackground="#00ff00", font=("Courier", 9))
        self.log_text.pack(fill=tk.BOTH, expand=True)
    
    def setup_windows_options(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Windows Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.win_vcpp = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, 
            text="Install Visual C++ & .NET Framework", 
            variable=self.win_vcpp
        ).pack(anchor=tk.W)
        
        # Debloat options (radio buttons)
        ttk.Label(options_frame, text="\nWindows Debloat:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        self.win_debloat = tk.StringVar(value="none")
        
        ttk.Radiobutton(
            options_frame,
            text="None",
            variable=self.win_debloat,
            value="none"
        ).pack(anchor=tk.W, padx=(20, 0))
        
        ttk.Radiobutton(
            options_frame,
            text="Chris Titus Tech Debloat",
            variable=self.win_debloat,
            value="christitus"
        ).pack(anchor=tk.W, padx=(20, 0))
        
        ttk.Radiobutton(
            options_frame,
            text="Windows10Debloater",
            variable=self.win_debloat,
            value="windows10debloater"
        ).pack(anchor=tk.W, padx=(20, 0))
    
    def setup_linux_options(self, parent):
        # Desktop Environment
        de_frame = ttk.LabelFrame(parent, text="Desktop Environment", padding="10")
        de_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.linux_de = tk.StringVar(value="none")
        
        ttk.Radiobutton(
            de_frame, 
            text="Install KDE Plasma", 
            variable=self.linux_de, 
            value="kde"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            de_frame, 
            text="Install XFCE", 
            variable=self.linux_de, 
            value="xfce"
        ).pack(anchor=tk.W)
        
        # Power Management
        power_frame = ttk.LabelFrame(parent, text="Power Management", padding="10")
        power_frame.pack(fill=tk.X, pady=(0, 10))
        
        cpu_vendor = self.hw_info['cpu_vendor']
        has_nvidia = self.hw_info['has_nvidia']
        
        # Show detected hardware
        hw_label = f"Detected: {cpu_vendor.upper()} CPU"
        if has_nvidia:
            hw_label += " + NVIDIA GPU"
        ttk.Label(power_frame, text=hw_label, font=("Arial", 9, "italic")).pack(anchor=tk.W, pady=(0, 5))
        
        # Basic power management (radio buttons - mutually exclusive)
        ttk.Label(power_frame, text="\nBase Power Management:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        self.power_base = tk.StringVar(value="none")
        
        ttk.Radiobutton(
            power_frame,
            text="None",
            variable=self.power_base,
            value="none"
        ).pack(anchor=tk.W, padx=(20, 0))
        
        ttk.Radiobutton(
            power_frame,
            text="auto-cpufreq (Automatic CPU optimization)",
            variable=self.power_base,
            value="auto-cpufreq"
        ).pack(anchor=tk.W, padx=(20, 0))
        
        ttk.Radiobutton(
            power_frame,
            text="TLP (Comprehensive power management)",
            variable=self.power_base,
            value="tlp"
        ).pack(anchor=tk.W, padx=(20, 0))
        
        self.power_tools = {}
        
        # CPU-specific (checkboxes)
        if cpu_vendor == 'intel' or cpu_vendor == 'amd':
            ttk.Label(power_frame, text="\nAdditional Tools:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        if cpu_vendor == 'intel':
            self.power_tools['thermald'] = tk.BooleanVar()
            ttk.Checkbutton(
                power_frame,
                text="thermald (Intel thermal management)",
                variable=self.power_tools['thermald']
            ).pack(anchor=tk.W, padx=(20, 0))
        elif cpu_vendor == 'amd':
            self.power_tools['ryzenadj'] = tk.BooleanVar()
            ttk.Checkbutton(
                power_frame,
                text="ryzenadj (AMD Ryzen tuning)",
                variable=self.power_tools['ryzenadj']
            ).pack(anchor=tk.W, padx=(20, 0))
        
        # NVIDIA tools (checkboxes)
        if has_nvidia:
            if cpu_vendor not in ['intel', 'amd']:
                ttk.Label(power_frame, text="\nAdditional Tools:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
            
            self.power_tools['envycontrol'] = tk.BooleanVar()
            ttk.Checkbutton(
                power_frame,
                text="envycontrol (NVIDIA GPU switching)",
                variable=self.power_tools['envycontrol']
            ).pack(anchor=tk.W, padx=(20, 0))
            
            self.power_tools['optimus-manager'] = tk.BooleanVar()
            ttk.Checkbutton(
                power_frame,
                text="optimus-manager (Advanced NVIDIA switching)",
                variable=self.power_tools['optimus-manager']
            ).pack(anchor=tk.W, padx=(20, 0))
    
    def setup_apps_section(self, parent):
        apps_frame = ttk.LabelFrame(parent, text="Applications", padding="10")
        apps_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(apps_frame, text="Cross-Platform", font=("Arial", 9, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 2))
        for col in range(3):
            apps_frame.columnconfigure(col, weight=1)

        for i, app_name in enumerate(self.apps['cross_platform'].keys()):
            var = tk.BooleanVar()
            ttk.Checkbutton(apps_frame, text=app_name, variable=var).grid(row=i//3+1, column=i%3, sticky=tk.W, pady=2)
            self.checkboxes[app_name] = var

        if self.system == "Windows":
            offset = len(self.apps['cross_platform'])
            row_offset = offset//3 + 2
            ttk.Label(apps_frame, text="Windows Only", font=("Arial", 9, "bold")).grid(row=row_offset, column=0, columnspan=3, sticky=tk.W, pady=(10, 2))
            for i, app_name in enumerate(self.apps['windows_only'].keys()):
                var = tk.BooleanVar()
                ttk.Checkbutton(apps_frame, text=app_name, variable=var).grid(row=row_offset+1+i//3, column=i%3, sticky=tk.W, pady=2)
                self.checkboxes[app_name] = var
    
    def toggle_theme(self):
        self.dark_mode.set(not self.dark_mode.get())
        style = ttk.Style()
        if self.dark_mode.get():
            self.theme_btn.config(text="🌙 Dark Mode")
            self.root.configure(bg=BG_COLOR)
            style.theme_use('clam')
            style.configure('.', background=BG_COLOR, foreground=FG_COLOR, fieldbackground=FRAME_BG)
            style.configure('TFrame', background=BG_COLOR)
            style.configure('TLabelframe', background=BG_COLOR, foreground=ACCENT_COLOR)
            style.configure('TLabelframe.Label', background=BG_COLOR, foreground=ACCENT_COLOR)
            style.configure('TLabel', background=BG_COLOR, foreground=FG_COLOR)
            style.configure('TCheckbutton', background=BG_COLOR, foreground=FG_COLOR)
            style.configure('TRadiobutton', background=BG_COLOR, foreground=FG_COLOR)
            style.configure('TButton', background=ACCENT_COLOR, foreground='#ffffff')
            style.map('TButton', background=[('active', '#357abd')])
        else:
            self.theme_btn.config(text="☀ Light Mode")
            style.theme_use('default')

    def select_all_apps(self):
        for var in self.checkboxes.values():
            var.set(True)
    
    def deselect_all_apps(self):
        for var in self.checkboxes.values():
            var.set(False)
    
    def log(self, message):
        self.log_text.config(state='normal')
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state='disabled')
    
    def install_selected(self):
        if self.system == "Linux":
            self.log("Requesting sudo privileges...")
            result = subprocess.run("sudo -v", shell=True)
            if result.returncode != 0:
                messagebox.showerror("Error", "sudo authentication failed. Please run as a user with sudo privileges.")
                return
        thread = threading.Thread(target=self._install_thread)
        thread.daemon = True
        thread.start()
    
    def _install_thread(self):
        self.log("Starting installation...\n")
        
        # Windows-specific installations
        if self.system == "Windows":
            if self.win_vcpp.get():
                self.log("Installing Visual C++ & .NET Framework...")
                install_windows_runtimes()
                self.log("Done.\n")
            
            debloat_choice = self.win_debloat.get()
            if debloat_choice == "christitus":
                self.log("Running Chris Titus Tech Windows Utility...")
                run_command('powershell -Command "irm christitus.com/win | iex"')
                self.log("Done.\n")
            elif debloat_choice == "windows10debloater":
                self.log("Running Windows10Debloater...")
                run_command('powershell -Command "iwr -useb https://git.io/debloat|iex"')
                self.log("Done.\n")
        
        # Linux-specific installations
        elif self.system == "Linux":
            de_choice = self.linux_de.get()
            if de_choice != "none":
                self.log(f"Installing {de_choice.upper()} Desktop Environment...")
                if de_choice == "kde":
                    self._install_linux_de("1")
                elif de_choice == "xfce":
                    self._install_linux_de("2")
                self.log("Done.\n")
            
            # Install power management tools
            base_power = self.power_base.get()
            if base_power != "none":
                self.log(f"Installing {base_power}...")
                self._install_power_tool(base_power)
            
            selected_power_tools = [name for name, var in self.power_tools.items() if var.get()]
            if selected_power_tools:
                self.log(f"Installing {len(selected_power_tools)} additional power tools...")
                for tool in selected_power_tools:
                    self.log(f"Installing {tool}...")
                    self._install_power_tool(tool)
                self.log("Done.\n")
        
        # Install selected apps
        selected_apps = [name for name, var in self.checkboxes.items() if var.get()]
        
        if selected_apps:
            self.log(f"Installing {len(selected_apps)} applications...")
            self._install_apps(selected_apps)
            self.log("Done.\n")
        
        self.log("\nInstallation complete! Check omnisetup.log for details.")
        messagebox.showinfo("Complete", "Installation finished! Check the log for details.")
    
    def _install_linux_de(self, choice):
        try:
            distro = platform.freedesktop_os_release().get('ID', '').lower()
        except:
            distro = ''
        
        if 'ubuntu' in distro or 'debian' in distro:
            if choice == "1":
                run_command("sudo apt update && sudo apt install -y kde-plasma-desktop")
            elif choice == "2":
                run_command("sudo apt update && sudo apt install -y xfce4")
        elif 'fedora' in distro or 'rhel' in distro:
            if choice == "1":
                run_command("sudo dnf install -y @kde-desktop-environment")
            elif choice == "2":
                run_command("sudo dnf install -y @xfce-desktop-environment")
        elif 'arch' in distro:
            if choice == "1":
                run_command("sudo pacman -S --noconfirm plasma-meta")
            elif choice == "2":
                run_command("sudo pacman -S --noconfirm xfce4")
    
    def _create_desktop_shortcut(self, app_name):
        """Create a desktop shortcut for the installed app"""
        shortcuts = {
            'Brave Browser':      ('brave-browser',       'brave-browser',         'brave-browser'),
            'Google Chrome':      ('google-chrome',        'google-chrome-stable',  'google-chrome'),
            'Mozilla Firefox':    ('firefox',              'firefox',               'firefox'),
            'Slack':              ('slack',                'slack',                 'slack'),
            'Telegram':           ('telegram-desktop',     'telegram-desktop',      'telegram-desktop'),
            'Zoom':               ('zoom',                 'zoom',                  'zoom'),
            'VLC Media Player':   ('vlc',                  'vlc',                   'vlc'),
            'Visual Studio Code': ('code',                 'code',                  'code'),
            'Python':             ('python3',              'python3',               'python3'),
        }

        if self.system == "Windows":
            # winget creates shortcuts automatically, nothing to do
            return

        if app_name not in shortcuts:
            return

        exec_cmd, icon, wm_class = shortcuts[app_name]
        desktop = os.path.expanduser("~/Desktop")
        if not os.path.isdir(desktop):
            return

        shortcut_path = os.path.join(desktop, f"{app_name}.desktop")
        content = f"""[Desktop Entry]
Name={app_name}
Exec={exec_cmd}
Icon={icon}
Type=Application
Categories=Application;
StartupWMClass={wm_class}
"""
        try:
            with open(shortcut_path, 'w') as f:
                f.write(content)
            os.chmod(shortcut_path, 0o755)
            self.log(f"  ✓ Desktop shortcut created for {app_name}")
        except Exception as e:
            self.log(f"  ✗ Could not create shortcut for {app_name}: {e}")

    def _install_apps(self, selected_apps):
        try:
            distro = platform.freedesktop_os_release().get('ID', '').lower()
        except:
            distro = ''

        if self.system == "Windows":
            all_apps = {**self.apps['cross_platform'], **self.apps['windows_only']}
            for name in selected_apps:
                val = all_apps.get(name)
                pkg = val if isinstance(val, str) else val.get('winget') if val else None
                if pkg:
                    self.log(f"Installing {name}...")
                    run_command(f'winget install --id {pkg} --silent --accept-package-agreements --accept-source-agreements')
                    self._create_desktop_shortcut(name)
        else:
            if 'ubuntu' in distro or 'debian' in distro:
                run_command("sudo apt update")
            for name in selected_apps:
                app_config = self.apps['cross_platform'].get(name)
                if app_config:
                    self.log(f"Installing {name}...")
                    install_linux_app(name, app_config, distro)
                    self._create_desktop_shortcut(name)
    
    def _install_power_tool(self, tool):
        """Install power management tool"""
        try:
            distro = platform.freedesktop_os_release().get('ID', '').lower()
        except:
            distro = ''
        
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
                self.log("Note: ryzenadj requires manual installation from GitHub")
            elif tool == "envycontrol":
                run_command("sudo apt update && sudo apt install -y python3-pip")
                run_command("pip3 install envycontrol")
            elif tool == "optimus-manager":
                self.log("Note: optimus-manager is primarily for Arch-based distros")
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
                self.log("Note: ryzenadj requires manual installation from GitHub")
            elif tool == "envycontrol":
                run_command("pip3 install envycontrol")
            elif tool == "optimus-manager":
                self.log("Note: optimus-manager is primarily for Arch-based distros")
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

def main():
    # Check and install Git if needed (Windows only)
    if platform.system() == "Windows" and not check_git_installed():
        response = messagebox.askyesno(
            "Git Not Found",
            "Git is required for branch selection and updates.\n\nInstall Git now?"
        )
        if response:
            install_git_windows()
    
    root = tk.Tk()
    app = OmniSetupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
