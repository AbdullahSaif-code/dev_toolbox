import subprocess
import sys
import os
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_slack():
    try:
        if sys.platform != 'linux':
            return "Slack installation is only supported on Linux."
        
        # Check if already installed
        if os.path.exists('/usr/bin/slack'):
            return "Slack is already installed."
        
        # Install via snap
        subprocess.run(['sudo', 'snap', 'install', 'slack', '--classic'], check=True, capture_output=True)
        
        return "Slack installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Slack: {e}")
        return f"Error installing Slack: {e.stderr.decode()}"
