import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_androidstudio():
    try:
        if sys.platform != 'linux':
            return "Android Studio installation is only supported on Linux."
        
        if os.path.exists('/opt/android-studio/bin/studio.sh'):
            return "Android Studio is already installed."
        
        # Install dependencies
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'openjdk-11-jdk', 'lib32z1'], 
                      check=True, capture_output=True)
        
        # Install Android Studio via snap (easiest method)
        subprocess.run(['sudo', 'snap', 'install', 'android-studio', '--classic'], 
                      check=True, capture_output=True)
        
        return "Android Studio installed successfully!"
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Android Studio: {err}")
        return f"Error installing Android Studio: {err}"
    except Exception as e:
        logger.error(f"Android Studio installation failed: {e}")
        return f"Error installing Android Studio: {str(e)}"

def uninstall_androidstudio():
    try:
        if sys.platform != 'linux':
            return "Android Studio uninstallation is only supported on Linux."
        
        subprocess.run(['sudo', 'snap', 'remove', 'android-studio'], 
                      check=True, capture_output=True)
        
        return "Android Studio uninstalled successfully."
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error uninstalling Android Studio: {err}")
        return f"Error uninstalling Android Studio: {err}"
    except Exception as e:
        logger.error(f"Android Studio uninstall failed: {e}")
        return f"Error uninstalling Android Studio: {str(e)}"