"""Core DXF to SVG conversion logic."""

import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout
from ezdxf.addons.drawing import svg as svg_backend
from ezdxf.addons.drawing import config
from pathlib import Path
from typing import Dict, Optional, Callable
import re


def _apply_background_color(svg_string: str, background_color: str) -> str:
    """Apply background color to SVG string."""
    if background_color == "DEFAULT" or background_color == "TRANSPARENT":
        return svg_string
    
    # Extract SVG tag
    svg_match = re.search(r'<svg[^>]*>', svg_string, re.IGNORECASE)
    if not svg_match:
        return svg_string
    
    svg_tag = svg_match.group(0)
    
    if background_color == "WHITE":
        bg_color = "white"
    elif background_color == "BLACK":
        bg_color = "black"
    else:
        return svg_string
    
    # Modify the SVG tag to include style attribute with background
    # Add xmlns attribute if not present to ensure valid SVG
    if 'xmlns' not in svg_tag:
        modified_tag = svg_tag.rstrip('>') + ' xmlns="http://www.w3.org/2000/svg">'
    else:
        modified_tag = svg_tag
    
    # Add style to SVG element for background
    if 'style=' not in modified_tag:
        modified_tag = modified_tag.rstrip('>') + f' style="background-color: {bg_color};">'
    else:
        # Append to existing style
        modified_tag = re.sub(
            r'style="([^"]*)"',
            f'style="\\1 background-color: {bg_color};"',
            modified_tag
        )
    
    new_svg = svg_string.replace(svg_tag, modified_tag, 1)
    return new_svg


def _create_layer_groups(doc, msp, backend, svg_config) -> str:
    """Create SVG with layer groups instead of flat structure."""
    from io import StringIO
    import xml.etree.ElementTree as ET
    
    # Render standard SVG first
    Frontend(RenderContext(doc), backend, svg_config).draw_layout(msp)
    svg_string = backend.get_string(layout.Page(0, 0))
    
    # For layer support, we'll need to modify the SVG to group by layers
    # This is a workaround since ezdxf's layer grouping isn't directly available
    # We'll enhance the SVG by wrapping elements in groups per layer
    
    try:
        root = ET.fromstring(svg_string)
        
        # Group elements by data-layer attribute (set by backend if available)
        # or create a default layer group
        layer_groups = {}
        
        for child in list(root):
            if child.tag.endswith('g'):
                # Keep existing groups
                layer_groups.setdefault('__groups__', []).append(child)
            else:
                # Group individual elements
                layer_id = child.get('data-layer', 'Layer0')
                if layer_id not in layer_groups:
                    group = ET.Element('g')
                    group.set('id', f'layer-{layer_id}')
                    group.set('class', 'dxf-layer')
                    layer_groups[layer_id] = group
                    root.append(group)
                
                if layer_id != '__groups__':
                    layer_groups[layer_id].append(child)
        
        svg_string = ET.tostring(root, encoding='unicode')
    except Exception:
        # If XML parsing fails, return original SVG
        pass
    
    return svg_string



def convert_dxf_to_svg(
    input_path: str,
    output_path: str,
    lineweight_scaling: float = 0.05,
    separate_layers: bool = False,
    background_color: str = "DEFAULT",
    stream_callback: Optional[Callable] = None,
    min_lineweight: float = 0.001
) -> Dict[str, float]:
    """
    Convert DXF file to SVG.
    
    Args:
        input_path: Path to input DXF file
        output_path: Path for output SVG file
        lineweight_scaling: Scaling factor for line weights (default: 0.05)
        separate_layers: Whether to separate layers into SVG groups (default: False)
        background_color: SVG background color (DEFAULT, WHITE, BLACK, TRANSPARENT)
        stream_callback: Optional callback function for progress reporting
        min_lineweight: Minimum line weight (default: 0.001)
        
    Returns:
        Dict with timing metrics for each stage
        
    Raises:
        IOError: If file reading/writing fails
        ezdxf.DXFError: If DXF parsing fails
    """
    import time
    metrics = {}
    
    def emit_event(event: str, **data):
        """Emit a progress event if callback is registered."""
        if stream_callback:
            stream_callback(event, data)
    
    # Read DXF file
    emit_event("read_start")
    start = time.perf_counter()
    doc = ezdxf.readfile(input_path)
    msp = doc.modelspace()
    metrics['read_dxf'] = time.perf_counter() - start
    emit_event("read_complete", duration=metrics['read_dxf'])
    
    # Configure SVG backend
    svg_config = config.Configuration(
        min_lineweight=min_lineweight,
        lineweight_scaling=lineweight_scaling
    )
    
    # Render to SVG
    emit_event("render_start")
    start = time.perf_counter()
    backend = svg_backend.SVGBackend()
    
    # Generate SVG with or without layer separation
    if separate_layers:
        svg_string = _create_layer_groups(doc, msp, backend, svg_config)
    else:
        Frontend(RenderContext(doc), backend, svg_config).draw_layout(msp)
        svg_string = backend.get_string(layout.Page(0, 0))
    
    metrics['render_svg'] = time.perf_counter() - start
    emit_event("render_complete", duration=metrics['render_svg'])
    
    # Apply background color
    svg_string = _apply_background_color(svg_string, background_color)
    
    # Write SVG file
    emit_event("write_start")
    start = time.perf_counter()
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Use buffered write for efficiency
    with open(output_path, 'wt', encoding='utf-8', buffering=8192) as fp:
        fp.write(svg_string)
    
    metrics['write_svg'] = time.perf_counter() - start
    emit_event("write_complete", duration=metrics['write_svg'])
    
    return metrics

