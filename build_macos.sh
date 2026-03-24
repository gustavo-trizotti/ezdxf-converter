#!/bin/bash
# Build script for macOS binary
# Run this on a macOS machine

echo "Building ezdxf-convert for macOS..."

# Install PyInstaller if not already installed
pip install pyinstaller

# Build the binary
pyinstaller --clean --noconfirm \
    --onefile \
    --name ezdxf-convert \
    --hidden-import ezdxf \
    --hidden-import ezdxf.addons.drawing \
    --hidden-import ezdxf.addons.drawing.svg \
    --hidden-import ezdxf.addons.drawing.layout \
    --hidden-import ezdxf.addons.drawing.config \
    --hidden-import PIL \
    --hidden-import PIL._imaging \
    --hidden-import ezdxf_converter \
    --hidden-import ezdxf_converter.cli \
    --hidden-import ezdxf_converter.converter \
    --hidden-import ezdxf_converter.utils \
    --hidden-import ezdxf_converter.dwg_handler \
    build_entry.py

# Move to bin directory
mkdir -p bin
mv dist/build_entry bin/ezdxf-convert-macos
chmod +x bin/ezdxf-convert-macos

echo "macOS binary created at: bin/ezdxf-convert-macos"
