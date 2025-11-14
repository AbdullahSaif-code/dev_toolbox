import subprocess
import sys
import os
import time
import pty
import select
from .logging import get_logger

logger = get_logger(__name__)

class AuthManager:
    """Manage sudo authentication and password caching"""
    
    def __init__(self):
        self.sudo_timeout = 300  # 5 minutes
        self.last_auth_time = 0
        self.auth_process = None
    
    def is_sudo_cached(self):
        """Check if sudo is already authenticated"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                timeout=3,
                text=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
            cached = result.returncode == 0
            logger.debug(f"Sudo cached check: {cached}")
            return cached
        except subprocess.TimeoutExpired:
            logger.debug("Sudo check timed out")
            return False
        except Exception as e:
            logger.debug(f"Sudo check error: {e}")
            return False
    
    def request_sudo_password(self, timeout=90):
        """
        Request sudo password via TTY dialog
        Must be called from a web context where user can respond
        """
        try:
            logger.info("Attempting to request sudo password...")
            
            # Try to allocate a pseudo-terminal for interactive input
            # This allows the sudo password prompt to appear
            
            process = subprocess.Popen(
                ['sudo', '-v', '-p', 'DevToolBox needs your password: '],
                stdin=sys.stdin,
                stdout=sys.stdout,
                stderr=sys.stderr,
                text=True,
                preexec_fn=None,
                env=dict(os.environ, SUDO_ASKPASS_IGNORE=1)
            )
            
            try:
                returncode = process.wait(timeout=timeout)
                
                if returncode == 0:
                    self.last_auth_time = time.time()
                    logger.info("✓ Authentication successful")
                    return True, "✓ Authentication successful! Admin access enabled for 5 minutes."
                elif returncode == 1:
                    logger.warning("Authentication failed - wrong password")
                    return False, "✗ Authentication failed - incorrect password."
                else:
                    logger.warning(f"Authentication failed with code {returncode}")
                    return False, f"✗ Authentication failed (code {returncode})."
            
            except subprocess.TimeoutExpired:
                process.kill()
                logger.error("Authentication timeout")
                return False, "✗ Authentication timed out. Please try again."
        
        except KeyboardInterrupt:
            logger.info("Authentication cancelled by user")
            return False, "✗ Authentication cancelled."
        except Exception as e:
            logger.error(f"Authentication error: {e}", exc_info=True)
            return False, f"✗ Error: {str(e)}"
    
    def validate_sudo_access(self):
        """Validate if current sudo session is still valid"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                timeout=3,
                text=True,
                stdin=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            logger.debug(f"Sudo validation error: {e}")
            return False
    
    def extend_sudo_session(self):
        """Extend the current sudo session timeout"""
        try:
            result = subprocess.run(
                ['sudo', '-v'],
                capture_output=True,
                timeout=5,
                text=True,
                stdin=subprocess.DEVNULL
            )
            return result.returncode == 0
        except Exception as e:
            logger.error(f"Extend sudo error: {e}")
            return False

# Global instance
_auth_manager = None

def get_auth_manager():
    """Get or create authentication manager instance"""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager