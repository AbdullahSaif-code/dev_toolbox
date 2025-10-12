import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_vscode():
    try:
        if sys.platform != 'linux':
            return "VSCode installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/code'):
            return "Visual Studio Code is already installed."
        
        # Install via snap
        subprocess.run(['sudo', 'snap', 'install', 'code', '--classic'], check=True, capture_output=True)
        
        return "Visual Studio Code installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing VSCode: {e}")
        return f"Error installing Visual Studio Code: {e.stderr.decode()}"
