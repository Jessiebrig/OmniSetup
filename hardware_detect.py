"""
Hardware Detection Module
Detects CPU vendor (Intel/AMD) and NVIDIA GPU presence
"""

import subprocess
import platform

def detect_cpu_vendor():
    """
    Detect CPU vendor (Intel or AMD)
    Returns: 'intel', 'amd', or 'unknown'
    """
    if platform.system() != "Linux":
        return 'unknown'
    
    try:
        result = subprocess.run(
            ['cat', '/proc/cpuinfo'],
            capture_output=True,
            text=True,
            check=True
        )
        
        output = result.stdout.lower()
        
        if 'genuineintel' in output or 'intel' in output:
            return 'intel'
        elif 'authenticamd' in output or 'amd' in output:
            return 'amd'
        else:
            return 'unknown'
    except:
        return 'unknown'

def detect_nvidia_gpu():
    """
    Detect if NVIDIA GPU is present
    Returns: True if NVIDIA detected, False otherwise
    """
    if platform.system() != "Linux":
        return False
    
    try:
        result = subprocess.run(
            ['lspci'],
            capture_output=True,
            text=True,
            check=True
        )
        
        return 'nvidia' in result.stdout.lower()
    except:
        return False

def get_hardware_info():
    """
    Get complete hardware information
    Returns: dict with cpu_vendor and has_nvidia
    """
    return {
        'cpu_vendor': detect_cpu_vendor(),
        'has_nvidia': detect_nvidia_gpu()
    }
