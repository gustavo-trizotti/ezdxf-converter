# ezdxf-convert Quick Reference

## Installation
```bash
pip install -e .
```

## Basic Usage
```bash
# Convert DXF to SVG (output in same directory)
ezdxf-convert input.dxf

# Specify output path
ezdxf-convert input.dxf -o output.svg

# Convert DWG (requires ODA File Converter)
ezdxf-convert input.dwg --oda-path "C:\ODA\ODAFileConverter.exe"
```

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `input` | Input DXF/DWG file (required) | - |
| `-o, --output` | Output SVG file path | Same as input with .svg |
| `--lineweight-scaling` | Line weight scaling factor | 0.05 |
| `--layers` | Separate layers into SVG groups | Off |
| `--metrics` | Show performance metrics | Off |
| `--oda-path` | Path to ODA File Converter | $ODA_FILE_CONVERTER |
| `--verbose` | Verbose output | Off |
| `--version` | Show version | - |
| `--help` | Show help | - |

## Environment Variables
```bash
# Set ODA File Converter path
export ODA_FILE_CONVERTER="/path/to/ODAFileConverter"  # Linux/Mac
set ODA_FILE_CONVERTER=C:\ODA\ODAFileConverter.exe      # Windows CMD
$env:ODA_FILE_CONVERTER="C:\ODA\ODAFileConverter.exe"   # PowerShell
```

## Common Workflows

### High Performance Conversion
```bash
ezdxf-convert input.dxf  # Minimal output, maximum speed
```

### Detailed Analysis
```bash
ezdxf-convert input.dxf --metrics --verbose
```

### Layer-Aware SVG
```bash
ezdxf-convert input.dxf --layers -o output.svg
```

### Custom Line Weights
```bash
ezdxf-convert input.dxf --lineweight-scaling 0.1  # Thicker lines
ezdxf-convert input.dxf --lineweight-scaling 0.02 # Thinner lines
```

### Batch Processing
```bash
# Bash
for f in *.dxf; do ezdxf-convert "$f"; done

# PowerShell
Get-ChildItem *.dxf | ForEach-Object { ezdxf-convert $_.Name }
```

## Performance Tips

1. **DXF over DWG**: Use DXF when possible (no ODA overhead)
2. **Disable metrics**: Only use `--metrics` when analyzing performance
3. **Skip layers**: Omit `--layers` unless needed (slight overhead)
4. **Use SSD**: Fast storage improves I/O performance
5. **Batch process**: Convert multiple files in one session

## Troubleshooting

### "ODA File Converter path not specified"
```bash
# Solution: Set ODA path or use --oda-path flag
ezdxf-convert input.dwg --oda-path "C:\ODA\ODAFileConverter.exe"
```

### "Input file not found"
```bash
# Solution: Check file path is correct
ls input.dxf  # Verify file exists
```

### "Unsupported file format"
```bash
# Solution: Only .dxf and .dwg files supported
# Convert other formats to DXF first
```

## Module API (Advanced)

```python
from ezdxf_converter.converter import convert_dxf_to_svg
from ezdxf_converter.utils import PerformanceMetrics

# Convert programmatically
metrics = convert_dxf_to_svg(
    input_path="input.dxf",
    output_path="output.svg",
    lineweight_scaling=0.05,
    separate_layers=True
)

print(f"Conversion took {sum(metrics.values()):.4f} seconds")
```

## Project Structure
```
ezdxf_converter/
├── __init__.py       # Package version
├── cli.py            # CLI entry point
├── converter.py      # DXF→SVG conversion
├── dwg_handler.py    # DWG→DXF via ODA
└── utils.py          # Utilities & metrics
```

## Links

- **ezdxf Documentation**: https://ezdxf.mozman.at/
- **ODA File Converter**: https://www.opendesign.com/guestfiles/oda_file_converter
- **Full README**: See README.md in project root
