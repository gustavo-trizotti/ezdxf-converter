"""
Basic structure test for ezdxf-convert CLI.
Tests components that don't require PIL.
"""

import sys
import os

# Add parent directory to path for local testing
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported (structure check)."""
    print("Testing module imports...")
    
    try:
        from ezdxf_converter import __version__
        print(f"✓ Package version: {__version__}")
    except Exception as e:
        print(f"✗ Package import failed: {e}")
        return False
    
    try:
        from ezdxf_converter.utils import detect_file_type, resolve_output_path, FileType, PerformanceMetrics
        print("✓ Utils module imported")
    except Exception as e:
        print(f"✗ Utils import failed: {e}")
        return False
    
    try:
        from ezdxf_converter.dwg_handler import get_oda_path, ODAConverterError
        print("✓ DWG handler module imported")
    except Exception as e:
        print(f"✗ DWG handler import failed: {e}")
        return False
    
    return True

def test_utils():
    """Test utility functions."""
    print("\nTesting utility functions...")
    
    from ezdxf_converter.utils import detect_file_type, resolve_output_path, FileType, PerformanceMetrics
    
    # Test file type detection
    assert detect_file_type("test.dxf") == FileType.DXF
    assert detect_file_type("test.DXF") == FileType.DXF
    assert detect_file_type("test.dwg") == FileType.DWG
    assert detect_file_type("test.DWG") == FileType.DWG
    print("✓ File type detection works")
    
    try:
        detect_file_type("test.txt")
        assert False, "Should raise ValueError"
    except ValueError:
        print("✓ Invalid file type correctly rejected")
    
    # Test output path resolution
    assert resolve_output_path("input/test.dxf") == "input\\test.svg" or resolve_output_path("input/test.dxf") == "input/test.svg"
    assert resolve_output_path("input/test.dxf", "output/custom.svg") == "output/custom.svg"
    print("✓ Output path resolution works")
    
    # Test performance metrics
    metrics = PerformanceMetrics()
    metrics.start_stage("test")
    import time
    time.sleep(0.01)
    metrics.end_stage("test")
    assert metrics.get_total_time() >= 0.01
    assert "test" in metrics.format_metrics()
    print("✓ Performance metrics tracking works")
    
    print("\n✓ All utility tests passed!")
    return True

def test_dwg_handler():
    """Test DWG handler functions."""
    print("\nTesting DWG handler...")
    
    from ezdxf_converter.dwg_handler import get_oda_path, ODAConverterError
    
    # Test ODA path not found scenario
    try:
        get_oda_path(None)
        print("✗ Should have raised ODAConverterError")
        return False
    except ODAConverterError as e:
        print(f"✓ ODA path error correctly raised: {str(e)[:50]}...")
    
    print("✓ DWG handler tests passed!")
    return True

def test_cli_parser():
    """Test CLI parser structure."""
    print("\nTesting CLI parser...")
    
    try:
        from ezdxf_converter.cli import create_parser
        parser = create_parser()
        
        # Test help generation
        help_str = parser.format_help()
        assert "ezdxf-convert" in help_str
        assert "--output" in help_str
        assert "--lineweight-scaling" in help_str
        assert "--layers" in help_str
        assert "--metrics" in help_str
        assert "--oda-path" in help_str
        print("✓ CLI parser structure is correct")
        
        # Test argument parsing
        args = parser.parse_args(["test.dxf", "-o", "output.svg", "--lineweight-scaling", "0.1", "--layers", "--metrics"])
        assert args.input == "test.dxf"
        assert args.output == "output.svg"
        assert args.lineweight_scaling == 0.1
        assert args.layers == True
        assert args.metrics == True
        print("✓ CLI argument parsing works")
        
        print("\n✓ CLI parser tests passed!")
        return True
    except Exception as e:
        print(f"✗ CLI parser test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_project_structure():
    """Test project file structure."""
    print("\nTesting project structure...")
    
    expected_files = [
        "ezdxf_converter/__init__.py",
        "ezdxf_converter/cli.py",
        "ezdxf_converter/converter.py",
        "ezdxf_converter/dwg_handler.py",
        "ezdxf_converter/utils.py",
        "setup.py",
        "requirements.txt",
        "README.md"
    ]
    
    for file_path in expected_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path}")
        else:
            print(f"✗ Missing: {file_path}")
            return False
    
    print("\n✓ All required files present!")
    return True

if __name__ == "__main__":
    print("=" * 60)
    print("ezdxf-convert Structure Test Suite")
    print("=" * 60)
    print()
    
    all_passed = True
    
    all_passed = test_imports() and all_passed
    all_passed = test_project_structure() and all_passed
    all_passed = test_utils() and all_passed
    all_passed = test_dwg_handler() and all_passed
    all_passed = test_cli_parser() and all_passed
    
    print("\n" + "=" * 60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nNote: Conversion tests require Pillow (PIL) to be installed.")
        print("To fully test the converter, install in an environment with:")
        print("  pip install -e .")
    else:
        print("✗ SOME TESTS FAILED")
        sys.exit(1)
    print("=" * 60)
