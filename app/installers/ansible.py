import shutil
import subprocess
from ..utils.logging import get_logger

logger = get_logger(__name__)


def install_ansible():
    try:
        if shutil.which("ansible"):
            return "Ansible is already installed."
        # Install via apt from Ubuntu/Debian repos
        subprocess.run(["sudo", "apt", "update"], check=True, capture_output=True)
        subprocess.run(["sudo", "apt", "install", "-y", "ansible"], check=True, capture_output=True)
        return "Ansible installed successfully."
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Ansible install error: {stderr}")
        return f"Error installing Ansible: {stderr}"
    except Exception as e:
        logger.error(f"Ansible installation failed: {e}")
        return f"Error installing Ansible: {str(e)}"

def uninstall_ansible():
    try:
        if not shutil.which("ansible"):
            return "Ansible is not installed."
        subprocess.run(["sudo", "apt", "remove", "-y", "ansible"], check=True, capture_output=True)
        return "Ansible uninstalled successfully."
    except subprocess.CalledProcessError as e:
        stderr = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Ansible uninstall error: {stderr}")
        return f"Error uninstalling Ansible: {stderr}"
    except Exception as e:
        logger.error(f"Ansible uninstallation failed: {e}")
        return f"Error uninstalling Ansible: {str(e)}"
