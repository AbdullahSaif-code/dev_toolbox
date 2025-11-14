import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_qemu():
    """Install QEMU/KVM hypervisor with virt-manager GUI"""
    try:
        if sys.platform != 'linux':
            return "QEMU/KVM is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/qemu-system-x86_64'):
            return "QEMU/KVM is already installed."
        
        # Install dependencies
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        
        # Install QEMU, KVM, and virt-manager
        packages = [
            'qemu-system-x86',
            'qemu-utils',
            'libvirt-daemon-system',
            'libvirt-clients',
            'virtinst',
            'virt-manager',
            'virt-viewer',
            'cpu-checker',
        ]
        
        subprocess.run(['sudo', 'apt', 'install', '-y'] + packages, 
                      check=True, capture_output=True, timeout=300)
        
        # Enable and start libvirtd service
        subprocess.run(['sudo', 'systemctl', 'enable', 'libvirtd'], 
                      check=False, capture_output=True)
        subprocess.run(['sudo', 'systemctl', 'start', 'libvirtd'], 
                      check=False, capture_output=True)
        
        # Add current user to libvirt group (requires re-login)
        import getpass
        user = getpass.getuser()
        subprocess.run(['sudo', 'usermod', '-aG', 'libvirt', user], 
                      check=False, capture_output=True)
        subprocess.run(['sudo', 'usermod', '-aG', 'kvm', user], 
                      check=False, capture_output=True)
        
        # Verify KVM support
        kvm_check = subprocess.run(['kvm-ok'], capture_output=True, text=True)
        kvm_status = "KVM acceleration enabled" if kvm_check.returncode == 0 else "KVM not available (will use software emulation)"
        
        logger.info("QEMU/KVM installed successfully")
        return (f"QEMU/KVM with virt-manager installed successfully! "
                f"{kvm_status}. "
                f"Launch 'virt-manager' from terminal to create VMs. "
                f"You may need to log out and log back in for group permissions to take effect.")
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing QEMU/KVM: {err}")
        return f"Error installing QEMU/KVM: {err}"
    except Exception as e:
        logger.error(f"QEMU/KVM installation failed: {e}")
        return f"Error installing QEMU/KVM: {str(e)}"

def uninstall_qemu():
    """Uninstall QEMU/KVM and virt-manager"""
    try:
        if sys.platform != 'linux':
            return "QEMU/KVM uninstallation is only supported on Linux."
        
        # Stop libvirtd service
        subprocess.run(['sudo', 'systemctl', 'stop', 'libvirtd'], 
                      check=False, capture_output=True)
        
        # Remove packages
        packages = [
            'qemu-system-x86',
            'qemu-utils',
            'virt-manager',
            'virt-viewer',
            'virtinst',
            'libvirt-clients',
            'libvirt-daemon-system',
        ]
        
        subprocess.run(['sudo', 'apt', 'remove', '-y'] + packages, 
                      check=False, capture_output=True)
        
        # Clean up
        subprocess.run(['sudo', 'rm', '-rf', '/var/lib/libvirt'], 
                      check=False, capture_output=True)
        
        logger.info("QEMU/KVM uninstalled")
        return "QEMU/KVM uninstalled successfully."
        
    except Exception as e:
        logger.error(f"QEMU/KVM uninstall failed: {e}")
        return f"Error uninstalling QEMU/KVM: {str(e)}"