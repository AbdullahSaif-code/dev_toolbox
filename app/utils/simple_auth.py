import subprocess
import os
import time
import threading
from .logging import get_logger

logger = get_logger(__name__)

class SimpleAuth:
    """Simple, working authentication system"""
    
    def __init__(self):
        self.sudo_cached = False
        self.cache_time = 0
        self.sudo_timeout = 300  # 5 minutes
    
    def check_sudo(self):
        """Check if sudo is cached"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'true'],
                capture_output=True,
                timeout=2,
                env={**os.environ, 'SUDO_ASKPASS': '/bin/false'}
            )
            is_cached = result.returncode == 0
            logger.info(f"Sudo cache status: {is_cached}")
            return is_cached
        except Exception as e:
            logger.error(f"Sudo check failed: {e}")
            return False
    
    def request_password(self):
        """
        Request password using zenity or kdialog
        Falls back to terminal prompt
        """
        try:
            logger.info("Requesting sudo password...")
            
            # Try graphical dialog first
            graphical_methods = [
                ['zenity', '--password', '--title=DevToolBox Admin Authentication'],
                ['kdialog', '--password', 'DevToolBox Admin Authentication:'],
            ]
            
            password = None
            for cmd in graphical_methods:
                try:
                    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
                    if result.returncode == 0:
                        password = result.stdout.strip()
                        logger.info("Password from GUI dialog")
                        break
                except Exception as e:
                    logger.debug(f"{cmd[0]} not available: {e}")
                    continue
            
            # If no GUI, return error asking user to use terminal
            if password is None:
                logger.error("No GUI dialog available")
                return False, "No graphical dialog available. Please run from terminal: sudo -v"
            
            # Use the password with sudo
            process = subprocess.Popen(
                ['sudo', '-S', 'true'],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            stdout, stderr = process.communicate(input=password + '\n', timeout=10)
            
            if process.returncode == 0:
                logger.info("✓ Authentication successful")
                self.sudo_cached = True
                self.cache_time = time.time()
                return True, "✓ Authentication successful! Admin access enabled."
            else:
                logger.warning("Authentication failed")
                return False, "✗ Authentication failed - wrong password."
        
        except subprocess.TimeoutExpired:
            logger.error("Auth timeout")
            return False, "✗ Authentication timed out."
        except Exception as e:
            logger.error(f"Auth error: {e}")
            return False, f"✗ Error: {str(e)}"
    
    def execute_sudo_cmd(self, cmd):
        """Execute a command with sudo"""
        try:
            result = subprocess.run(
                ['sudo', '-n'] + cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.returncode == 0, result.stdout, result.stderr
        except Exception as e:
            return False, "", str(e)

# Global auth instance
_auth = SimpleAuth()

def get_auth():
    return _auth