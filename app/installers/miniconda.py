import os
import shutil
import subprocess
from pathlib import Path
from ..utils.logging import get_logger

logger = get_logger(__name__)

HOME = str(Path.home())
CONDA_BIN = shutil.which("conda")
INSTALL_PREFIX = os.path.join(HOME, "miniconda3")
INSTALLER_PATH = "/tmp/Miniconda3.sh"


def install_miniconda():
    try:
        # Detect existing install
        if CONDA_BIN or os.path.exists(os.path.join(INSTALL_PREFIX, "bin", "conda")):
            return "Miniconda is already installed."

        # Download installer
        url = "https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh"
        subprocess.run(["wget", "-O", INSTALLER_PATH, url], check=True, capture_output=True)

        # Run installer in batch mode to user home prefix
        subprocess.run(["bash", INSTALLER_PATH, "-b", "-p", INSTALL_PREFIX], check=True, capture_output=True)

        # Cleanup
        try:
            os.remove(INSTALLER_PATH)
        except OSError:
            pass

        # Add to PATH in shell rc if not present
        bashrc = os.path.join(HOME, ".bashrc")
        path_line = f'export PATH="{INSTALL_PREFIX}/bin:$PATH"\n'
        already = False
        if os.path.exists(bashrc):
            with open(bashrc, "r", encoding="utf-8", errors="ignore") as f:
                already = path_line.strip() in f.read()
        if not already:
            with open(bashrc, "a", encoding="utf-8") as f:
                f.write("\n# Added by DevToolBox Miniconda installer\n")
                f.write(path_line)

        return "Miniconda installed successfully. Open a new shell or source ~/.bashrc to use conda."
    except subprocess.CalledProcessError as e:
        logger.error(f"Miniconda installer error: {e.stderr.decode(errors='ignore')}")
        return f"Error installing Miniconda: {e.stderr.decode(errors='ignore')}"
    except Exception as e:
        logger.error(f"Miniconda installation failed: {e}")
        return f"Error installing Miniconda: {str(e)}"
