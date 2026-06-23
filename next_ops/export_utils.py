"""Utility functions for saving local report exports."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path


def ensure_output_dir(output_dir: str = "outputs") -> Path:
    """Create and return the output directory path."""
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    return path


def generate_report_filename(prefix: str, extension: str) -> str:
    """Return a timestamped report filename using the provided extension."""
    clean_extension = extension.strip().lstrip(".")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{clean_extension}"


def save_text_report(
    content: str,
    filename_prefix: str,
    extension: str,
    output_dir: str = "outputs",
) -> Path:
    """Save text report content as UTF-8 and return the written path."""
    directory = ensure_output_dir(output_dir)
    filename = generate_report_filename(filename_prefix, extension)
    report_path = directory / filename
    report_path.write_text(content, encoding="utf-8")
    return report_path
