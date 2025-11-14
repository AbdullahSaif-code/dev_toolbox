import subprocess
import socket
import time
from .logging import get_logger

logger = get_logger(__name__)

def check_internet(host: str = "8.8.8.8", port: int = 53, timeout: float = 3.0) -> bool:
    """Check internet connectivity"""
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        logger.debug("Internet connectivity confirmed")
        return True
    except Exception as e:
        logger.debug(f"Internet check failed: {e}")
        return False

def scan_upgrades() -> dict:
    """Return a dict with available upgrade info"""
    try:
        result = subprocess.run(
            ["apt-get", "-s", "upgrade"],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        upgrades = []
        for line in result.stdout.splitlines():
            if line.startswith("Inst "):
                upgrades.append(line)
        
        return {
            "upgrade_count": len(upgrades),
            "upgrades": upgrades,
        }
    except subprocess.TimeoutExpired:
        logger.warning("Upgrade scan timed out")
        return {"upgrade_count": 0, "upgrades": []}
    except FileNotFoundError:
        logger.warning("apt-get not found")
        return {"error": "apt-get not found", "upgrades": [], "upgrade_count": 0}
    except Exception as e:
        logger.error(f"Upgrade scan error: {e}")
        return {"error": str(e), "upgrades": [], "upgrade_count": 0}

def check_sudo_cached() -> bool:
    """Check if sudo is cached"""
    try:
        result = subprocess.run(
            ['sudo', '-n', 'true'],
            capture_output=True,
            timeout=2,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False

def _run_collect(cmd: list, timeout: int = 120) -> tuple:
    """Run a command and collect output"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        output = (result.stdout or "") + (result.stderr or "")
        return result.returncode, output
    except subprocess.TimeoutExpired:
        return 124, f"Command timed out after {timeout}s"
    except FileNotFoundError:
        return 127, f"Command not found: {cmd[0]}"
    except Exception as e:
        return 1, str(e)

def apt_update() -> tuple:
    """Run sudo apt update"""
    try:
        code, log = _run_collect(["sudo", "/usr/bin/apt", "update"], timeout=60)
        if code == 0:
            return ("✓ apt update completed", log)
        return (f"✗ apt update failed (code {code})", log)
    except Exception as e:
        return (f"✗ Error: {str(e)}", str(e))

def apt_upgrade() -> tuple:
    """Run sudo apt upgrade -y"""
    try:
        code, log = _run_collect(["sudo", "/usr/bin/apt", "upgrade", "-y"], timeout=300)
        if code == 0:
            return ("✓ apt upgrade completed", log)
        return (f"✗ apt upgrade failed (code {code})", log)
    except Exception as e:
        return (f"✗ Error: {str(e)}", str(e))

def snap_refresh() -> tuple:
    """Run sudo snap refresh"""
    try:
        code, log = _run_collect(["sudo", "/usr/bin/snap", "refresh"], timeout=300)
        if code == 0:
            return ("✓ snap refresh completed", log)
        return (f"✗ snap refresh failed (code {code})", log)
    except FileNotFoundError:
        return ("⚠ snap not installed", "snap command not found")
    except Exception as e:
        return (f"✗ Error: {str(e)}", str(e))

def one_click_upgrade() -> tuple:
    """Run all system upgrades"""
    results = {}
    logs = []
    
    logger.info("Starting one-click upgrade...")
    
    msg, log = apt_update()
    results["apt update"] = msg
    logs.append(f"=== apt update ===\n{log}\n")
    time.sleep(1)
    
    msg, log = apt_upgrade()
    results["apt upgrade"] = msg
    logs.append(f"=== apt upgrade ===\n{log}\n")
    time.sleep(1)
    
    msg, log = snap_refresh()
    results["snap refresh"] = msg
    logs.append(f"=== snap refresh ===\n{log}\n")
    
    combined_log = "".join(logs)
    return results, combined_log

def do_release_upgrade() -> tuple:
    """Run do-release-upgrade"""
    try:
        code, log = _run_collect(
            ["sudo", "/usr/bin/do-release-upgrade", "-f", "DistUpgradeViewNonInteractive"],
            timeout=3600
        )
        if code == 0:
            return ("✓ Distribution upgrade completed", log)
        return (f"✗ do-release-upgrade failed (code {code})", log)
    except Exception as e:
        return (f"✗ Error: {str(e)}", str(e))
