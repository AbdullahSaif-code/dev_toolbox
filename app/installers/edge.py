import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_edge():
    try:
        if sys.platform != 'linux':
            return "Edge installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/microsoft-edge'):
            return "Microsoft Edge is already installed."
        
        # Install using official script
        subprocess.run(['curl', 'https://packages.microsoft.com/keys/microsoft.asc', '|', 'gpg', '--dearmor', '>', 'microsoft.gpg'], shell=True, check=True, capture_output=True)
        subprocess.run(['sudo', 'install', '-o', 'root', '-g', 'root', '-m', '644', 'microsoft.gpg', '/etc/apt/trusted.gpg.d/'], shell=True, check=True, capture_output=True)
        subprocess.run(['sudo', 'sh', '-c', 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge-dev.list'], shell=True, check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'microsoft-edge-stable'], check=True, capture_output=True)
        
        return "Microsoft Edge installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Edge: {e}")
        return f"Error installing Microsoft Edge: {e.stderr.decode()}"

def uninstall_edge():
    try:
        if sys.platform != 'linux':
            return "Edge uninstallation is only supported on Linux."

        subprocess.run(['sudo', 'apt', 'remove', '-y', 'microsoft-edge-stable'], check=True, capture_output=True)

        list_file = '/etc/apt/sources.list.d/microsoft-edge-dev.list'
        if os.path.exists(list_file):
            subprocess.run(['sudo', 'rm', '-f', list_file], check=True, capture_output=True)
        gpg = '/etc/apt/trusted.gpg.d/microsoft.gpg'
        if os.path.exists(gpg):
            subprocess.run(['sudo', 'rm', '-f', gpg], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)

        return "Microsoft Edge uninstalled successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error uninstalling Edge: {e}")
        return f"Error uninstalling Microsoft Edge: {e.stderr.decode()}"
