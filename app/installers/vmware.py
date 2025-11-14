import subprocess
import sys
import os
import urllib.request
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_vmware():
    """Install VMware Workstation Pro (Linux) - requires license or trial"""
    try:
        if sys.platform != 'linux':
            return "VMware Workstation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/vmware'):
            return "VMware Workstation is already installed."
        
        logger.warning("VMware Workstation requires manual download from VMware website")
        return ("VMware Workstation requires a license or trial activation. "
                "Download from: https://www.vmware.com/products/workstation-pro.html "
                "Then run: sudo ./VMware-Workstation-Full-*.bundle --console --required "
                "For open-source alternative, consider QEMU/KVM + virt-manager.")
        
    except Exception as e:
        logger.error(f"VMware installation info error: {e}")
        return f"Error: {str(e)}"

def uninstall_vmware():
    """Uninstall VMware Workstation"""
    try:
        if sys.platform != 'linux':
            return "VMware uninstallation is only supported on Linux."
        
        # Try standard uninstall method
        subprocess.run(['sudo', '/usr/bin/vmware-installer', '-u', 'vmware-workstation'], 
                      check=False, capture_output=True, timeout=120)
        
        # Cleanup remaining files
        subprocess.run(['sudo', 'rm', '-rf', '/usr/lib/vmware', '/opt/vmware', '/etc/vmware'],
                      check=False, capture_output=True)
        
        logger.info("VMware uninstalled")
        return "VMware Workstation uninstalled successfully."
        
    except Exception as e:
        logger.error(f"VMware uninstall failed: {e}")
        return f"Error uninstalling VMware: {str(e)}"