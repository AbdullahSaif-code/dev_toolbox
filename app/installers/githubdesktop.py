import subprocess
import sys
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_githubdesktop():
    try:
        if sys.platform != 'linux':
            return "GitHub Desktop installation is only supported on Linux."
        
        # GitHub Desktop doesn't have an official Linux version; suggest alternative
        return "GitHub Desktop is not available for Linux. Consider using GitHub CLI or a web-based alternative."
    except Exception as e:
        logger.error(f"Error with GitHub Desktop: {e}")
        return f"Error: {str(e)}"
