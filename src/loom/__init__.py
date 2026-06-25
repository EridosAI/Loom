"""loom — shared, validated primitives for the Loom associative-memory program.

These modules are ported from the isolation rigs (exp01 pooling substrate, exp03
order-as-content) and grow as experiments are integrated. Stage-0 fuses them in one loop.
"""

from . import completion, order, poolmetrics, pooling, spread

__all__ = ["pooling", "poolmetrics", "order", "completion", "spread"]
