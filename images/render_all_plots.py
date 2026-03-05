"""
images/render_all_plots.py
──────────────────────────
Pre-render script called by _quarto.yml before the site is built.

    project:
      pre-render: python images/render_all_plots.py

What it does
────────────
1. Finds every .py file in the images/ directory whose name is NOT this script
   and NOT a utility (rename_biases.py, etc.).
2. Executes each one inside a clean matplotlib context so it cannot accidentally
   share state with the next script.
3. Intercepts plt.show() — instead of opening a window it saves a .png next to
   the .py file with the same stem (e.g. gamblers-fallacy.py → gamblers-fallacy.png).
4. Skips regeneration if the .png is newer than the .py (incremental builds).
5. Prints a tidy summary so you can see what happened during `quarto render`.

How to write a plot script so this works
─────────────────────────────────────────
Your existing scripts (gamblers-fallacy.py, hot-hand-fallacy.py,
extrapolation-bias.py) already end with plt.show() or just draw to the current
figure. This script replaces plt.show() before execution, so no changes to those
files are needed.

The only rule: each script must produce exactly one figure (or the last active
figure is saved). If a script creates multiple figures, all of them are saved as
<stem>-0.png, <stem>-1.png, etc.
"""

import importlib
import os
import sys
import traceback
from pathlib import Path
from unittest.mock import patch

import matplotlib
matplotlib.use("Agg")          # non-interactive backend — no GUI window needed
import matplotlib.pyplot as plt


# ── Configuration ─────────────────────────────────────────────────────────────

IMAGES_DIR = Path(__file__).parent          # same folder as this script
SKIP_FILES = {
    "render_all_plots.py",                  # this script itself
    "rename_biases.py",                     # utility, not a plot
}
DPI = 150                                   # output resolution
OUTPUT_FORMAT = "png"


# ── Helpers ───────────────────────────────────────────────────────────────────

def _is_stale(py_path: Path, png_path: Path) -> bool:
    """Return True if the PNG does not exist or is older than the Python file."""
    return not png_path.exists() or py_path.stat().st_mtime > png_path.stat().st_mtime


def _save_current_figures(stem: str) -> list[Path]:
    """Save all open matplotlib figures and return their paths."""
    figs = [plt.figure(n) for n in plt.get_fignums()]
    saved = []
    for i, fig in enumerate(figs):
        if len(figs) == 1:
            out = IMAGES_DIR / f"{stem}.{OUTPUT_FORMAT}"
        else:
            out = IMAGES_DIR / f"{stem}-{i}.{OUTPUT_FORMAT}"
        fig.savefig(out, dpi=DPI, bbox_inches="tight")
        saved.append(out)
    return saved


def run_script(py_path: Path) -> list[Path]:
    """
    Execute a plot script in an isolated namespace with plt.show() patched.
    Returns a list of saved PNG paths.
    """
    stem = py_path.stem
    plt.close("all")                        # clean slate for this script

    # Read source and compile
    source = py_path.read_text(encoding="utf-8")

    # Patch plt.show to a no-op so scripts don't block waiting for a window
    with patch.object(plt, "show", lambda *a, **kw: None):
        namespace = {
            "__file__": str(py_path),
            "__name__": "__main__",
        }
        # Add the images/ dir to sys.path in case a script does local imports
        sys.path.insert(0, str(IMAGES_DIR))
        try:
            exec(compile(source, str(py_path), "exec"), namespace)  # noqa: S102
        finally:
            sys.path.pop(0)

    return _save_current_figures(stem)


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    plot_scripts = sorted(
        p for p in IMAGES_DIR.glob("*.py")
        if p.name not in SKIP_FILES
    )

    if not plot_scripts:
        print("[render_all_plots] No plot scripts found — nothing to do.")
        return

    print(f"[render_all_plots] Found {len(plot_scripts)} plot script(s) in {IMAGES_DIR}")
    print()

    results = {"saved": [], "skipped": [], "errors": []}

    for py_path in plot_scripts:
        stem = py_path.stem
        expected_png = IMAGES_DIR / f"{stem}.{OUTPUT_FORMAT}"

        if not _is_stale(py_path, expected_png):
            print(f"  ⏭  SKIP   {py_path.name}  (PNG up-to-date)")
            results["skipped"].append(py_path.name)
            continue

        print(f"  ⚙  RENDER {py_path.name} ...", end=" ", flush=True)
        try:
            saved = run_script(py_path)
            for p in saved:
                print(f"\n         → {p.name}", end="")
            print()
            results["saved"].extend(saved)
        except Exception:                   # noqa: BLE001
            print("FAILED")
            traceback.print_exc()
            results["errors"].append(py_path.name)
        finally:
            plt.close("all")

    # ── Summary ───────────────────────────────────────────────────────────────
    print()
    print("─" * 50)
    print(f"[render_all_plots] Done.")
    print(f"  Rendered : {len(results['saved'])} file(s)")
    print(f"  Skipped  : {len(results['skipped'])} file(s)")
    if results["errors"]:
        print(f"  ERRORS   : {len(results['errors'])} file(s): {', '.join(results['errors'])}")
        sys.exit(1)          # non-zero exit causes `quarto render` to abort with a clear message
    print()


if __name__ == "__main__":
    main()