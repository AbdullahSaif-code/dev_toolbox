import subprocess
import socket
from .logging import get_logger

logger = get_logger(__name__)

def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    try:
        socket.setdefaulttimeout(timeout)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((host, port))
        return True
    except Exception as e:
        logger.warning(f"Internet check failed: {e}")
        return False

def scan_upgrades() -> dict:
    """Return a dict with available upgrade info using apt in simulate mode.
    Does not require sudo and does not perform any changes.
    """
    try:
        # Update package lists (no sudo required for reading sources)
        update = subprocess.run([
            "apt-get", "update"
        ], capture_output=True, text=True)

        # Simulate upgrade to list packages to be upgraded
        sim = subprocess.run([
            "apt-get", "-s", "upgrade"
        ], capture_output=True, text=True)

        upgrades = []
        for line in sim.stdout.splitlines():
            # Lines like: Inst pkg [ver] (newver repo)
            if line.startswith("Inst "):
                upgrades.append(line)
        return {
            "updated": update.returncode == 0,
            "upgrade_count": len(upgrades),
            "upgrades": upgrades,
        }
    except FileNotFoundError:
        return {"error": "apt-get not found", "upgrades": [], "upgrade_count": 0}
    except Exception as e:
        logger.error(f"Upgrade scan error: {e}")
        return {"error": str(e), "upgrades": [], "upgrade_count": 0}

def check_sudo_cached() -> bool:
    """Return True if sudo timestamp is valid (no password prompt needed).
    Uses non-interactive mode so it never hangs the server process.
    """
    try:
        proc = subprocess.run([
            "sudo", "-n", "true"
        ], capture_output=True)
        return proc.returncode == 0
    except FileNotFoundError:
        # sudo not installed; treat as not available
        logger.warning("sudo not found on system")
        return False
    except Exception as e:
        logger.warning(f"sudo check failed: {e}")
        return False

def _run_collect(cmd: list[str]) -> tuple[int, str]:
    """Run a command and collect stdout+stderr as text."""
    proc = subprocess.run(cmd, capture_output=True, text=True)
    out = (proc.stdout or "") + (proc.stderr or "")
    return proc.returncode, out

def apt_update() -> tuple[str, str]:
    """Run sudo apt update and return (message, log)."""
    try:
        code, log = _run_collect(["pkexec", "/usr/bin/apt", "update"])
        if code == 0:
            return ("apt update completed.", log)
        return ("apt update failed.", log)
    except Exception as e:
        return ("apt update error.", str(e))

def apt_upgrade() -> tuple[str, str]:
    """Run sudo apt upgrade -y and return (message, log)."""
    try:
        code, log = _run_collect(["pkexec", "/usr/bin/apt", "upgrade", "-y"])
        if code == 0:
            return ("apt upgrade completed.", log)
        return ("apt upgrade failed.", log)
    except Exception as e:
        return ("apt upgrade error.", str(e))

def snap_refresh() -> tuple[str, str]:
    """Run sudo snap refresh and return (message, log)."""
    try:
        code, log = _run_collect(["pkexec", "/usr/bin/snap", "refresh"])
        if code == 0:
            return ("snap refresh completed.", log)
        return ("snap refresh failed.", log)
    except FileNotFoundError:
        return ("snap not installed.", "snap command not found")
    except Exception as e:
        return ("snap refresh error.", str(e))
