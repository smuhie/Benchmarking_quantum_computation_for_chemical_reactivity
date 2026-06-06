"""Generate all manuscript figures.

Run from the repository root:
    python generate_all_figures.py

The output files are written to the figures/ directory.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    ROOT / "src" / "figure1.py",
    ROOT / "src" / "figure2.py",
    ROOT / "src" / "figure3.py",
    ROOT / "src" / "figure4.py",
]


def main() -> None:
    for script in SCRIPTS:
        print(f"Generating {script.name}...")
        subprocess.run([sys.executable, str(script)], check=True, cwd=str(ROOT))
    print("Done. Figure files are in:", ROOT / "figures")


if __name__ == "__main__":
    main()
