import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_dockerdesktop():
    try:
        if sys.platform != 'linux':
            return "Docker Desktop installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/docker-desktop'):
            return "Docker Desktop is already installed."
        
        # Install Docker first if not present
        if not os.path.exists('/usr/bin/docker'):
            subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'docker.io'], check=True, capture_output=True)
        
        # Download and install Docker Desktop
        subprocess.run(['wget', 'https://desktop.docker.com/linux/main/amd64/docker-desktop-amd64.deb'], check=True, capture_output=True)
        subprocess.run(['sudo', 'dpkg', '-i', 'docker-desktop-amd64.deb'], check=True, capture_output=True)
        subprocess.run(['rm', 'docker-desktop-amd64.deb'], check=True, capture_output=True)
        
        return "Docker Desktop installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Docker Desktop: {e}")
        return f"Error installing Docker Desktop: {e.stderr.decode()}"

def uninstall_dockerdesktop():
    try:
        if sys.platform != 'linux':
            return "Docker Desktop uninstallation is only supported on Linux."
        # Attempt to remove package installed via dpkg/apt
        subprocess.run(['sudo', 'apt', 'remove', '-y', 'docker-desktop'], check=False, capture_output=True)
        # Remove leftover desktop files
        paths = [
            '/usr/bin/docker-desktop',
            '/usr/share/applications/docker-desktop.desktop',
        ]
        for p in paths:
            if os.path.exists(p):
                subprocess.run(['sudo', 'rm', '-f', p], check=False, capture_output=True)
        return "Docker Desktop uninstalled successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error uninstalling Docker Desktop: {e}")
        return f"Error uninstalling Docker Desktop: {e.stderr.decode() if e.stderr else str(e)}"
