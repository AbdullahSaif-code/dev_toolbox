import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_jupyter():
    try:
        if sys.platform != 'linux':
            return "Jupyter installation is only supported on Linux."
        
        # Install via pip
        subprocess.run(['pip3', 'install', 'jupyter'], check=True, capture_output=True)
        
        return "Jupyter Notebook installed successfully!"
    except subprocess.CalledProcessError as e:
        logger.error(f"Error installing Jupyter: {e}")
        return f"Error installing Jupyter Notebook: {e.stderr.decode()}"
