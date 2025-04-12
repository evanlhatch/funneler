#!/usr/bin/env python3

import typer
import subprocess
import os
import signal
import sys
import time
from pathlib import Path
from typing import Optional, List
import atexit

app = typer.Typer(help="Share directories via Tailscale Funnel")
server_process = None
cleanup_registered = False

def get_tailscale_info():
    """Get machine name and tailnet domain from Tailscale."""
    try:
        # Get the machine name from tailscale status
        result = subprocess.run(
            ["tailscale", "status", "--self"],
            capture_output=True,
            text=True,
            check=True
        )
        
        # Parse the output to get the machine name
        lines = result.stdout.strip().split('\n')
        if not lines:
            typer.echo("Error: Could not get Tailscale status")
            sys.exit(1)
            
        # The machine name should be the second field in the first line
        parts = lines[0].split()
        if len(parts) < 2:
            typer.echo("Error: Unexpected Tailscale status output format")
            sys.exit(1)
            
        machine_info = parts[1]
        
        # Check if the machine name includes a domain
        if "." in machine_info:
            machine_name, *domain_parts = machine_info.split(".")
            tailnet_domain = ".".join(domain_parts)
        else:
            machine_name = machine_info
            # Try to get the tailnet name from the search domains
            try:
                search_result = subprocess.run(
                    ["tailscale", "status"],
                    capture_output=True,
                    text=True,
                    check=True
                )
                for line in search_result.stdout.split('\n'):
                    if "cinnamon-galaxy.ts.net" in line:  # This is a common pattern in the output
                        tailnet_domain = "cinnamon-galaxy.ts.net"
                        break
                else:
                    tailnet_domain = "tailnet.ts.net"  # Default fallback
            except:
                tailnet_domain = "tailnet.ts.net"  # Default fallback
                
        return machine_name, tailnet_domain
    except subprocess.CalledProcessError:
        typer.echo("Error: Failed to get Tailscale status. Is Tailscale running?")
        sys.exit(1)

def cleanup():
    """Clean up resources when the script exits."""
    global server_process
    
    typer.echo("\nCleaning up...")
    
    # Kill the HTTP server if it's running
    if server_process:
        try:
            server_process.terminate()
            server_process.wait(timeout=5)
        except:
            try:
                server_process.kill()
            except:
                pass
    
    # Reset Tailscale Funnel
    try:
        subprocess.run(
            ["sudo", "tailscale", "funnel", "reset"],
            check=False
        )
        typer.echo("Funnel and HTTP server stopped.")
    except:
        typer.echo("Warning: Failed to reset Tailscale Funnel.")

def signal_handler(sig, frame):
    """Handle Ctrl+C."""
    cleanup()
    sys.exit(0)

@app.command()
def share(
    directory: Optional[Path] = typer.Argument(
        None,
        help="Directory to share (defaults to current directory)",
        exists=True,
        file_okay=False,
        dir_okay=True,
    ),
    port: int = typer.Option(
        8000,
        "--port",
        "-p",
        help="Port to use for the HTTP server"
    ),
):
    """Share a directory via Tailscale Funnel."""
    global server_process, cleanup_registered
    
    # Register cleanup function and signal handler
    if not cleanup_registered:
        atexit.register(cleanup)
        signal.signal(signal.SIGINT, signal_handler)
        cleanup_registered = True
    
    # Use current directory if none specified
    if directory is None:
        directory = Path.cwd()
    
    # Get absolute path
    directory = directory.absolute()
    
    # Validate directory
    if not directory.exists():
        typer.echo(f"Error: Directory '{directory}' does not exist")
        sys.exit(1)
    
    # Get machine name and tailnet domain
    machine_name, tailnet_domain = get_tailscale_info()
    
    # Clean up any previous instances
    typer.echo("Cleaning up any previous instances...")
    try:
        subprocess.run(
            ["pkill", "-f", f"python3 -m http.server {port}"],
            check=False
        )
        subprocess.run(
            ["sudo", "tailscale", "funnel", "reset"],
            check=False
        )
    except:
        pass
    
    # Start Python HTTP server
    typer.echo(f"Starting Python HTTP server on port {port}...")
    typer.echo(f"Serving files from: {directory}")
    
    try:
        # Change to the directory
        os.chdir(directory)
        
        # Start the HTTP server
        server_process = subprocess.Popen(
            ["python3", "-m", "http.server", str(port)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Give the server a moment to start up
        time.sleep(2)
        
        # Configure Tailscale Funnel
        typer.echo("Configuring Tailscale Funnel (requires sudo)...")
        subprocess.run(
            ["sudo", "tailscale", "funnel", str(port)],
            check=True
        )
        
        # Display the URL
        typer.echo("")
        typer.echo("===================================================")
        typer.echo("Directory is now available via Tailscale Funnel at:")
        typer.echo(f"https://{machine_name}.{tailnet_domain}/")
        typer.echo("")
        typer.echo("Press Ctrl+C to stop the server and clean up")
        typer.echo("===================================================")
        
        # Keep the script running until Ctrl+C
        while True:
            time.sleep(1)
            
    except subprocess.CalledProcessError:
        typer.echo("Error: Failed to configure Tailscale Funnel")
        cleanup()
        sys.exit(1)
    except KeyboardInterrupt:
        cleanup()
        sys.exit(0)
    except Exception as e:
        typer.echo(f"Error: {str(e)}")
        cleanup()
        sys.exit(1)

if __name__ == "__main__":
    app()
