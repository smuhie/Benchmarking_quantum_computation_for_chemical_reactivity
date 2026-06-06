"""Generate Figure 3: evidence-audited maturity map.

This script was derived from the original notebook:
notebooks/Benchmarking_quantum_computation_for_chemical_reactivity.ipynb
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg", force=True)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure 3
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "Helvetica", "DejaVu Sans"]

fig = plt.figure(figsize=(18, 10), dpi=240)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

dark = "#111111"
mid = "#555555"
grid = "#6a6a6a"
soft = "#9a9a9a"
dominant = "#b9c4d4"
adjacent = "#e5ebf3"
group_fill = "#f7f7f7"
warning_fill = "#fff5ec"
warning_edge = "#9a5823"

group_x = 0.020
group_w = 0.145
label_x = 0.168

grid_x = 0.385
grid_y = 0.195
grid_h = 0.550
timeline_w = 0.450
gap_w = 0.017
warn_w = 0.085
warn_x = grid_x + timeline_w + gap_w

matrix_left = grid_x
matrix_right = warn_x + warn_w
matrix_center = (matrix_left + matrix_right) / 2

ax.text(
    matrix_center, 0.960,
    "Evidence-audited maturity map",
    ha="center", va="center",
    fontsize=21.5, fontweight="bold", color=mid
)

ax.text(
    matrix_center, 0.905,
    "Maturity reflects evidence for quantum endpoint claims, not chemical importance.",
    ha="center", va="center",
    fontsize=17.0, fontweight="medium", color=mid
)

row_labels = [
    "Barrier heights",
    "Transition states",
    "Rate constants",
    "Selectivity and branching",
    "Solvation and environment",
    "Catalytic mechanism \ndiscrimination",
    "Nonadiabatic dynamics",
    "Open-system \nreaction dynamics",
]
n_rows = len(row_labels)
row_h = grid_h / n_rows

timeline_cols = [
    "Localized/embedded\nproof-of-principle",
    "Plausible early\nfault-tolerant\ntargets",
    "Longer-term\ndirections",
]
col_ws = np.array([0.34, 0.34, 0.32])
col_ws = col_ws / col_ws.sum() * timeline_w

groups = [
    ("Localized\nobservables", 0, 1),
    ("Reaction-level\ninference", 2, 3),
    ("Environment-coupled\nand dynamical\nendpoints", 4, 7),
]

for g_label, r0, r1 in groups:
    y_top = grid_y + grid_h - r0 * row_h
    y_bot = grid_y + grid_h - (r1 + 1) * row_h
    ax.add_patch(
        Rectangle(
            (group_x + 0.036, y_bot),
            group_w,
            y_top - y_bot,
            facecolor=group_fill,
            edgecolor="none",
            zorder=0.1,
        )
    )
    ax.text(
        group_x + group_w / 1.33,
        (y_top + y_bot) / 2,
        g_label,
        ha="center", va="center",
        fontsize=17.0, fontweight="bold",
        color=mid, linespacing=1.3,
    )

header_y = grid_y + grid_h + 0.055

cx = grid_x
for w, lab in zip(col_ws, timeline_cols):
    ax.text(
        cx + w / 2,
        header_y,
        lab,
        ha="center", va="center",
        fontsize=17.6, fontweight="black",
        color=mid, linespacing=1.3,
    )
    cx += w

ax.text(
    warn_x + warn_w / 2,
    header_y + 0.001,
    "Caution:\noverclaim risk",
    ha="center", va="center",
    fontsize=17.0, fontweight="bold",
    color=warning_edge, linespacing=1.3,
)

# Move row-label anchor closer to the matrix and right-align labels
label_x = grid_x - 0.018

for r, lab in enumerate(row_labels):
    y = grid_y + grid_h - (r + 0.5) * row_h
    ax.text(
        label_x, y, lab,
        ha="right", va="center",
        fontsize=17.4, color=dark,
    )
# for r, lab in enumerate(row_labels):
#     y = grid_y + grid_h - (r + 0.5) * row_h
#     ax.text(
#         label_x, y, lab,
#         ha="left", va="center",
#         fontsize=17.6, color=dark,
#     )

def timeline_cell(c, r, inset=0.0):
    x0 = grid_x + np.sum(col_ws[:c]) + inset
    y0 = grid_y + grid_h - (r + 1) * row_h + inset
    w = col_ws[c] - 2 * inset
    h = row_h - 2 * inset
    return x0, y0, w, h

def warning_cell(r, inset=0.010):
    x0 = warn_x + inset
    y0 = grid_y + grid_h - (r + 1) * row_h + inset
    w = warn_w - 2 * inset
    h = row_h - 2 * inset
    return x0, y0, w, h

dominant_cells = [
    (0, 0),
    (0, 1),
    (1, 2),
    (1, 3),
    (1, 4),
    (1, 5),
    (2, 6),
    (2, 7),
]

adjacent_cells = [
    (1, 0),
    (1, 1),
    (0, 2),
    (0, 3),
    (2, 4),
    (2, 5),
    (1, 6),
]

warning_rows = [3, 7]

for c, r in adjacent_cells:
    x0, y0, w, h = timeline_cell(c, r)
    ax.add_patch(
        Rectangle(
            (x0, y0), w, h,
            facecolor=adjacent,
            edgecolor="none",
            zorder=0.35,
        )
    )

for c, r in dominant_cells:
    x0, y0, w, h = timeline_cell(c, r)
    ax.add_patch(
        Rectangle(
            (x0, y0), w, h,
            facecolor=dominant,
            edgecolor="none",
            zorder=0.40,
        )
    )

for r in warning_rows:
    x0, y0, w, h = warning_cell(r)
    ax.add_patch(
        Rectangle(
            (x0, y0), w, h,
            facecolor=warning_fill,
            edgecolor=warning_edge,
            linewidth=1.8,
            zorder=0.80,
        )
    )

ax.add_patch(
    Rectangle(
        (grid_x, grid_y),
        timeline_w,
        grid_h,
        facecolor="none",
        edgecolor=grid,
        linewidth=0.80,
        zorder=2,
    )
)

x_cursor = grid_x
for w in col_ws[:-1]:
    x_cursor += w
    ax.plot(
        [x_cursor, x_cursor],
        [grid_y, grid_y + grid_h],
        color=grid,
        lw=0.65,
        zorder=2,
    )

for r in range(1, n_rows):
    y = grid_y + r * row_h
    ax.plot(
        [grid_x, grid_x + timeline_w],
        [y, y],
        color=grid,
        lw=0.65,
        zorder=2,
    )

ax.add_patch(
    Rectangle(
        (warn_x, grid_y),
        warn_w,
        grid_h,
        facecolor="none",
        edgecolor=grid,
        linewidth=0.75,
        zorder=2,
    )
)

for r in range(1, n_rows):
    y = grid_y + r * row_h
    ax.plot(
        [warn_x, warn_x + warn_w],
        [y, y],
        color=grid,
        lw=0.65,
        zorder=2,
    )

ax.plot(
    [grid_x + timeline_w + gap_w / 2, grid_x + timeline_w + gap_w / 2],
    [grid_y, grid_y + grid_h],
    color=soft,
    lw=0.85,
    linestyle=(0, (2, 3)),
    zorder=1.5,
)

legend_y = 0.130
legend_xs = [0.070, 0.355, 0.630]
legend_labels = [
    "dominant evidence-based placement",
    "adjacent plausible regime",
    "caution / overclaim risk",
]
legend_styles = [
    dict(facecolor=dominant, edgecolor=grid, linewidth=0.70),
    dict(facecolor=adjacent, edgecolor=grid, linewidth=0.70),
    dict(facecolor=warning_fill, edgecolor=warning_edge, linewidth=1.8),
]

for lx, lab, style in zip(legend_xs, legend_labels, legend_styles):
    ax.add_patch(
        Rectangle(
            (lx +0.15, legend_y - 0.014),
            0.027,
            0.027,
            **style,
        )
    )
    ax.text(
        lx + 0.039 + 0.15,
        legend_y,
        lab,
        ha="left", va="center",
        fontsize=16.0,
        color=dark,
    )
# ----------------------------
# Export
# ----------------------------
fig.savefig(OUTPUT_DIR / "Figure3_evidence_audited_maturity_map.pdf",
            bbox_inches="tight", facecolor="white")
fig.savefig(OUTPUT_DIR / "Figure3_evidence_audited_maturity_map.png",
            dpi=600, bbox_inches="tight", facecolor="white")
plt.close(fig)
