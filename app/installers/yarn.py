import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_yarn():
    try:
        if sys.platform != 'linux':
            return "Yarn installation is only supported on Linux."
        # Prefer installing via npm globally; requires elevation for system prefix
        subprocess.run(["sudo", "/usr/bin/apt", "update"], check=True, capture_output=True)
        # Ensure npm exists (from nodejs package); user should install nodejs first
        subprocess.run(["sudo", "/usr/bin/npm", "install", "-g", "yarn"], check=True, capture_output=True)
        return "Yarn installed successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Yarn: {err}")
        return f"Error installing Yarn: {err}"


def uninstall_yarn():
    try:
        if sys.platform != 'linux':
            return "Yarn uninstallation is only supported on Linux."
        subprocess.run(["sudo", "/usr/bin/npm", "uninstall", "-g", "yarn"], check=True, capture_output=True)
        return "Yarn uninstalled successfully."
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error uninstalling Yarn: {err}")
        return f"Error uninstalling Yarn: {err}"
