"""MAJIC evaluation package adapted for the eval-dace (MAGIC) pipeline.

Upstream reference: MAJIC (AAAI 2026, arXiv:2508.13048).
This package wires the paper's 10-strategy "Disguise Strategy Pool" and
Markov-chain selection/adaptation to the OpenAI-compatible endpoints used by
``eval-dace/OpenRT/run_eval.sh`` (DACE defender + base-attacker + GPT-4o judge).

To avoid double-imports when launched via ``python -m majic_eval.runner``,
we keep ``__init__`` light and expose ``main`` lazily via ``__getattr__``.
"""

__all__ = ["main"]


def __getattr__(name):  # pragma: no cover - thin lazy import
    if name == "main":
        from .runner import main as _main
        return _main
    raise AttributeError(f"module 'majic_eval' has no attribute {name!r}")
