#!/usr/bin/env python3
"""Zero-dependency, no-network environment report for Ubuntu VPS acceptance.

Avoids printing user names, full home paths, IP addresses, tokens or process arguments.
"""
from __future__ import annotations
import argparse
import importlib.metadata
import json
import os
import platform
import shutil
import sys
from pathlib import Path


def _meminfo() -> dict[str, int | None]:
    values: dict[str, int] = {}
    try:
        for line in Path("/proc/meminfo").read_text(encoding="utf-8").splitlines():
            key, _, rest = line.partition(":")
            if key in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree"):
                values[key] = int(rest.strip().split()[0]) * 1024
    except (OSError, ValueError, IndexError):
        pass
    return {key: values.get(key) for key in ("MemTotal", "MemAvailable", "SwapTotal", "SwapFree")}


def _cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text(encoding="utf-8").splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def report() -> dict:
    disk = shutil.disk_usage(Path.cwd())
    packages = ("Pillow", "PyMuPDF", "reportlab", "python-docx", "requests", "streamlit", "pytest", "optimum-intel")
    versions = {}
    for package in packages:
        try:
            versions[package] = importlib.metadata.version(package)
        except importlib.metadata.PackageNotFoundError:
            versions[package] = None
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "cpu_model": _cpu_model(),
        "logical_cpu_count": os.cpu_count(),
        "memory_bytes": _meminfo(),
        "working_directory_disk_bytes": {"total": disk.total, "free": disk.free},
        "packages": versions,
        "notes": [
            "Diagnostic only: no neural model is downloaded or executed.",
            "Package availability and system capacity do not guarantee successful CPU diffusion.",
            "No username, IP address, environment secrets or source files are included.",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Story2KDP read-only VPS diagnostics")
    parser.add_argument("--json", action="store_true", help="machine-readable report")
    args = parser.parse_args()
    data = report()
    print(json.dumps(data, indent=2) if args.json else json.dumps(data, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
