#!/usr/bin/env python3
"""
README Generator - Updates the Applications Installed section
Run this after modifying apps_config.py
"""

import re
from apps_config import APPS, CATEGORIES

WINDOWS_ONLY = set(APPS['windows_only'].keys())

def generate_apps_section():
    lines = ["### Applications Installed\n"]
    for category, apps in CATEGORIES.items():
        lines.append(f"\n**{category}:**")
        for app in apps:
            suffix = " (Windows only)" if app in WINDOWS_ONLY else ""
            lines.append(f"- {app}{suffix}")
    return "\n".join(lines)

def update_readme():
    readme_path = "README.md"
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()

    new_section = generate_apps_section()
    pattern = r'(### Applications Installed\n).*?(\n## One-Line Installation)'
    replacement = r'\1' + new_section + r'\2'
    updated_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(updated_content)

    print("[OK] README.md updated successfully!")
    print("\nGenerated section:")
    print(new_section)

if __name__ == "__main__":
    update_readme()
