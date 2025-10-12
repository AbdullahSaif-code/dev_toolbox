import subprocess
import sys
import os
import tarfile
import urllib.request
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_pycharm():
    try:
        if sys.platform != 'linux':
            return "PyCharm installation is only supported on Linux."
        
        # Check if already installed (assuming in /opt)
        if os.path.exists('/opt/pycharm-professional'):
            return "PyCharm Professional is already installed."
        
        # Download and install
        url = 'https://download.jetbrains.com/python/pycharm-professional-2023.2.1.tar.gz'  # Update to latest
        tar_path = '/tmp/pycharm.tar.gz'
        urllib.request.urlretrieve(url, tar_path)
        
        with tarfile.open(tar_path, 'r:gz') as tar:
            tar.extractall('/opt')
        
        os.remove(tar_path)
        
        return "PyCharm Professional installed successfully!"
    except Exception as e:
        logger.error(f"Error installing PyCharm: {e}")
        return f"Error installing PyCharm Professional: {str(e)}"
