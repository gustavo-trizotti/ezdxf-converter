# Building ezdxf-convert Binaries

This document explains how to build standalone executables for ezdxf-convert on different platforms.

## Current Status

✅ **Windows** - Binary built and ready at `bin/ezdxf-convert-windows.exe` (32.8 MB)
❌ **Linux** - Requires building on Linux (build script provided)
❌ **macOS** - Requires building on macOS (build script provided)

## Why Platform-Specific Builds?

Python binaries created with PyInstaller are platform-specific because they bundle:
- Platform-specific Python interpreter
- Compiled C extensions (e.g., numpy, PIL)
- Platform-specific system libraries

Therefore:
- Windows binaries must be built on Windows
- Linux binaries must be built on Linux
- macOS binaries must be built on macOS

## Quick Build Options

### Option 1: Local Build (Recommended for single platform)

#### Windows (Already Built ✅)
The Windows binary is already available at `bin/ezdxf-convert-windows.exe`

#### Linux
```bash
# On a Linux machine
git clone <repository>
cd ezdxf-converter
bash build_linux.sh
```

#### macOS
```bash
# On a macOS machine
git clone <repository>
cd ezdxf-converter
bash build_macos.sh
```

### Option 2: GitHub Actions (Recommended for all platforms)

If you push this repository to GitHub, you can use GitHub Actions to automatically build all three binaries:

1. Push the repository to GitHub
2. Go to Actions tab
3. Run the "Build Binaries" workflow manually, or
4. Create a git tag to trigger automatic builds:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

The workflow will:
- Build binaries for Windows, Linux, and macOS
- Create a GitHub Release with all binaries attached
- Make them available for download

### Option 3: Docker (Linux binary only)

You can build the Linux binary from any platform using Docker:

```bash
docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim bash -c "
  apt-get update && apt-get install -y binutils &&
  pip install -r requirements.txt &&
  pip install pyinstaller &&
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
    build_entry.py &&
  mkdir -p bin &&
  mv dist/build_entry bin/ezdxf-convert-linux &&
  chmod +x bin/ezdxf-convert-linux
"
```

**Note:** For PowerShell on Windows, use:
```powershell
docker run --rm -v "${PWD}:/app" -w /app python:3.11-slim bash -c "apt-get update && apt-get install -y binutils && pip install -r requirements.txt && pip install pyinstaller && pyinstaller --clean --noconfirm --onefile --name ezdxf-convert --hidden-import ezdxf --hidden-import ezdxf.addons.drawing --hidden-import ezdxf.addons.drawing.svg --hidden-import ezdxf.addons.drawing.layout --hidden-import ezdxf.addons.drawing.config --hidden-import PIL --hidden-import PIL._imaging --hidden-import ezdxf_converter --hidden-import ezdxf_converter.cli --hidden-import ezdxf_converter.converter --hidden-import ezdxf_converter.utils --hidden-import ezdxf_converter.dwg_handler build_entry.py && mkdir -p bin && mv dist/build_entry bin/ezdxf-convert-linux && chmod +x bin/ezdxf-convert-linux"
```

## Manual Build Instructions

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
pip install pyinstaller
```

### Step 2: Build the Binary

The PyInstaller spec file (`ezdxf-convert.spec`) is already configured. Simply run:

```bash
pyinstaller --clean --noconfirm ezdxf-convert.spec
```

Or use the command line directly:

```bash
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
```

### Step 3: Move Binary to bin Directory

#### Windows
```powershell
New-Item -ItemType Directory -Path bin -Force
Move-Item dist\ezdxf-convert.exe bin\ezdxf-convert-windows.exe
```

#### Linux / macOS
```bash
mkdir -p bin
mv dist/ezdxf-convert bin/ezdxf-convert-$(uname -s | tr '[:upper:]' '[:lower:]')
chmod +x bin/ezdxf-convert-$(uname -s | tr '[:upper:]' '[:lower:]')
```

## Testing the Binary

After building, test the binary:

### Windows
```cmd
bin\ezdxf-convert-windows.exe --version
bin\ezdxf-convert-windows.exe input\sample.dxf -o output\sample.svg
```

### Linux / macOS
```bash
./bin/ezdxf-convert-linux --version
./bin/ezdxf-convert-linux input/sample.dxf -o output/sample.svg
```

## Binary Characteristics

- **Size:** ~30-35 MB (includes Python interpreter and all dependencies)
- **Standalone:** No Python installation required
- **Dependencies:** All bundled (ezdxf, Pillow, numpy, etc.)
- **DWG Support:** Still requires ODA File Converter to be installed separately

## Troubleshooting

### Binary is too large
The binary size is normal for PyInstaller executables. If size is critical, consider:
- Using UPX compression: `--upx-dir=/path/to/upx`
- Excluding unnecessary packages
- Using PyInstaller's `--exclude-module` option

### Import errors at runtime
If you encounter import errors, add the missing module to the `hiddenimports` list in `ezdxf-convert.spec` or use `--hidden-import module_name`

### Permission denied (Linux/macOS)
Make sure the binary is executable:
```bash
chmod +x bin/ezdxf-convert-linux  # or ezdxf-convert-macos
```

## Distribution

Once built, the binaries in the `bin/` directory can be distributed directly. Users do not need:
- Python installation
- pip or package management
- Manual dependency installation

They only need:
- The appropriate binary for their platform
- ODA File Converter (if DWG support is needed)

## Next Steps

1. **For local use:** Use the Windows binary at `bin/ezdxf-convert-windows.exe`
2. **For Linux/macOS:** Run the build scripts on those platforms or use Docker
3. **For distribution:** Push to GitHub and use GitHub Actions for automated multi-platform builds
