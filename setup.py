"""Setup configuration for ezdxf-convert."""

from setuptools import setup, find_packages
from pathlib import Path

# Read requirements
requirements = []
requirements_file = Path(__file__).parent / "requirements.txt"
if requirements_file.exists():
    with open(requirements_file, 'r') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    with open(readme_file, 'r', encoding='utf-8') as f:
        long_description = f.read()

setup(
    name="ezdxf-convert",
    version="1.0.0",
    author="Your Name",
    description="High-performance DXF/DWG to SVG converter using ezdxf library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ezdxf-converter",
    packages=find_packages(),
    install_requires=requirements,
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ezdxf-convert=ezdxf_converter.cli:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Graphics :: Graphics Conversion",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="dxf dwg svg cad conversion ezdxf drawing",
)
