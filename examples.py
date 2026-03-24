#!/usr/bin/env python3
"""
Example usage scripts for ezdxf-convert CLI.

These examples demonstrate the main features of the converter.
"""

import os
import subprocess
import sys

# Color codes for terminal output
GREEN = '\033[92m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
RESET = '\033[0m'

def run_example(description, command):
    """Run an example command and display output."""
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}Example: {description}{RESET}")
    print(f"{YELLOW}Command: {command}{RESET}")
    print(f"{BLUE}{'='*60}{RESET}\n")
    
    # Note: In production, this would actually run the command
    # subprocess.run(command, shell=True)
    print("(Command shown for reference - requires ezdxf-convert to be installed)")

def main():
    """Display example usage patterns."""
    print(f"{BLUE}╔═══════════════════════════════════════════════════════════╗{RESET}")
    print(f"{BLUE}║         ezdxf-convert Usage Examples                     ║{RESET}")
    print(f"{BLUE}╚═══════════════════════════════════════════════════════════╝{RESET}")
    
    # Example 1: Basic DXF conversion
    run_example(
        "Basic DXF to SVG conversion",
        "ezdxf-convert input/residential.dxf"
    )
    
    # Example 2: Custom output path
    run_example(
        "Convert with custom output path",
        "ezdxf-convert input/residential.dxf -o output/residential.svg"
    )
    
    # Example 3: Adjust lineweight scaling
    run_example(
        "Convert with thicker lines",
        "ezdxf-convert input/residential.dxf --lineweight-scaling 0.1"
    )
    
    # Example 4: Separate layers
    run_example(
        "Convert with layer separation",
        "ezdxf-convert input/residential.dxf --layers"
    )
    
    # Example 5: Show performance metrics
    run_example(
        "Convert and show performance metrics",
        "ezdxf-convert input/residential.dxf --metrics"
    )
    
    # Example 6: All options combined
    run_example(
        "Convert with all options",
        "ezdxf-convert input/residential.dxf -o output/result.svg --lineweight-scaling 0.08 --layers --metrics --verbose"
    )
    
    # Example 7: DWG conversion (requires ODA)
    run_example(
        "Convert DWG file (Windows)",
        'ezdxf-convert input.dwg --oda-path "C:\\Program Files\\ODA\\ODAFileConverter.exe"'
    )
    
    # Example 8: DWG with environment variable
    run_example(
        "Convert DWG with environment variable set",
        "export ODA_FILE_CONVERTER=/path/to/ODAFileConverter\nezdxf-convert input.dwg"
    )
    
    # Example 9: Batch processing (shell script)
    run_example(
        "Batch convert all DXF files in a directory",
        "for file in input/*.dxf; do\n  ezdxf-convert \"$file\" -o \"output/$(basename \"$file\" .dxf).svg\"\ndone"
    )
    
    # Installation reminder
    print(f"\n{BLUE}{'='*60}{RESET}")
    print(f"{GREEN}Installation:{RESET}")
    print(f"  pip install -e .")
    print(f"\n{GREEN}Help:{RESET}")
    print(f"  ezdxf-convert --help")
    print(f"\n{GREEN}Version:{RESET}")
    print(f"  ezdxf-convert --version")
    print(f"{BLUE}{'='*60}{RESET}\n")

if __name__ == "__main__":
    main()
