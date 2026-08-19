#!/usr/bin/env python3
"""Standalone entry point — run the tidy checks without the PeakRDL CLI.

Usage: python tidy.py <file.rdl> [<file2.rdl> ...]

For the full PeakRDL CLI experience, install with the [cli] extra and run:
    peakrdl tidy <file.rdl>
"""
import argparse
import sys
from pathlib import Path

from systemrdl import RDLCompiler
from systemrdl import warnings
from systemrdl.messages import RDLCompileError

from peakrdl_tidy.tidy import run

parser = argparse.ArgumentParser(description="Validate SystemRDL source files.")
parser.add_argument(
    "files",
    nargs="+",
    type=Path,
    help="SystemRDL source files",
)
args = parser.parse_args()

rdlc = RDLCompiler(warning_flags=warnings.ALL)
try:
    for file in args.files:
        rdlc.compile_file(file)
    root = rdlc.elaborate()
except RDLCompileError:
    print("RDL validation failed")
    raise

sys.exit(run(root))
