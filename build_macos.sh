#!/bin/bash
set -e

echo "Building ezdxf-convert for macOS..."

# Create isolated environment
python3.14 -m venv .venv
source .venv/bin/activate

# Install build dependencies
python -m pip install --upgrade pip
python -m pip install pyinstaller ezdxf pillow

# Build the binary
python -m PyInstaller --clean --noconfirm \
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

mkdir -p bin
mv dist/ezdxf-convert bin/ezdxf-convert-macos
chmod +x bin/ezdxf-convert-macos

echo "macOS binary created at: bin/ezdxf-convert-macos"