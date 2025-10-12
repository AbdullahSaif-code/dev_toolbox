import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_mysqlworkbench():
    try:
        if sys.platform != 'linux':
            return "MySQL Workbench installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/mysql-workbench'):
            return "MySQL Workbench is already installed."
        
        # Install via apt
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'mysql-workbench'], check=True, capture_output=True)
        
        return "MySQL Workbench installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing MySQL Workbench: {e}")
        return f"Error installing MySQL Workbench: {e.stderr.decode()}"
