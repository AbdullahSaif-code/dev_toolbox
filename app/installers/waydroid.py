import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_waydroid():
    """Install Waydroid - lightweight Android container for Linux"""
    try:
        if sys.platform != 'linux':
            return "Waydroid is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/waydroid'):
            return "Waydroid is already installed."
        
        # Install dependencies
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'python3-gbulb', 'libglib2.0-0'], 
                      check=True, capture_output=True)
        
        # Add Waydroid repository (Debian/Ubuntu)
        subprocess.run(['sudo', 'curl', '-fsSL', 'https://repo.waydro.id/KEY.gpg', '|', 
                       'sudo', 'gpg', '--dearmor', '-o', '/usr/share/keyrings/waydroid.gpg'], 
                      shell=True, check=True, capture_output=True)
        
        subprocess.run(['sudo', 'curl', '-fsSL', '-o', '/etc/apt/sources.list.d/waydroid.sources',
                       'https://repo.waydro.id/waydroid.sources'],
                      shell=True, check=True, capture_output=True)
        
        # Install Waydroid
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'waydroid'], check=True, capture_output=True)
        
        # Initialize Waydroid
        subprocess.run(['sudo', 'waydroid', 'init', '-s', 'GAPPS'], 
                      check=False, capture_output=True, timeout=300)
        
        logger.info("Waydroid installed successfully")
        return "Waydroid installed successfully! Run 'sudo waydroid session start' to launch Android. Then use 'waydroid app install <apk>' to install apps."
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Waydroid: {err}")
        return f"Error installing Waydroid: {err}"
    except Exception as e:
        logger.error(f"Waydroid installation failed: {e}")
        return f"Error installing Waydroid: {str(e)}"

def uninstall_waydroid():
    """Uninstall Waydroid"""
    try:
        if sys.platform != 'linux':
            return "Waydroid uninstallation is only supported on Linux."
        
        # Stop Waydroid session if running
        subprocess.run(['sudo', 'waydroid', 'session', 'stop'], 
                      check=False, capture_output=True, timeout=30)
        
        # Remove package
        subprocess.run(['sudo', 'apt', 'remove', '-y', 'waydroid'], 
                      check=True, capture_output=True)
        
        # Clean up repository
        subprocess.run(['sudo', 'rm', '-f', '/etc/apt/sources.list.d/waydroid.sources',
                       '/usr/share/keyrings/waydroid.gpg'],
                      check=False, capture_output=True)
        
        subprocess.run(['sudo', 'apt', 'update'], check=False, capture_output=True)
        
        logger.info("Waydroid uninstalled")
        return "Waydroid uninstalled successfully."
        
    except Exception as e:
        logger.error(f"Waydroid uninstall failed: {e}")
        return f"Error uninstalling Waydroid: {str(e)}"