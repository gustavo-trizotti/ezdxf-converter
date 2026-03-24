"""DWG file handling via ODA File Converter."""

import os
import tempfile
import subprocess
from pathlib import Path
from typing import Optional


class ODAConverterError(Exception):
    """Exception raised when ODA File Converter operations fail."""
    pass


def get_oda_path(oda_flag: Optional[str] = None) -> str:
    """
    Get ODA File Converter executable path.
    
    Args:
        oda_flag: Path from --oda-path flag
        
    Returns:
        Path to ODA File Converter executable
        
    Raises:
        ODAConverterError: If ODA path not found or specified
    """
    if oda_flag:
        if os.path.isfile(oda_flag):
            return oda_flag
        raise ODAConverterError(f"ODA File Converter not found at: {oda_flag}")
    
    env_path = os.environ.get("ODA_FILE_CONVERTER")
    if env_path:
        if os.path.isfile(env_path):
            return env_path
        raise ODAConverterError(f"ODA File Converter not found at: {env_path} (from ODA_FILE_CONVERTER env var)")
    
    raise ODAConverterError(
        "ODA File Converter path not specified. Please either:\n"
        "  1. Use --oda-path flag to specify the path, or\n"
        "  2. Set ODA_FILE_CONVERTER environment variable\n"
        "Example: --oda-path \"C:\\Program Files\\ODA\\ODAFileConverter.exe\""
    )


def convert_dwg_to_dxf(dwg_path: str, oda_path: str) -> str:
    """
    Convert DWG file to DXF using ODA File Converter.
    
    Args:
        dwg_path: Path to input DWG file
        oda_path: Path to ODA File Converter executable
        
    Returns:
        Path to converted DXF file in temporary directory
        
    Raises:
        ODAConverterError: If conversion fails
    """
    dwg_file = Path(dwg_path)
    
    if not dwg_file.exists():
        raise ODAConverterError(f"DWG file not found: {dwg_path}")
    
    # Create temp directory for conversion
    temp_dir = tempfile.mkdtemp(prefix="ezdxf_convert_")
    output_dir = Path(temp_dir)
    
    try:
        # ODA File Converter command line format:
        # ODAFileConverter "input_folder" "output_folder" "ACAD_version" "output_type" "recurse" "audit"
        # We use ACAD2018 (R2018) DXF format for best compatibility
        
        input_dir = str(dwg_file.parent.absolute())
        output_path = str(output_dir.absolute())
        
        cmd = [
            oda_path,
            input_dir,
            output_path,
            "ACAD2018",  # Output version
            "DXF",       # Output format
            "0",         # Don't recurse subdirectories
            "1"          # Audit and recover
        ]
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout
        )
        
        if result.returncode != 0:
            raise ODAConverterError(
                f"ODA File Converter failed with return code {result.returncode}\n"
                f"Error: {result.stderr}"
            )
        
        # Find the converted DXF file
        dxf_filename = dwg_file.stem + ".dxf"
        converted_dxf = output_dir / dxf_filename
        
        if not converted_dxf.exists():
            raise ODAConverterError(
                f"Conversion appeared to succeed but output file not found: {converted_dxf}"
            )
        
        return str(converted_dxf)
        
    except subprocess.TimeoutExpired:
        raise ODAConverterError("ODA File Converter timed out after 5 minutes")
    except Exception as e:
        # Clean up temp directory on failure
        import shutil
        try:
            shutil.rmtree(temp_dir, ignore_errors=True)
        except:
            pass
        raise


def cleanup_temp_dxf(dxf_path: str):
    """
    Clean up temporary DXF file and its directory.
    
    Args:
        dxf_path: Path to temporary DXF file
    """
    import shutil
    try:
        dxf_file = Path(dxf_path)
        temp_dir = dxf_file.parent
        
        # Only delete if it's in a temp directory (safety check)
        if "ezdxf_convert_" in str(temp_dir):
            shutil.rmtree(temp_dir, ignore_errors=True)
    except Exception:
        pass  # Silent cleanup failure
