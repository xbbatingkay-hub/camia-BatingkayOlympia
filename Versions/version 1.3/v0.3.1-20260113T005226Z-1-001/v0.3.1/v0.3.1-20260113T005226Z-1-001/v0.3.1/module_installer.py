import subprocess
import sys
import importlib

# Simple automatic installer of required modules and stuff
def install_and_import(package):
    try:
        importlib.import_module(package)
        print(f"{package} is already installed.")
    except ImportError:
        print(f"{package} not found, attempting to install...")
        try:
            # Use sys.executable to ensure the correct pip for the current interpreter is used
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}. Error: {e}")
            sys.exit(1)
# Install them packages
install_and_import('sv_ttk')
install_and_import('pygame')