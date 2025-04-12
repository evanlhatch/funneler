#!/usr/bin/env python3

import os
import sys
import subprocess
import venv
import argparse
import shutil
from pathlib import Path

def create_venv_if_not_exists(venv_dir):
    """Create a virtual environment if it doesn't exist."""
    if not os.path.exists(venv_dir):
        print(f"Creating virtual environment in {venv_dir}...")
        venv.create(venv_dir, with_pip=True)
        return True
    return False

def get_venv_python(venv_dir):
    """Get the path to the Python executable in the virtual environment."""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_dir, 'Scripts', 'python.exe')
    else:  # Unix-like
        return os.path.join(venv_dir, 'bin', 'python')

def get_venv_pip(venv_dir):
    """Get the path to the pip executable in the virtual environment."""
    if os.name == 'nt':  # Windows
        return os.path.join(venv_dir, 'Scripts', 'pip.exe')
    else:  # Unix-like
        return os.path.join(venv_dir, 'bin', 'pip')

def install_package(venv_dir, package_dir):
    """Install the package in development mode."""
    pip_path = get_venv_pip(venv_dir)
    subprocess.check_call([pip_path, 'install', '-e', package_dir])

def run_funneler(venv_dir, script_dir, args):
    """Run the funneler command with the given arguments."""
    # Get the path to the Python executable in the virtual environment
    python_path = get_venv_python(venv_dir)
    
    # Path to the funneler.py script
    funneler_script = os.path.join(script_dir, 'funneler.py')
    
    # Construct the command to run funneler
    cmd = [python_path, funneler_script]
    cmd.extend(args)
    
    # Run the command
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nExiting...")

def main():
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Set up the virtual environment directory
    venv_dir = os.path.join(script_dir, '.venv')
    
    # Create the virtual environment if it doesn't exist
    newly_created = create_venv_if_not_exists(venv_dir)
    
    # Install the package if the virtual environment was newly created
    if newly_created:
        print("Installing funneler package...")
        install_package(venv_dir, script_dir)
    
    # Run funneler with the arguments passed to this script
    run_funneler(venv_dir, script_dir, sys.argv[1:])

if __name__ == '__main__':
    main()
