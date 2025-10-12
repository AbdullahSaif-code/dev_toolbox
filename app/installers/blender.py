import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_blender():
    try:
        if sys.platform != 'linux':
            return "Blender installation is only supported on Linux."
        # Prefer snap for simplicity
        subprocess.run(['sudo', 'snap', 'install', 'blender', '--classic'], check=True, capture_output=True)
        return "Blender installed successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Blender: {e}")
        return f"Error installing Blender: {e.stderr.decode() if e.stderr else str(e)}"


def uninstall_blender():
    try:
        if sys.platform != 'linux':
            return "Blender uninstallation is only supported on Linux."
        subprocess.run(['sudo', 'snap', 'remove', 'blender'], check=True, capture_output=True)
        return "Blender uninstalled successfully."
    except subprocess.CalledProcessError as e:
        logger.error(f"Error uninstalling Blender: {e}")
        return f"Error uninstalling Blender: {e.stderr.decode() if e.stderr else str(e)}"
