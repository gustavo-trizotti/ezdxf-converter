"""Command-line interface for ezdxf-convert."""

import argparse
import sys
import os
from pathlib import Path

from .utils import detect_file_type, resolve_output_path, PerformanceMetrics, FileType
from .dwg_handler import get_oda_path, convert_dwg_to_dxf, cleanup_temp_dxf, ODAConverterError


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog="ezdxf-convert",
        description="High-performance DXF/DWG to SVG converter using ezdxf library",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  ezdxf-convert input.dxf
  ezdxf-convert input.dwg --oda-path "C:\\ODA\\ODAFileConverter.exe"
  ezdxf-convert input.dxf -o output.svg --lineweight-scaling 0.1
  ezdxf-convert input.dxf --layers --metrics
  
Environment Variables:
  ODA_FILE_CONVERTER   Path to ODA File Converter executable (for DWG support)
        """
    )
    
    parser.add_argument(
        "input",
        help="Input DXF or DWG file path"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output SVG file path (default: same as input with .svg extension)",
        metavar="PATH"
    )
    
    parser.add_argument(
        "--lineweight-scaling",
        type=float,
        default=0.05,
        help="Line weight scaling factor (default: 0.05)",
        metavar="FLOAT"
    )
    
    parser.add_argument(
        "--layers",
        action="store_true",
        help="Separate layers into SVG groups"
    )
    
    parser.add_argument(
        "--metrics",
        action="store_true",
        help="Display performance metrics after conversion"
    )
    
    parser.add_argument(
        "--oda-path",
        help="Path to ODA File Converter executable (required for DWG files)",
        metavar="PATH"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    return parser


def main():
    """Main entry point for CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    metrics = PerformanceMetrics()
    temp_dxf_path = None
    
    try:
        # Validate input file
        if not os.path.isfile(args.input):
            print(f"Error: Input file not found: {args.input}", file=sys.stderr)
            sys.exit(1)
        
        # Detect file type
        try:
            file_type = detect_file_type(args.input)
        except ValueError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        
        if args.verbose:
            print(f"Input file: {args.input}")
            print(f"File type: {file_type.value.upper()}")
        
        # Handle DWG conversion
        dxf_path = args.input
        if file_type == FileType.DWG:
            if args.verbose:
                print("Converting DWG to DXF...")
            
            try:
                oda_path = get_oda_path(args.oda_path)
            except ODAConverterError as e:
                print(f"Error: {e}", file=sys.stderr)
                sys.exit(1)
            
            metrics.start_stage("dwg_to_dxf")
            try:
                temp_dxf_path = convert_dwg_to_dxf(args.input, oda_path)
                dxf_path = temp_dxf_path
            except ODAConverterError as e:
                print(f"Error: DWG conversion failed: {e}", file=sys.stderr)
                sys.exit(1)
            finally:
                metrics.end_stage("dwg_to_dxf")
            
            if args.verbose:
                print(f"Temporary DXF: {dxf_path}")
        
        # Resolve output path
        output_path = resolve_output_path(args.input, args.output)
        
        if args.verbose:
            print(f"Output file: {output_path}")
            print(f"Lineweight scaling: {args.lineweight_scaling}")
            print(f"Layer separation: {'enabled' if args.layers else 'disabled'}")
            print("\nConverting to SVG...")
        
        # Convert DXF to SVG
        try:
            # Lazy import to avoid PIL dependency at CLI load time
            from .converter import convert_dxf_to_svg
            
            conversion_metrics = convert_dxf_to_svg(
                input_path=dxf_path,
                output_path=output_path,
                lineweight_scaling=args.lineweight_scaling,
                separate_layers=args.layers
            )
            
            # Add conversion metrics to overall metrics
            for stage, duration in conversion_metrics.items():
                metrics.stages[stage] = duration
            
        except Exception as e:
            print(f"Error: Conversion failed: {e}", file=sys.stderr)
            sys.exit(1)
        
        # Success message
        if not args.metrics and not args.verbose:
            # Performance-first: minimal output
            print(f"Converted: {output_path}")
        else:
            print(f"\nSuccessfully converted to: {output_path}")
        
        # Display metrics if requested
        if args.metrics:
            print()
            print(metrics.format_metrics())
        
    except KeyboardInterrupt:
        print("\nConversion cancelled by user.", file=sys.stderr)
        sys.exit(130)
    
    except Exception as e:
        print(f"Error: Unexpected error: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)
    
    finally:
        # Clean up temporary DXF file
        if temp_dxf_path:
            if args.verbose:
                print("\nCleaning up temporary files...")
            cleanup_temp_dxf(temp_dxf_path)


if __name__ == "__main__":
    main()
