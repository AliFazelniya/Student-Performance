# plot_utils.py
# Helper for notebooks: save all matplotlib figures when the kernel ends.
from pathlib import Path
import matplotlib.pyplot as plt
import atexit
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = PROJECT_ROOT / "reports" / "plots"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def slugify(text: str) -> str:
    text = text.strip().lower()
    text = re.sub(r"\s+", "_", text)
    text = re.sub(r"[^\w\-۰-۹ا-ی_]", "", text)
    return text if text else "figure"


def save_all_figs(title) -> None:
    for i in plt.get_fignums():
        fig = plt.figure(i)
        axes = fig.get_axes()
        filename = slugify(title) + ".png"
        fig.savefig(OUT_DIR / filename, dpi=300, bbox_inches="tight")
    print(f"All figures saved in {OUT_DIR}")
