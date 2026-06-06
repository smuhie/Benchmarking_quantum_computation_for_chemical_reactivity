"""Generate Figure 1: reaction-observable benchmarks.

This script was derived from the original notebook:
notebooks/Benchmarking_quantum_computation_for_chemical_reactivity.ipynb
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg", force=True)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Figure 1 | From internal metrics to reaction decisions

# - single conceptual panel
# - left/right conceptual framing
# - right-side shaded reaction-observable region
# - decision-relevant zone banner
# - bottom consequence axis


import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Circle, Rectangle

# -----------------------
# Global style
# -----------------------
plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "font.size": 16,
    "pdf.fonttype": 42,
    "ps.fonttype": 42
})

# Large source figure, designed with 50% reduction in mind.
# If reduced by 50%, final width is ~8.4 inches and smallest text is ~8 pt.
fig = plt.figure(figsize=(14.8, 9.8), dpi=600, facecolor="white")
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis("off")

# -----------------------
# Palette
# -----------------------
dark = "#111111"
mid = "#666666"
soft_mid = "#7b7b7b"

gray_fill = "#efefef"
gray_edge = "#444444"

left_zone_fill = "#fbfbfb"

blue_fill = "#dfe9f6"
blue_edge = "#6e93bc"
blue_dark = "#567ea9"
right_zone_fill = "#ecf4fb"
right_zone_banner = "#d7e8f8"
divider_blue = "#c7d8e8"

# -----------------------
# Geometry controls
# -----------------------
axis_x0 = 0.10
axis_x1 = 0.94
axis_y = 0.14

panel_y = 0.12
panel_h = 0.70
panel_top = panel_y + panel_h

# Blue boundary/divider.
# The Rate tick is placed exactly at this x-coordinate.
thr_x = 0.555

# Proportional mapping for all right-side elements.
# This starts from the original code's right-side geometry:
# old Rate/boundary = 0.60, old right edge = 0.94.
old_rate_x = 0.60
old_right_edge = 0.94

new_rate_x = thr_x - 0.018
new_right_edge = axis_x1

right_scale = (new_right_edge - new_rate_x) / (old_right_edge - old_rate_x)

def rx(x_old):
    """Map old right-side x-coordinate to new proportional right-side coordinate."""
    return new_rate_x + (x_old - old_rate_x) * right_scale

# Coordinated right-side positions, mapped proportionally from the supplied code.
q_form_x = rx(0.690)
rx_obs_x = rx(0.725)
rx_dec_x = rx(0.765)

# Separate label columns prevent overlap with the decision circle while preserving proportional placement.
obs_label_x = rx(0.830)
decision_label_x = rx(0.850)

# Banner mapped proportionally.
banner_x = rx(0.635)
banner_right = rx(0.910)
banner_w = banner_right - banner_x
banner_center_x = banner_x + banner_w / 2

# Header centered over the new right-side zone.
right_header_x = (thr_x + axis_x1) / 2

# Bottom-axis ticks.
tick_energy = 0.15
tick_barrier = 0.28
tick_free_energy = 0.41

# Critical correction: Rate tick exactly at the blue boundary (to the left of the boundary).
tick_rate = thr_x + 0.013

# Right-side ticks moved proportionally with the right-side geometry.
tick_selectivity = rx(0.700)
tick_mechanism = rx(0.800)
tick_decision = rx(0.900)

# -----------------------
# No internal title
# -----------------------
# The formal title belongs in the caption:
# Figure 1 | From internal metrics to reaction decisions.

# -----------------------
# Background zones
# -----------------------
# Left side: internal-metric framing
ax.add_patch(Rectangle(
    (0.10, panel_y),
    thr_x - 0.10,
    panel_h,
    facecolor=left_zone_fill,
    edgecolor="none",
    zorder=0.15
))

# Right side: reaction-observable framing
ax.add_patch(Rectangle(
    (thr_x, panel_y),
    axis_x1 - thr_x,
    panel_h,
    facecolor=right_zone_fill,
    edgecolor="none",
    zorder=0.15
))

# Blue divider
ax.plot(
    [thr_x, thr_x],
    [panel_y, panel_top],
    color=divider_blue,
    lw=1.6,
    zorder=1
)

# -----------------------
# Section headers
# -----------------------
ax.text(
    0.22, 0.84,
    "Internal-metric framing",
    ha="center",
    va="center",
    fontsize=24,
    fontweight="bold",
    color=dark
)

ax.text(
    right_header_x, 0.84,
    "Reaction-observable framing",
    ha="center",
    va="center",
    fontsize=24,
    fontweight="bold",
    color=dark
)

# -----------------------
# Decision-relevant zone banner
# -----------------------
ax.add_patch(Rectangle(
    (banner_x, 0.765),
    banner_w,
    0.052,
    facecolor=right_zone_banner,
    edgecolor=blue_edge,
    linewidth=1.2,
    zorder=1.8
))

ax.text(
    banner_center_x, 0.791,
    "Decision-relevant zone",
    ha="center",
    va="center",
    fontsize=20,
    fontweight="bold",
    color=dark,
    zorder=2
)

# Short cue label only, not explanatory prose
ax.text(
    thr_x - 0.018,
    0.705,
    "decision-level effect",
    ha="right",
    va="center",
    fontsize=17,
    color=mid,
    linespacing=1.0,
    zorder=2
)

ax.add_patch(FancyArrowPatch(
    (thr_x - 0.012, 0.705),
    (thr_x + 0.014, 0.705),
    arrowstyle='-|>',
    mutation_scale=14,
    lw=1.2,
    color=mid,
    zorder=2
))

# -----------------------
# Internal-metric trajectory
# -----------------------
left_nodes = [
    (0.20, 0.68, "Quantum\nalgorithm"),
    (0.21, 0.50, "Isolated\nmolecular\nenergy"),
    (0.20, 0.32, "Internal\nmetric"),
]

left_r = 0.064

for i, (cx, cy, txt) in enumerate(left_nodes):
    ax.add_patch(Circle(
        (cx, cy),
        left_r,
        facecolor=gray_fill,
        edgecolor=gray_edge,
        linewidth=1.35,
        zorder=3
    ))

    ax.text(
        cx,
        cy,
        txt,
        ha="center",
        va="center",
        fontsize=18,
        color=dark,
        linespacing=0.95,
        zorder=4
    )

    if i < len(left_nodes) - 1:
        nx, ny = left_nodes[i + 1][0], left_nodes[i + 1][1]
        ax.add_patch(FancyArrowPatch(
            (cx, cy - left_r - 0.008),
            (nx, ny + left_r + 0.008),
            arrowstyle='-|>',
            mutation_scale=15,
            lw=1.35,
            color=gray_edge,
            zorder=3
        ))

# Internal-metric loop cue
ax.add_patch(FancyArrowPatch(
    (0.145, 0.300),
    (0.145, 0.705),
    connectionstyle="arc3,rad=-0.45",
    arrowstyle='-|>',
    mutation_scale=13,
    lw=1.1,
    color=soft_mid,
    zorder=2
))

# Left-side internal metric labels
ax.text(
    0.300,
    0.500,
    "molecular energy error\ncircuit depth\nscaling \nfidelity",
    ha="left",
    va="center",
    fontsize=17,
    color=mid,
    linespacing=1.5
)

# Short left-side endpoint label
ax.text(
    0.220,
    0.230,
    "internal computational\nendpoints",
    ha="center",
    va="center",
    fontsize=16,
    color=mid,
    linespacing=0.98
)

ax.add_patch(FancyArrowPatch(
    (0.257, 0.292),
    (0.232, 0.178),
    arrowstyle='-|>',
    mutation_scale=12.5,
    lw=1.0,
    color=soft_mid,
    zorder=2
))

# -----------------------
# Reaction-observable trajectory
# -----------------------
right_nodes = [
    (q_form_x, 0.68, "Quantum\nformulation", gray_fill, gray_edge, 18, False, 0.070),
    (rx_obs_x, 0.50, "Reaction\nobservable", blue_fill, blue_dark, 20, True, 0.080),
    (rx_dec_x, 0.29, "Reaction\ndecision", gray_fill, gray_edge, 19, True, 0.080),
]

for i, (cx, cy, txt, fc, ec, fs, bold, r) in enumerate(right_nodes):
    ax.add_patch(Circle(
        (cx, cy),
        r,
        facecolor=fc,
        edgecolor=ec,
        linewidth=1.8 if i == 1 else 1.35,
        zorder=3
    ))

    ax.text(
        cx,
        cy,
        txt,
        ha="center",
        va="center",
        fontsize=fs,
        fontweight="bold" if bold else "normal",
        color=dark,
        linespacing=0.95,
        zorder=4
    )

    if i < len(right_nodes) - 1:
        nx, ny = right_nodes[i + 1][0], right_nodes[i + 1][1]
        next_r = right_nodes[i + 1][7]
        ax.add_patch(FancyArrowPatch(
            (cx, cy - r - 0.006),
            (nx, ny + next_r + 0.006),
            connectionstyle="arc3,rad=-0.08",
            arrowstyle='-|>',
            mutation_scale=16,
            lw=1.6 if i == 0 else 1.75,
            color=blue_dark if i == 0 else blue_edge,
            zorder=2.6
        ))

# -----------------------
# Right-side annotation labels
# Split into compact groups to preserve >=16 pt readability after 50% reduction.
# -----------------------

# Reaction-observable labels, upper group
ax.text(
    obs_label_x - 0.06,
    0.680,
    "barriers\ntransition-state energetics\nrates\nselectivity trends\nsolvent shifts",
    ha="left",
    va="center",
    fontsize=16,
    color=mid,
    linespacing=1.3
)

# Reaction-observable labels, lower group
ax.text(
    obs_label_x - 0.02,
    0.500,
    "catalytic-step ordering\nbranching ratios\nquantum yields\nproduct-channel distributions",
    ha="left",
    va="center",
    fontsize=16,
    color=mid,
    linespacing=1.3
)

# Reaction-decision labels
ax.text(
    # decision_label_x,
    obs_label_x + 0.03,
    0.300,
    "mechanism ranking\ndominant-pathway assignment\ncatalyst choice\nselectivity assignment\nproduct-channel assignment",
    ha="left",
    va="center",
    fontsize=16,
    color=mid,
    linespacing=1.3
)

# -----------------------
# Shared consequence axis
# -----------------------
ax.plot(
    [axis_x0, axis_x1],
    [axis_y, axis_y],
    color=dark,
    lw=1.6,
    zorder=2
)

ax.add_patch(FancyArrowPatch(
    (axis_x1 - 0.015, axis_y),
    (axis_x1, axis_y),
    arrowstyle='-|>',
    mutation_scale=15,
    lw=1.6,
    color=dark,
    zorder=2
))

ticks = [
    (tick_energy, "Energy"),
    (tick_barrier, "Barrier"),
    (tick_free_energy, "Free-energy\nbarrier"),
    (tick_rate, "Rate"),
    (tick_selectivity, "Selectivity"),
    (tick_mechanism, "Mechanism"),
    (tick_decision, "Decision"),
]

for tx, lab in ticks:
    ax.plot(
        [tx, tx],
        [axis_y, axis_y + 0.016],
        color=dark,
        lw=1.1,
        zorder=2
    )

    ax.text(
        tx,
        axis_y + 0.022,
        lab,
        ha="center",
        va="bottom",
        fontsize=16,
        fontweight="bold" if lab in ["Selectivity", "Mechanism", "Decision"] else "normal",
        color=dark,
        linespacing=0.95,
        zorder=3
    )

ax.text(
    0.53,
    0.085,
    "Increasing chemical consequence",
    ha="center",
    va="center",
    fontsize=22,
    fontweight="bold",
    color=dark
)

# -----------------------
# Links from right side to consequence axis
# -----------------------
# Observable -> updated selectivity tick
ax.add_patch(FancyArrowPatch(
    (rx_obs_x - 0.020, 0.450),
    (tick_selectivity, axis_y + 0.042),
    connectionstyle="arc3,rad=0.24",
    arrowstyle='-|>',
    mutation_scale=13,
    lw=1.15,
    color=blue_edge,
    zorder=2
))

# Decision -> updated decision tick
ax.add_patch(FancyArrowPatch(
    (rx_dec_x + 0.070, 0.253),
    (tick_decision, axis_y + 0.048),
    connectionstyle="arc3,rad=-0.04",
    arrowstyle='-|>',
    mutation_scale=15,
    lw=1.35,
    color=blue_edge,
    zorder=2
))

# -----------------------
# No explanatory footer
# Caption carries this idea:
# Useful accuracy begins when a propagated quantum contribution changes or stabilizes
# a reaction-level conclusion, or rules out a previously plausible alternative.
# -----------------------

# -----------------------
# Export
# -----------------------
plt.savefig(
    OUTPUT_DIR / "Figure1_reaction_observable_benchmarks.pdf",
    bbox_inches="tight",
    facecolor="white"
)

plt.savefig(
    OUTPUT_DIR / "Figure1_reaction_observable_benchmarks.png",
    dpi=600,
    bbox_inches="tight",
    facecolor="white"
)

plt.close(fig)