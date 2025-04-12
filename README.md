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
git clone https://github.com/yourusername/funneler.git
cd funneler

# Install the package
pip install -e .
```

### Requirements

- Python 3.6+
- Tailscale with Funnel capability
- `sudo` access (required for Tailscale Funnel)

## Usage

### Using the Wrapper Script

The easiest way to use Funneler is with the included wrapper script, which automatically handles the virtual environment:

Share the current directory:

```bash
./run-funneler.fish
```

Share a specific directory:

```bash
./run-funneler.fish /path/to/directory
```

### Using the Installed Package

If you've installed the package, you can use it directly (make sure to activate the virtual environment first):

```bash
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
./run-funneler.fish
```

Share a specific directory on port 8080:

```bash
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
