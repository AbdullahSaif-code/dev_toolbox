import subprocess
import sys
import os
import shutil
from pathlib import Path
from ..utils.logging import get_logger

logger = get_logger(__name__)

def install_flutter():
    try:
        if sys.platform != 'linux':
            return "Flutter installation is only supported on Linux."
        
        # Check if already installed
        if shutil.which('flutter'):
            return "Flutter is already installed."
        
        flutter_dir = os.path.expanduser('~/Development/flutter')
        os.makedirs(os.path.expanduser('~/Development'), exist_ok=True)
        
        # Install dependencies
        subprocess.run(['sudo', 'apt', 'update'], check=True, capture_output=True)
        subprocess.run(['sudo', 'apt', 'install', '-y', 'git', 'curl', 'libglu1-mesa'], 
                      check=True, capture_output=True)
        
        # Clone Flutter repo
        subprocess.run(['git', 'clone', 'https://github.com/flutter/flutter.git', '-b', 'stable', flutter_dir], 
                      check=True, capture_output=True)
        
        # Add to PATH
        bashrc = os.path.expanduser('~/.bashrc')
        path_line = f'export PATH="{flutter_dir}/bin:$PATH"\n'
        
        if os.path.exists(bashrc):
            with open(bashrc, 'r') as f:
                content = f.read()
                if path_line.strip() not in content:
                    with open(bashrc, 'a') as f:
                        f.write(path_line)
        
        # Run flutter doctor
        env = os.environ.copy()
        env['PATH'] = f"{flutter_dir}/bin:{env['PATH']}"
        subprocess.run([os.path.join(flutter_dir, 'bin', 'flutter'), 'doctor'], 
                      capture_output=True, env=env)
        
        return "Flutter installed successfully! Run 'source ~/.bashrc' and 'flutter doctor' in a new terminal."
        
    except subprocess.CalledProcessError as e:
        err = e.stderr.decode(errors='ignore') if e.stderr else str(e)
        logger.error(f"Error installing Flutter: {err}")
        return f"Error installing Flutter: {err}"
    except Exception as e:
        logger.error(f"Flutter installation failed: {e}")
        return f"Error installing Flutter: {str(e)}"

def uninstall_flutter():
    try:
        if sys.platform != 'linux':
            return "Flutter uninstallation is only supported on Linux."
        
        flutter_dir = os.path.expanduser('~/Development/flutter')
        if os.path.isdir(flutter_dir):
            shutil.rmtree(flutter_dir)
        
        # Remove from PATH
        bashrc = os.path.expanduser('~/.bashrc')
        if os.path.exists(bashrc):
            with open(bashrc, 'r') as f:
                lines = f.readlines()
            with open(bashrc, 'w') as f:
                for line in lines:
                    if 'flutter' not in line.lower():
                        f.write(line)
        
        return "Flutter uninstalled successfully."
        
    except Exception as e:
        logger.error(f"Flutter uninstall failed: {e}")
        return f"Error uninstalling Flutter: {str(e)}"