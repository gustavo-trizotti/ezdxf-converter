#!/bin/bash
# Build script for Linux binary
# Run this on a Linux machine

echo "Building ezdxf-convert for Linux..."

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
mv dist/build_entry bin/ezdxf-convert-linux
chmod +x bin/ezdxf-convert-linux

echo "Linux binary created at: bin/ezdxf-convert-linux"
