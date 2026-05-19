"""MAJIC eval-dace CLI shim.

This file used to aggregate the upstream HuggingFace-based method modules,
which depend on local GPU inference and are not compatible with the
eval-dace API-only pipeline. We leave those modules in place as research
artifacts and expose the new runnable adapter instead.

Running ``python3 majic.py`` (or ``python3 -m majic_eval``) is equivalent
to ``python3 -m majic_eval.runner``.
"""

from majic_eval.runner import main


if __name__ == "__main__":
    main()
