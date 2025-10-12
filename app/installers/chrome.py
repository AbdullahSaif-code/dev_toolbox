import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_chrome():
    try:
        if sys.platform != 'linux':
            return "Chrome installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/google-chrome'):
            return "Google Chrome is already installed."
        
        # Update package index
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        
        # Install dependencies
        subprocess.run(['sudo', 'apt', 'install', '-y', 'wget', 'gnupg'], check=True, capture_output=True)
        
        # Add Google Chrome repository
        subprocess.run(['wget', '-q', '-O', '-', 'https://dl.google.com/linux/linux_signing_key.pub', '|', 'sudo', 'apt-key', 'add', '-'], shell=True, check=True, capture_output=True)
        subprocess.run(['sudo', 'sh', '-c', 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'], shell=True, check=True, capture_output=True)
        
        # Update and install
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'google-chrome-stable'], check=True, capture_output=True)
        
        return "Google Chrome installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Chrome: {e}")
        return f"Error installing Google Chrome: {e.stderr.decode()}"
