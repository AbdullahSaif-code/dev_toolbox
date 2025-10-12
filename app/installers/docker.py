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
