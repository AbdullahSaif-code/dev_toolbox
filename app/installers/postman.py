import subprocess
import sys
import os
import tarfile
import urllib.request
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_postman():
    try:
        if sys.platform != 'linux':
            return "Postman installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/opt/Postman'):
            return "Postman is already installed."
        
        # Download and install
        url = 'https://dl.pstmn.io/download/latest/linux64'
        tar_path = '/tmp/postman.tar.gz'
        urllib.request.urlretrieve(url, tar_path)
        
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall('/opt')
        
        os.remove(tar_path)
        
        return "Postman installed successfully!"
    except Exception as e:
        logger.error(f"Error installing Postman: {e}")
        return f"Error installing Postman: {str(e)}"

def uninstall_postman():
    try:
        if sys.platform != 'linux':
            return "Postman uninstallation is only supported on Linux."
        if os.path.isdir('/opt/Postman'):
            subprocess.run(['sudo', 'rm', '-rf', '/opt/Postman'], check=True, capture_output=True)
        # Remove common desktop entry path if present
        desktop_entry = '/usr/share/applications/postman.desktop'
        if os.path.exists(desktop_entry):
            subprocess.run(['sudo', 'rm', '-f', desktop_entry], check=True, capture_output=True)
        return "Postman uninstalled successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error uninstalling Postman: {e}")
        return f"Error uninstalling Postman: {e.stderr.decode() if e.stderr else str(e)}"
