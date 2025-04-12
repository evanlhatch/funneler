#!/usr/bin/env fish

# Get the directory of this script
set SCRIPT_DIR (dirname (realpath (status -f)))

# Activate the virtual environment
source $SCRIPT_DIR/.venv/bin/activate.fish

# Run the funneler command with all arguments passed to this script
funneler $argv

# Deactivate the virtual environment when done
# This will only happen if funneler exits normally (not with Ctrl+C)
# Since funneler runs in an infinite loop until Ctrl+C, this won't normally be reached
deactivate
