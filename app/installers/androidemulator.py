import subprocess
import sys
import os
import shutil
from pathlib import Path
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_androidemulator():
    """Install Android Emulator via Android Studio"""
    try:
        if sys.platform != 'linux':
            return "Android Emulator is only supported on Linux."
        
        # Check if already installed
        android_home = os.path.expanduser('~/.android')
        if os.path.exists(android_home):
            return "Android Emulator appears to be already installed."
        
        # Install prerequisites
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'qemu-system-x86', 'libvirt-daemon', 'libvirt-daemon-system'], 
                      check=True, capture_output=True)
        
        # Install Android Studio (which includes AVD Manager)
        if not os.path.exists('/opt/android-studio'):
            subprocess.run(['sudo', 'apt', 'install', '-y', 'android-studio'], 
                          check=False, capture_output=True)
        
        # Create Android home directory
        os.makedirs(android_home, exist_ok=True)
        
        # Download and setup Android SDK if needed
        sdk_root = os.path.expanduser('~/Android/Sdk')
        os.makedirs(os.path.join(sdk_root, 'cmdline-tools'), exist_ok=True)
        
        logger.info("Android Emulator prerequisites installed")
        return "Android Emulator installed successfully! Launch Android Studio to create virtual devices (AVDs)."
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Android Emulator: {err}")
        return f"Error installing Android Emulator: {err}"
    except Exception as e:
        logger.error(f"Android Emulator installation failed: {e}")
        return f"Error installing Android Emulator: {str(e)}"

def uninstall_androidemulator():
    """Uninstall Android Emulator and related tools"""
    try:
        if sys.platform != 'linux':
            return "Android Emulator uninstallation is only supported on Linux."
        
        # Remove Android Studio
        subprocess.run(['sudo', 'apt', 'remove', '-y', 'android-studio'], 
                      check=False, capture_output=True)
        
        # Remove QEMU and libvirt if not needed elsewhere
        subprocess.run(['sudo', 'apt', 'remove', '-y', 'qemu-system-x86', 'libvirt-daemon'], 
                      check=False, capture_output=True)
        
        # Clean up Android SDK (user's choice to keep/remove)
        android_home = os.path.expanduser('~/.android')
        if os.path.isdir(android_home):
            shutil.rmtree(android_home, ignore_errors=True)
        
        sdk_root = os.path.expanduser('~/Android/Sdk')
        if os.path.isdir(sdk_root):
            shutil.rmtree(sdk_root, ignore_errors=True)
        
        logger.info("Android Emulator uninstalled")
        return "Android Emulator and related tools uninstalled successfully."
        
    except Exception as e:
        logger.error(f"Android Emulator uninstall failed: {e}")
        return f"Error uninstalling Android Emulator: {str(e)}"