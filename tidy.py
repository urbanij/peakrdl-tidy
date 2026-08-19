import argparse
import sys
from pathlib import Path
from systemrdl import RDLCompiler
from systemrdl.messages import RDLCompileError
from systemrdl import warnings
from systemrdl.node import RegNode

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


def check_overlapping_fields(node):
    """Report fields within a register that share bit positions."""
    problems = []
    for reg in node.descendants(unroll=True):
        if not isinstance(reg, RegNode):
            continue
        fields = sorted(reg.fields(), key=lambda f: f.low)
        for i, a in enumerate(fields):
            for b in fields[i + 1:]:
                if a.high >= b.low and b.high >= a.low:
                    problems.append(
                        f"{reg.get_path()}: fields '{a.get_path()}' "
                        f"[{a.high}:{a.low}] and '{b.get_path()}' "
                        f"[{b.high}:{b.low}] overlap"
                    )
    return problems


problems = check_overlapping_fields(root)
if problems:
    for p in problems:
        print(f"warning: {p}")
    sys.exit(1)
