import sys

from systemrdl.node import AddrmapNode, RegNode


def check_overlapping_fields(node: AddrmapNode) -> list[str]:
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


def run(node: AddrmapNode) -> int:
    """Run all tidy checks on the elaborated node. Returns exit code."""
    problems = check_overlapping_fields(node)
    if problems:
        for p in problems:
            print(f"error: {p}")
        return 1
    return 0
