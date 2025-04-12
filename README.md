# Funneler

A simple CLI tool to share directories via Tailscale Funnel.

## Overview

Funneler makes it easy to share any directory on your computer with anyone on the internet using Tailscale Funnel. It automatically:

1. Starts a Python HTTP server to serve the files in the directory
2. Configures Tailscale Funnel to expose the server to the internet
3. Provides you with a URL that can be accessed from anywhere
4. Cleans up everything when you're done

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/evanlhatch/funneler.git
cd funneler
```

That's it! You can now use the shell-agnostic launcher script:

```bash
./funneler-launcher.py
```

The launcher script will automatically create a virtual environment and install all dependencies the first time you run it.

#### Manual Installation (Alternative)

If you prefer to install manually:

```bash
# Using uv (recommended)
uv venv
source .venv/bin/activate  # For Bash/Zsh
# OR source .venv/bin/activate.fish  # For Fish
uv pip install -e .

# Using standard pip
python -m venv .venv
source .venv/bin/activate  # For Bash/Zsh
# OR source .venv/bin/activate.fish  # For Fish
pip install -e .
```

### Requirements

- Python 3.6+
- Tailscale with Funnel capability
- `sudo` access (required for Tailscale Funnel)

## Usage

### Using the Shell-Agnostic Launcher (Recommended)

The easiest way to use Funneler is with the included shell-agnostic launcher script, which works on any system with Python 3.6+ installed:

Share the current directory:

```bash
# Works on any system with Python 3.6+
./funneler-launcher.py
```

Share a specific directory:

```bash
./funneler-launcher.py /path/to/directory
```

The launcher script automatically:
- Creates a virtual environment if it doesn't exist
- Installs the required dependencies
- Runs the funneler command with the provided arguments

### Using the Fish Shell Wrapper

If you're using the Fish shell, you can also use the included Fish wrapper script:

```fish
./run-funneler.fish [OPTIONS] [DIRECTORY]
```

### Using the Installed Package Directly

If you've installed the package, you can use it directly (make sure to activate the virtual environment first):

```bash
# For Bash/Zsh
source .venv/bin/activate
funneler [OPTIONS] [DIRECTORY]
deactivate  # when done

# For Fish
source .venv/bin/activate.fish
funneler [OPTIONS] [DIRECTORY]
deactivate  # when done
```

### Options

- `--port`, `-p`: Specify the port to use for the HTTP server (default: 8000)
- `--help`, `-h`: Show help message

### Examples

Share the current directory on the default port (8000):

```bash
# Shell-agnostic (works everywhere)
./funneler-launcher.py

# Fish shell
./run-funneler.fish
```

Share a specific directory on port 8080:

```bash
# Shell-agnostic (works everywhere)
./funneler-launcher.py --port 8080 /path/to/directory

# Fish shell
./run-funneler.fish --port 8080 /path/to/directory
```

## How It Works

1. Funneler starts a Python HTTP server in the specified directory
2. It uses `sudo tailscale funnel` to expose the server to the internet
3. It automatically detects your Tailscale machine name and tailnet domain
4. When you press Ctrl+C, it cleans up by stopping the server and resetting the Funnel configuration

## Notes

- Tailscale Funnel requires `sudo` access to set up
- The shared URL will be in the format: `https://<machine-name>.<tailnet-domain>/`
- Files are served with their relative paths from the shared directory
