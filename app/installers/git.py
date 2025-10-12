import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_git():
    try:
        if sys.platform != 'linux':
            return "Git installation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "update"], check=True, capture_output=True)
        subprocess.run(["pkexec", "/usr/bin/apt", "install", "-y", "git"], check=True, capture_output=True)
        return "Git installed successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Git: {err}")
        return f"Error installing Git: {err}"


def uninstall_git():
    try:
        if sys.platform != 'linux':
            return "Git uninstallation is only supported on Linux."
        subprocess.run(["pkexec", "/usr/bin/apt", "remove", "-y", "git"], check=True, capture_output=True)
        return "Git uninstalled successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error uninstalling Git: {err}")
        return f"Error uninstalling Git: {err}"
