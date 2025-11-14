import subprocess
import os
from .logging import get_logger

logger = get_logger(__name__)

def check_system_health():
    """Check system health and dependencies"""
    results = {
        "status": "healthy",
        "issues": [],
        "warnings": [],
        "tools": {}
    }
    
    # Check required tools
    required_tools = {
        'apt': '/usr/bin/apt',
        'sudo': '/usr/bin/sudo',
        'git': '/usr/bin/git',
    }
    
    optional_tools = {
        'snap': '/usr/bin/snap',
        'docker': '/usr/bin/docker',
        'python3': '/usr/bin/python3',
    }
    
    for tool, path in required_tools.items():
        if os.path.exists(path):
            results["tools"][tool] = "✓"
        else:
            results["tools"][tool] = "✗"
            results["issues"].append(f"Required tool not found: {tool}")
            results["status"] = "unhealthy"
    
    for tool, path in optional_tools.items():
        if os.path.exists(path):
            results["tools"][tool] = "✓"
        else:
            results["tools"][tool] = "⚠"
            results["warnings"].append(f"Optional tool not found: {tool}")
    
    # Check disk space
    try:
        result = subprocess.run(['df', '/'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        if len(lines) > 1:
            parts = lines[1].split()
            if len(parts) >= 5:
                usage_percent = int(parts[4].rstrip('%'))
                if usage_percent > 90:
                    results["warnings"].append(f"Low disk space: {usage_percent}%")
                results["disk_usage"] = usage_percent
    except Exception as e:
        logger.error(f"Disk check error: {e}")
    
    # Check memory
    try:
        with open('/proc/meminfo', 'r') as f:
            meminfo = dict((i.split()[0].rstrip(':'), int(i.split()[1])) for i in f.readlines())
            total = meminfo.get('MemTotal', 0)
            available = meminfo.get('MemAvailable', 0)
            if total > 0:
                usage_percent = int(100 * (total - available) / total)
                results["memory_usage"] = usage_percent
                if usage_percent > 85:
                    results["warnings"].append(f"High memory usage: {usage_percent}%")
    except Exception as e:
        logger.error(f"Memory check error: {e}")
    
    return results

def test_connections():
    """Test important connections"""
    tests = {
        "internet": False,
        "apt_repository": False,
        "snap_store": False,
    }
    
    # Test internet
    try:
        result = subprocess.run(
            ['ping', '-c', '1', '-W', '2', '8.8.8.8'],
            capture_output=True,
            timeout=5
        )
        tests["internet"] = result.returncode == 0
    except Exception:
        pass
    
    # Test apt
    try:
        result = subprocess.run(
            ['apt-cache', 'search', 'vim'],
            capture_output=True,
            timeout=10
        )
        tests["apt_repository"] = result.returncode == 0
    except Exception:
        pass
    
    # Test snap
    try:
        result = subprocess.run(
            ['snap', 'info', 'ubuntu-core'],
            capture_output=True,
            timeout=10
        )
        tests["snap_store"] = result.returncode == 0
    except Exception:
        pass
    
    return tests