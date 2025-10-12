import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_drawio():
    try:
        if sys.platform != 'linux':
            return "Draw.io installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/drawio'):
            return "Draw.io is already installed."
        
        # Install via snap
        subprocess.run(['sudo', 'snap', 'install', 'drawio'], check=True, capture_output=True)
        
        return "Draw.io installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Draw.io: {e}")
        return f"Error installing Draw.io: {e.stderr.decode()}"

def uninstall_drawio():
    try:
        if sys.platform != 'linux':
            return "Draw.io uninstallation is only supported on Linux."
        subprocess.run(['sudo', 'snap', 'remove', 'drawio'], check=True, capture_output=True)
        return "Draw.io uninstalled successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error uninstalling Draw.io: {e}")
        return f"Error uninstalling Draw.io: {e.stderr.decode()}"
