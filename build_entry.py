"""Entry point script for PyInstaller build."""
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(__file__))

from ezdxf_converter.cli import main

if __name__ == "__main__":
    main()
