"""Utility functions for file handling and performance metrics."""

import os
import time
from enum import Enum
from typing import Dict
from pathlib import Path


class FileType(Enum):
    """Supported input file types."""
    DXF = "dxf"
    DWG = "dwg"


def detect_file_type(filepath: str) -> FileType:
    """
    Detect file type based on extension.
    
    Args:
        filepath: Path to input file
        
    Returns:
        FileType enum (DXF or DWG)
        
    Raises:
        ValueError: If file extension is not .dxf or .dwg
    """
    ext = Path(filepath).suffix.lower()
    
    if ext == ".dxf":
        return FileType.DXF
    elif ext == ".dwg":
        return FileType.DWG
    else:
        raise ValueError(f"Unsupported file format: {ext}. Only .dxf and .dwg files are supported.")


def resolve_output_path(input_path: str, output_path: str = None) -> str:
    """
    Resolve output file path.
    
    Args:
        input_path: Input file path
        output_path: Optional output path from -o flag
        
    Returns:
        Resolved output path with .svg extension
    """
    if output_path:
        return output_path
    
    # Default: same directory as input with .svg extension
    input_file = Path(input_path)
    return str(input_file.with_suffix(".svg"))


class PerformanceMetrics:
    """Track and format performance metrics."""
    
    def __init__(self):
        self.stages: Dict[str, float] = {}
        self._start_times: Dict[str, float] = {}
    
    def start_stage(self, stage_name: str):
        """Start timing a stage."""
        self._start_times[stage_name] = time.perf_counter()
    
    def end_stage(self, stage_name: str):
        """End timing a stage and record duration."""
        if stage_name in self._start_times:
            elapsed = time.perf_counter() - self._start_times[stage_name]
            self.stages[stage_name] = elapsed
            del self._start_times[stage_name]
    
    def get_total_time(self) -> float:
        """Get total elapsed time across all stages."""
        return sum(self.stages.values())
    
    def format_metrics(self) -> str:
        """Format metrics for display."""
        lines = ["Performance Metrics:", "=" * 40]
        
        for stage, duration in self.stages.items():
            lines.append(f"{stage:<25} {duration:>10.4f}s")
        
        lines.append("-" * 40)
        lines.append(f"{'Total':<25} {self.get_total_time():>10.4f}s")
        
        return "\n".join(lines)
