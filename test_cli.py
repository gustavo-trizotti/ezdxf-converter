"""
Manual test script for ezdxf-convert CLI.

This validates the CLI structure and conversion logic.
Run in an environment with ezdxf and Pillow installed.
"""

import sys
import os

# Add parent directory to path for local testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ezdxf_converter.utils import detect_file_type, resolve_output_path, FileType, PerformanceMetrics
from ezdxf_converter.converter import convert_dxf_to_svg

def test_utils():
    """Test utility functions."""
    print("Testing utility functions...")
    
    # Test file type detection
    assert detect_file_type("test.dxf") == FileType.DXF
    assert detect_file_type("test.DXF") == FileType.DXF
    assert detect_file_type("test.dwg") == FileType.DWG
    assert detect_file_type("test.DWG") == FileType.DWG
    
    try:
        detect_file_type("test.txt")
        assert False, "Should raise ValueError"
    except ValueError:
        pass
    
    # Test output path resolution
    assert resolve_output_path("input/test.dxf") == "input/test.svg"
    assert resolve_output_path("input/test.dxf", "output/custom.svg") == "output/custom.svg"
    
    # Test performance metrics
    metrics = PerformanceMetrics()
    metrics.start_stage("test")
    import time
    time.sleep(0.01)
    metrics.end_stage("test")
    assert metrics.get_total_time() >= 0.01
    assert "test" in metrics.format_metrics()
    
    print("✓ All utility tests passed!")

def test_conversion():
    """Test DXF to SVG conversion."""
    print("\nTesting DXF to SVG conversion...")
    
    input_file = "input/residential.dxf"
    output_file = "output/test_output.svg"
    
    if not os.path.exists(input_file):
        print(f"⚠ Skipping conversion test - input file not found: {input_file}")
        return
    
    try:
        # Test basic conversion
        metrics = convert_dxf_to_svg(input_file, output_file, lineweight_scaling=0.05)
        
        assert os.path.exists(output_file), "Output file not created"
        assert metrics['read_dxf'] > 0, "Read time not recorded"
        assert metrics['render_svg'] > 0, "Render time not recorded"
        assert metrics['write_svg'] > 0, "Write time not recorded"
        
        total = sum(metrics.values())
        print(f"  Conversion completed in {total:.4f}s")
        print(f"    Read:   {metrics['read_dxf']:.4f}s")
        print(f"    Render: {metrics['render_svg']:.4f}s")
        print(f"    Write:  {metrics['write_svg']:.4f}s")
        
        # Test with layer separation
        output_file_layers = "output/test_output_layers.svg"
        metrics_layers = convert_dxf_to_svg(
            input_file, 
            output_file_layers, 
            lineweight_scaling=0.05,
            separate_layers=True
        )
        
        assert os.path.exists(output_file_layers), "Output file with layers not created"
        total_layers = sum(metrics_layers.values())
        print(f"\n  Conversion with layers completed in {total_layers:.4f}s")
        
        print("\n✓ All conversion tests passed!")
        
    except ImportError as e:
        print(f"⚠ Skipping conversion test - missing dependency: {e}")
    except Exception as e:
        print(f"✗ Conversion test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 60)
    print("ezdxf-convert Test Suite")
    print("=" * 60)
    
    test_utils()
    test_conversion()
    
    print("\n" + "=" * 60)
    print("Testing complete!")
    print("=" * 60)
