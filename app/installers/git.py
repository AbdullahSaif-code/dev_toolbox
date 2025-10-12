import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_git():
    try:
        if sys.platform != 'linux':
            return "Git installation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "update"], check=True)
        subprocess.run(["pkexec", "/usr/bin/apt", "install", "-y", "git"], check=True)
        return "Git installed successfully."
    except subprocess.CalledProcessError as e:
        return f"Error installing Git: {str(e)}"


def uninstall_git():
    try:
        if sys.platform != 'linux':
            return "Git uninstallation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "remove", "-y", "git"], check=True)
        return "Git uninstalled successfully."
    except subprocess.CalledProcessError as e:
        return f"Error uninstalling Git: {str(e)}"}
