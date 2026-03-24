"""Core DXF to SVG conversion logic."""

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing import svg as svg_backend
from ezdxf.addons.drawing import config
from pathlib import Path
from typing import Dict, Optional


def convert_dxf_to_svg(
    input_path: str,
    output_path: str,
    lineweight_scaling: float = 0.05,
    separate_layers: bool = False,
    min_lineweight: float = 0.001
) -> Dict[str, float]:
    """
    Convert DXF file to SVG.
    
    Args:
        input_path: Path to input DXF file
        output_path: Path for output SVG file
        lineweight_scaling: Scaling factor for line weights (default: 0.05)
        separate_layers: Whether to separate layers into SVG groups (default: False)
            Note: Layer separation is not supported in ezdxf 1.4.3+
        min_lineweight: Minimum line weight (default: 0.001)
        
    Returns:
        Dict with timing metrics for each stage
        
    Raises:
        IOError: If file reading/writing fails
        ezdxf.DXFError: If DXF parsing fails
    """
    import time
    metrics = {}
    
    # Read DXF file
    start = time.perf_counter()
    doc = ezdxf.readfile(input_path)
    msp = doc.modelspace()
    metrics['read_dxf'] = time.perf_counter() - start
    
    # Configure SVG backend
    svg_config = config.Configuration(
        min_lineweight=min_lineweight,
        lineweight_scaling=lineweight_scaling
    )
    
    # Render to SVG
    start = time.perf_counter()
    backend = svg_backend.SVGBackend()
    
    # Note: Layer separation via enter_group/exit_group is not available in ezdxf 1.4.3+
    # The separate_layers parameter is ignored for compatibility
    if separate_layers:
        import warnings
        warnings.warn(
            "Layer separation is not supported in ezdxf 1.4.3+. "
            "The --layers flag will be ignored.",
            UserWarning
        )
    
    # Standard rendering
    Frontend(RenderContext(doc), backend, svg_config).draw_layout(msp)
    
    metrics['render_svg'] = time.perf_counter() - start
    
    # Write SVG file
    start = time.perf_counter()
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    svg_string = backend.get_string(layout.Page(0, 0))
    
    # Use buffered write for efficiency
    with open(output_path, 'wt', encoding='utf-8', buffering=8192) as fp:
        fp.write(svg_string)
    
    metrics['write_svg'] = time.perf_counter() - start
    
    return metrics
