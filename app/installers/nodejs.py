import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_nodejs():
    try:
        if sys.platform != 'linux':
            return "Node.js installation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "update"], check=True)
        subprocess.run(["pkexec", "/usr/bin/apt", "install", "-y", "nodejs", "npm"], check=True)
        return "Node.js and npm installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error installing Node.js: {str(e)}"


def uninstall_nodejs():
    try:
        if sys.platform != 'linux':
            return "Node.js uninstallation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "remove", "-y", "nodejs", "npm"], check=True)
        return "Node.js and npm uninstalled successfully."
    except subprocess.CalledProcessError as e:
        return f"Error uninstalling Node.js: {str(e)}"}
