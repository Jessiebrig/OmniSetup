#!/usr/bin/env python3
"""
README Generator - Updates the Applications Installed section
Run this after modifying apps_config.py
"""

import re
from apps_config import CATEGORIES, WINDOWS_ONLY, LINUX_ONLY

def generate_apps_section():
    """Generate the Applications Installed section"""
    lines = ["### Applications Installed\n"]
    
    for category, apps in CATEGORIES.items():
        lines.append(f"\n**{category}:**")
        for app in apps:
            suffix = ""
            if app in WINDOWS_ONLY:
                suffix = " (Windows only)"
            elif app in LINUX_ONLY:
                suffix = " (Linux only)"
            lines.append(f"- {app}{suffix}")
    
    return "\n".join(lines)

def update_readme():
    """Update README.md with generated apps section"""
    readme_path = "README.md"
    
    # Read current README
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Generate new apps section
    new_section = generate_apps_section()
    
    # Replace the section between "### Applications Installed" and "## One-Line Installation"
    pattern = r'(### Applications Installed\n).*?(\n## One-Line Installation)'
    replacement = r'\1' + new_section + r'\2'
    
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Write back
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print("[OK] README.md updated successfully!")
    print("\nGenerated section:")
    print(new_section)

if __name__ == "__main__":
    update_readme()
