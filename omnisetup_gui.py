#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import platform
import threading
import sys
import os

# Import from main script
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from omnisetup import (
    install_windows_debloat, 
    install_windows_runtimes, 
    install_linux_de,
    run_command,
    get_app_list,
    logging
)

class OmniSetupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OmniSetup - Universal Setup Tool")
        self.root.geometry("700x600")
        
        self.system = platform.system()
        
        # Get shared app list
        self.apps = get_app_list()
        
        self.checkboxes = {}
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = tk.Label(
            self.root, 
            text=f"OmniSetup - {self.system}", 
            font=("Arial", 16, "bold"),
            pady=10
        )
        header.pack()
        
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Platform-specific options
        if self.system == "Windows":
            self.setup_windows_options(main_frame)
        elif self.system == "Linux":
            self.setup_linux_options(main_frame)
        
        # Applications section
        self.setup_apps_section(main_frame)
        
        # Log output
        log_label = tk.Label(main_frame, text="Output Log:", font=("Arial", 10, "bold"))
        log_label.pack(anchor=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(main_frame, height=8, state='disabled')
        self.log_text.pack(fill=tk.BOTH, expand=True)
        
        # Buttons
        button_frame = ttk.Frame(self.root, padding="10")
        button_frame.pack(fill=tk.X)
        
        install_btn = ttk.Button(
            button_frame, 
            text="Install Selected", 
            command=self.install_selected
        )
        install_btn.pack(side=tk.LEFT, padx=5)
        
        select_all_btn = ttk.Button(
            button_frame, 
            text="Select All Apps", 
            command=self.select_all_apps
        )
        select_all_btn.pack(side=tk.LEFT, padx=5)
        
        deselect_all_btn = ttk.Button(
            button_frame, 
            text="Deselect All Apps", 
            command=self.deselect_all_apps
        )
        deselect_all_btn.pack(side=tk.LEFT, padx=5)
    
    def setup_windows_options(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Windows Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.win_vcpp = tk.BooleanVar()
        ttk.Checkbutton(
            options_frame, 
            text="Install Visual C++ & .NET Framework", 
            variable=self.win_vcpp
        ).pack(anchor=tk.W)
        
        self.win_debloat = tk.BooleanVar()
        debloat_cb = ttk.Checkbutton(
            options_frame, 
            text="Debloat Windows (Chris Titus Tech)", 
            variable=self.win_debloat
        )
        debloat_cb.pack(anchor=tk.W)
    
    def setup_linux_options(self, parent):
        options_frame = ttk.LabelFrame(parent, text="Linux Options", padding="10")
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.linux_de = tk.StringVar(value="none")
        
        ttk.Radiobutton(
            options_frame, 
            text="No Desktop Environment", 
            variable=self.linux_de, 
            value="none"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            options_frame, 
            text="Install KDE Plasma", 
            variable=self.linux_de, 
            value="kde"
        ).pack(anchor=tk.W)
        
        ttk.Radiobutton(
            options_frame, 
            text="Install XFCE", 
            variable=self.linux_de, 
            value="xfce"
        ).pack(anchor=tk.W)
    
    def setup_apps_section(self, parent):
        apps_frame = ttk.LabelFrame(parent, text="Applications", padding="10")
        apps_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Scrollable canvas for checkboxes
        canvas = tk.Canvas(apps_frame, height=200)
        scrollbar = ttk.Scrollbar(apps_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Get apps for current platform
        current_apps = self.apps.get('windows' if self.system == 'Windows' else 'linux', {})
        
        # Create checkboxes
        for app_name in current_apps.keys():
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(scrollable_frame, text=app_name, variable=var)
            cb.pack(anchor=tk.W, pady=2)
            self.checkboxes[app_name] = var
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
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
        # Run in thread to prevent GUI freeze
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
            
            if self.win_debloat.get():
                self.log("Running Windows debloat tool...")
                install_windows_debloat()
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
    
    def _install_apps(self, selected_apps):
        current_apps = self.apps.get('windows' if self.system == 'Windows' else 'linux', {})
        
        if self.system == "Windows":
            for app_name in selected_apps:
                pkg = current_apps.get(app_name)
                if pkg:
                    self.log(f"Installing {app_name}...")
                    run_command(f'winget install --id {pkg} --silent --accept-package-agreements --accept-source-agreements')
        else:
            try:
                distro = platform.freedesktop_os_release().get('ID', '').lower()
            except:
                distro = ''
            
            if 'ubuntu' in distro or 'debian' in distro:
                run_command("sudo apt update")
                for app_name in selected_apps:
                    pkg = current_apps.get(app_name)
                    if pkg:
                        self.log(f"Installing {app_name}...")
                        run_command(f"sudo apt install -y {pkg}")
            elif 'fedora' in distro:
                for app_name in selected_apps:
                    pkg = current_apps.get(app_name)
                    if pkg:
                        self.log(f"Installing {app_name}...")
                        run_command(f"sudo dnf install -y {pkg}")
            elif 'arch' in distro:
                for app_name in selected_apps:
                    pkg = current_apps.get(app_name)
                    if pkg:
                        self.log(f"Installing {app_name}...")
                        run_command(f"sudo pacman -S --noconfirm {pkg}")

def main():
    root = tk.Tk()
    app = OmniSetupGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
