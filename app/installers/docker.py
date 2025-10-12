import subprocess
import sys

def install_docker():
    try:
        if sys.platform == 'linux':
            subprocess.run(['sudo', 'apt', 'update'], check=True)
            subprocess.run(['sudo', 'apt', 'install', '-y', 'docker.io'], check=True)
            subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
            subprocess.run(['sudo', 'usermod', '-aG', 'docker', '$USER'], check=True)
            return "Docker installed successfully!"
        elif sys.platform == 'darwin':
            subprocess.run(['brew', 'install', 'docker'], check=True)
            return "Docker installed successfully!"
        else:
            return "Unsupported OS for Docker installation."
    except subprocess.CalledProcessError as e:
        return f"Error installing Docker: {str(e)}"

def uninstall_docker():
    try:
        if sys.platform != 'linux':
            return "Unsupported OS for Docker uninstallation."
        # Stop service if running, ignore errors
        subprocess.run(['sudo', 'systemctl', 'stop', 'docker'], check=False)
        # Remove package
        subprocess.run(['sudo', 'apt', 'remove', '-y', 'docker.io'], check=True)
        return "Docker uninstalled successfully."
    except subprocess.CalledProcessError as e:
        return f"Error uninstalling Docker: {str(e)}"
