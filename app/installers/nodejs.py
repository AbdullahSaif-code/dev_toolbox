import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_nodejs():
    try:
        if sys.platform != 'linux':
            return "Node.js installation is only supported on Linux."
        subprocess.run(["sudo", "/usr/bin/apt", "update"], check=True, capture_output=True)
        subprocess.run(["sudo", "/usr/bin/apt", "install", "-y", "nodejs", "npm"], check=True, capture_output=True)
        return "Node.js and npm installed successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Node.js: {err}")
        return f"Error installing Node.js: {err}"


def uninstall_nodejs():
    try:
        if sys.platform != 'linux':
            return "Node.js uninstallation is only supported on Linux."
        subprocess.run(["sudo", "/usr/bin/apt", "remove", "-y", "nodejs", "npm"], check=True, capture_output=True)
        return "Node.js and npm uninstalled successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error uninstalling Node.js: {err}")
        return f"Error uninstalling Node.js: {err}"
