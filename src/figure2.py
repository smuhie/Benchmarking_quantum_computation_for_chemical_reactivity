"""Generate Figure 2: benchmarking funnel and localized quantum leverage.

This script was derived from the original notebook:
notebooks/Benchmarking_quantum_computation_for_chemical_reactivity.ipynb
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg", force=True)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ============================================================
# Figure 2 | Benchmark funnel and localized quantum leverage
# Combined stacked figure:
#   a) Benchmark funnel
#   b) Localized quantum correction inside a classical workflow
#
# Key update:
# - Panel a is proportionally scaled from 16 x 9 to 24 x 13.5.
# - Panel a fonts, line widths, and arrow sizes are kept at 1.5x throughout.
# - Panel b uses the same final 24 x 13.5 footprint.
# - Panel b font sizes are increased proportionally at each text site.
# - Minimum panel b font size is 16 pt.
# - No image is displayed or saved unless export / plt.show() lines are uncommented.
# ============================================================

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Rectangle, Circle, PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D
import matplotlib as mpl
import numpy as np

# ----------------------------
# Vector-friendly settings
# ----------------------------
mpl.rcParams["font.family"] = "DejaVu Sans"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["svg.fonttype"] = "none"

# ----------------------------
# Figure geometry
# ----------------------------
FIG_W = 24.0

# Both panels use the same final physical footprint.
# Panel a is a true proportional expansion of the original 16 x 9 figure:
# 16 x 9 scaled by 1.5 = 24 x 13.5.
#
# Panel b is resized from 24 x 14 to 24 x 13.5.
# This is a slight vertical reduction but keeps the two panels visually balanced.
PANEL_A_W = 24.0
PANEL_A_H = 13.5
PANEL_B_W = 24.0
PANEL_B_H = 15.5

PANEL_GAP = 0.05
FIG_H = PANEL_A_H + PANEL_GAP + PANEL_B_H

fig = plt.figure(figsize=(FIG_W, FIG_H), dpi=600, facecolor="white")

# Panel b occupies the lower 24 x 13.5 slot.
ax_b = fig.add_axes([
    0.0,
    0.0,
    1.0,
    PANEL_B_H / FIG_H
])

# Panel a occupies the upper 24 x 13.5 slot.
ax_a = fig.add_axes([
    0.0,
    (PANEL_B_H + PANEL_GAP) / FIG_H,
    1.0,
    PANEL_A_H / FIG_H
])

for ax in (ax_a, ax_b):
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

# ----------------------------
# Panel a font and scaling helpers
# ----------------------------
MIN_FONT = 16.0

# Panel a must remain a full proportional 1.5x expansion.
A_SCALE = 1.5

def min_font(size):
    return max(float(size), MIN_FONT)

def fs(size):
    return min_font(size)

def fs_a(size):
    return min_font(size * A_SCALE)

def lw_a(width):
    return width * A_SCALE

def ms_a(size):
    return size * A_SCALE

# ============================================================
# PANEL A
# Draft Figure 2 geometry retained and proportionally enlarged
# ============================================================

ax = ax_a

# Palette
dark = "#111111"
mid = "#666666"
subtle = "#d7dde6"
line = "#202020"
stage_gray = "#f3f3f3"
stage_blue1 = "#edf3fb"
stage_blue2 = "#dde8f6"
stage_blue3 = "#c8d9ef"
white = "white"
text = "#252B35"

# Panel label
ax.text(
    0.035, 0.958,
    "a)",
    ha="center", va="center",
    fontsize=fs_a(24), fontweight="bold", color=dark
)

# Title
ax.text(
    0.45, 0.958,
    "Benchmark funnel",
    ha="center", va="center",
    fontsize=fs_a(22), fontweight="bold", color=dark
)

# Top pill
pill_x, pill_y, pill_w, pill_h = 0.345, 0.892, 0.21, 0.052
ax.add_patch(FancyBboxPatch(
    (pill_x, pill_y - pill_h / 2), pill_w, pill_h,
    boxstyle="round,pad=0.008,rounding_size=0.02",
    facecolor=white, edgecolor=line, linewidth=lw_a(1.2), zorder=8
))
ax.text(
    pill_x + pill_w / 2, pill_y,
    "Raw claim",
    ha="center", va="center",
    fontsize=fs_a(18.0), fontweight="bold",
    color=dark, zorder=9
)

# Funnel geometry
y_top = 0.842
y_bottom = 0.235
x_center = 0.46
w_top = 0.47
w_bottom = 0.18

stage_labels = [
    "Reaction question",
    "Target observable",
    "Chemical representation",
    "Endpoint-matched\ncomparator",
    "Quantum role",
    "Uncertainty /\nresource accounting",
    "Decision-level effect",
]

stage_colors = [
    stage_gray,
    stage_gray,
    stage_gray,
    stage_gray,
    stage_blue1,
    stage_blue2,
    stage_blue3,
]

ys = np.linspace(y_top, y_bottom, len(stage_labels) + 1)

def width_at_y_a(y):
    t = (y_top - y) / (y_top - y_bottom)
    return w_top + (w_bottom - w_top) * t

# Outer funnel boundary
left_top = (x_center - w_top / 2, y_top)
right_top = (x_center + w_top / 2, y_top)
left_bottom = (x_center - w_bottom / 2, y_bottom)
right_bottom = (x_center + w_bottom / 2, y_bottom)

verts = [left_top, right_top, right_bottom, left_bottom, left_top]
codes = [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO, Path.CLOSEPOLY]

ax.add_patch(PathPatch(
    Path(verts, codes),
    facecolor="none",
    edgecolor=line,
    linewidth=lw_a(1.35),
    zorder=6
))

# Curved stage patches
for i, label in enumerate(stage_labels):
    y1, y2 = ys[i], ys[i + 1]
    w1, w2 = width_at_y_a(y1), width_at_y_a(y2)
    xl1, xr1 = x_center - w1 / 2, x_center + w1 / 2
    xl2, xr2 = x_center - w2 / 2, x_center + w2 / 2
    sag = 0.010 if i < 4 else 0.008

    verts = [
        (xl1, y1),
        (xr1, y1),
        (xr1 - 0.10 * w1, y1 - sag),
        (x_center + 0.10 * w2, y2 + sag),
        (xr2, y2),
        (xl2, y2),
        (x_center - 0.10 * w2, y2 + sag),
        (xl1 + 0.10 * w1, y1 - sag),
        (xl1, y1),
    ]

    codes = [
        Path.MOVETO, Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
        Path.LINETO,
        Path.CURVE4, Path.CURVE4, Path.CURVE4,
    ]

    ax.add_patch(PathPatch(
        Path(verts, codes),
        facecolor=stage_colors[i],
        edgecolor="none",
        zorder=1
    ))

    if i > 0:
        prev_y = y1
        prev_w = w1
        xl, xr = x_center - prev_w / 2, x_center + prev_w / 2

        ax.add_patch(PathPatch(
            Path(
                [
                    (xl, prev_y),
                    (xl + 0.10 * prev_w, prev_y - sag),
                    (xr - 0.10 * prev_w, prev_y - sag),
                    (xr, prev_y),
                ],
                [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]
            ),
            facecolor="none",
            edgecolor=line,
            linewidth=lw_a(0.95),
            zorder=7
        ))

    y_mid = (y1 + y2) / 2
    base_fs = 18.5 if i < 4 else 19.2
    weight = "bold" if "Decision-level" in label else "normal"

    ax.text(
        x_center, y_mid, label,
        ha="center", va="center",
        fontsize=fs_a(base_fs),
        fontweight=weight,
        color=dark,
        zorder=8,
        linespacing=1.0
    )

# Left-side guide text
ax.text(
    0.12, 0.742,
    "Every credible claim\nmust pass through\nthese benchmark gates",
    ha="center", va="center",
    fontsize=fs_a(16.0),
    fontweight="bold",
    color=text,
    linespacing=1.5
)

# Top arrow
ax.annotate(
    "",
    xy=(x_center, y_top - 0.006),
    xytext=(x_center, pill_y - pill_h / 2 - 0.004),
    arrowprops=dict(
        arrowstyle='-|>',
        lw=lw_a(1.2),
        color=line,
        mutation_scale=ms_a(10)
    )
)

# Right-side callouts
callouts = [
    "mechanism · rate · selectivity\ncatalytic step · nonadiabatic outcome",
    "barrier · free-energy barrier\nrate constant · branching ratio · quantum yield",
    "active space · embedding\nenvironment · dynamical approximation",
    "best classical method\nexperiment where relevant",
    "localized correction\nor endpoint estimator",
    "model choice · truncation · sampling\nstate preparation · observable estimation",
    "changed / stabilized conclusion\nor alternative ruled out",
]

x_line0 = 0.62
x_line1 = 0.67
x_text = 0.695

for i, txt in enumerate(callouts):
    y_mid = (ys[i] + ys[i + 1]) / 2
    ax.plot([x_line0, x_line1], [y_mid, y_mid], color=subtle, lw=lw_a(1.0), zorder=2)
    ax.text(
        x_text, y_mid, txt,
        ha="left", va="center",
        fontsize=fs_a(15),
        color=mid,
        linespacing=1.3
    )


# Bottom statement box
box_x, box_y, box_w, box_h = 0.05, 0.100, 0.75, 0.210

box_top = box_y + box_h / 2
new_box_h = 0.075
new_box_y0 = box_top - new_box_h

ax.add_patch(FancyBboxPatch(
    (box_x, new_box_y0), box_w, new_box_h,
    boxstyle="round,pad=0.008,rounding_size=0.018",
    fc="#FAFAFA",
    ec="#C9C9C9",
    lw=1.0,
    #facecolor=white,
    #edgecolor=line,
    #linewidth=lw_a(0.6),
    zorder=5
))

ax.text(
    box_x + box_w / 2,
    box_y + 0.080,
    "Internal improvements are enabling evidence unless propagated to the reaction observable.",
    ha="center", va="center",
    fontsize=fs_a(16),
    fontweight="bold",
    color=text,
    zorder=6
)

ax.text(
    box_x + box_w / 2,
    box_y + 0.040,
    "Energy, fidelity, circuit depth, scaling, resource estimates, or an isolated subproblem are not enough.",
    ha="center", va="center",
    fontsize=fs_a(15),
    color=mid,
    zorder=6
)


# ============================================================
# PANEL B
# Same geometry; only font sizes increased proportionally
# ============================================================

ax = ax_b

# Palette
dark = "#111111"
text = "#252B35"
muted = "#5F6670"
light_text = "#6D7480"

classical_fill = "#EEF2F6"
classical_edge = "#98A8B8"
classical_box = "#FFFFFF"

quantum_fill = "#DCEBFA"
quantum_edge = "#285F97"
quantum_core = "#78A8D8"

decision_fill = "#FFFFFF"
decision_edge = "#8D8D8D"
decision_plot_fill = "#FBFBFC"

boundary_fill = "#E9DFC9"
boundary_edge = "#5D5142"

comparator_col = "#707070"
quantum_col = "#285F97"

arrow_classical = "#9BABBA"
arrow_quantum = "#285F97"
arrow_dark = "#4B5563"

# Helper functions for panel b
def label_b(x, y, s, size=22.4, weight="normal", color=text,
            ha="center", va="center", z=20, linespacing=1.10):
    ax.text(
        x, y, s,
        ha=ha, va=va,
        fontsize=size,
        fontweight=weight,
        color=color,
        linespacing=linespacing,
        zorder=z,
        clip_on=False
    )

def rounded_box_b(x, y, w, h, s="", fc="white", ec="#333333", lw=1.25,
                  radius=0.018, size=22.4, weight="normal", color=text,
                  z=5, linespacing=1.10, pad=0.010, alpha=1.0):
    patch = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad},rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        alpha=alpha,
        zorder=z
    )
    ax.add_patch(patch)

    if s:
        label_b(
            x + w / 2,
            y + h / 2,
            s,
            size=size,
            weight=weight,
            color=color,
            z=z + 1,
            linespacing=linespacing
        )
    return patch

def arrow_b(x1, y1, x2, y2, color="#333333", lw=1.8, ms=18,
            z=12, rad=0.0, alpha=1.0, shrinkA=5, shrinkB=5):
    patch = FancyArrowPatch(
        (x1, y1), (x2, y2),
        arrowstyle="-|>",
        mutation_scale=ms,
        linewidth=lw,
        color=color,
        alpha=alpha,
        shrinkA=shrinkA,
        shrinkB=shrinkB,
        connectionstyle=f"arc3,rad={rad}",
        zorder=z
    )
    ax.add_patch(patch)
    return patch

def interval_bar_b(x0, x1, y, color, label_text, label_y, size=19.2,
                   lw=6.0, z=25, linestyle="-", label_x_offset=0.0):
    ax.add_line(Line2D(
        [x0, x1], [y, y],
        color=color,
        linewidth=lw,
        linestyle=linestyle,
        solid_capstyle="round",
        zorder=z
    ))

    cap = 0.024

    ax.add_line(Line2D(
        [x0, x0], [y - cap, y + cap],
        color=color,
        linewidth=2.2,
        zorder=z
    ))

    ax.add_line(Line2D(
        [x1, x1], [y - cap, y + cap],
        color=color,
        linewidth=2.2,
        zorder=z
    ))

    label_b(
        (x0 + x1) / 2 + label_x_offset,
        label_y,
        label_text,
        size=size,
        weight="bold",
        color=color,
        z=z + 1,
        linespacing=1.02
    )

# Panel label
label_b(
    0.035, 0.973,
    "b)",
    size=28.8,
    weight="bold",
    color=dark
)

# Title
label_b(
    0.5, 0.973,
    "Localized quantum correction inside a classical workflow",
    size=30,
    weight="bold",
    color=dark
)

# Subtle outer frame
rounded_box_b(
    0.022, 0.018, 0.956, 0.925, "",
    fc="#FFFFFF",
    ec="#D4D7DA",
    lw=1.1,
    radius=0.024,
    z=0,
    pad=0.006
)

# Original expanded zone geometry
classical_x, classical_y, classical_w, classical_h = 0.040, 0.165, 0.300, 0.690
quantum_x, quantum_y, quantum_w, quantum_h = 0.435, 0.165, 0.230, 0.690
decision_x, decision_y, decision_w, decision_h = 0.760, 0.165, 0.205, 0.690

# Reader path labels
zone_info = [
    (0.050, 0.900, "1", "classical context"),
    (0.435, 0.900, "2", "local bottleneck"),
    (0.760, 0.900, "3", "decision test"),
]

for zx, zy, num, txt in zone_info:
    rounded_box_b(
        zx, zy - 0.021, 0.042, 0.042, num,
        fc=dark, ec=dark, lw=0,
        radius=0.011,
        size=27.2,
        weight="bold",
        color="white",
        z=30,
        pad=0.003
    )

    label_b(
        zx + 0.056,
        zy,
        txt,
        size=25.6,
        weight="bold",
        color=muted,
        ha="left",
        z=30
    )

# ============================================================
# Zone 1. Classical workflow context
# ============================================================

rounded_box_b(
    classical_x, classical_y, classical_w, classical_h, "",
    fc=classical_fill,
    ec=classical_edge,
    lw=1.35,
    radius=0.027,
    z=1,
    pad=0.012
)

label_b(
    classical_x + classical_w / 2,
    classical_y + classical_h - 0.02,
    "Global reaction workflow",
    size=30.0,
    weight="bold",
    color=dark,
    z=4,
    linespacing=1.15
)

label_b(
    classical_x + classical_w / 2,
    classical_y + classical_h - 0.055,
    "remains classical",
    size=31.2,
    weight="bold",
    color=dark,
    z=4,
    linespacing=1.12
)

box_w, box_h = 0.236, 0.070
box_x = classical_x + 0.032

workflow_y = [0.665, 0.555, 0.445, 0.335, 0.225]

workflow_labels = [
    "Reaction hypothesis\ngeneration",
    "Structure and ensemble\ngeneration",
    "Sampling / environment\ntreatment",
    "Classical screening /\nfree-energy estimation",
    "Kinetic / branching analysis\nendpoint propagation → decision",
]

for i, (yy, s) in enumerate(zip(workflow_y, workflow_labels)):
    rounded_box_b(
        box_x, yy, box_w, box_h, s,
        fc=classical_box,
        ec=classical_edge,
        lw=1.05,
        radius=0.016,
        size=19.2,
        color=text,
        z=6,
        linespacing=1.02,
        pad=0.009
    )

    if i < len(workflow_y) - 1:
        arrow_b(
            box_x + box_w / 2,
            yy - 0.010,
            box_x + box_w / 2,
            workflow_y[i + 1] + box_h + 0.010,
            color=arrow_classical,
            lw=1.35,
            ms=15,
            z=7,
            shrinkA=0,
            shrinkB=0
        )

label_b(
    classical_x + classical_w / 2,
    classical_y + 0.020,
    "hypotheses, ensembles, environment,\nscreening, free energy, branching,\nand decision propagation stay classical",
    size=16.8,
    color=light_text,
    z=10,
    linespacing=1.05
)

# ============================================================
# Zone 2. Local quantum bottleneck
# ============================================================

rounded_box_b(
    quantum_x + 0.008, quantum_y - 0.008,
    quantum_w, quantum_h, "",
    fc="#000000",
    ec="#000000",
    lw=0,
    radius=0.032,
    z=3,
    alpha=0.08
)

rounded_box_b(
    quantum_x, quantum_y, quantum_w - 0.005, quantum_h, "",
    fc=quantum_fill,
    ec=quantum_edge,
    lw=2.4,
    radius=0.032,
    z=11,
    pad=0.012
)

label_b(
    quantum_x + quantum_w / 2,
    quantum_y + quantum_h - 0.020,
    "Localized quantum\ncorrection",
    size=29,
    weight="bold",
    color=dark,
    z=13,
    linespacing=1.15
)

label_b(
    quantum_x + quantum_w / 2,
    quantum_y + quantum_h - 0.108,
    "Endpoint-controlling\nbottleneck",
    size=26.08,
    weight="bold",
    color=dark,
    z=13,
    linespacing=1.10
)

ax.add_patch(
    Circle(
        (quantum_x + quantum_w / 2, quantum_y + 0.5),
        0.050,
        facecolor=quantum_core,
        edgecolor=dark,
        linewidth=1.25,
        zorder=14
    )
)

label_b(
    quantum_x + quantum_w / 2,
    quantum_y + 0.5,
    "Q",
    size=38.4,
    weight="bold",
    color="white",
    z=15
)

label_b(
    quantum_x + quantum_w / 2,
    quantum_y + 0.385,
    "where uncertainty\ncontrols the endpoint",
    size=23.68,
    color=muted,
    weight="bold",
    z=14,
    linespacing=1.12
)

rounded_box_b(
    quantum_x + 0.026,
    quantum_y + 0.286,
    quantum_w - 0.052,
    0.068,
    "Electronic structure | Embedding\nDynamics | Estimator / extraction",
    fc="#FFFFFF",
    ec=quantum_edge,
    lw=0.95,
    radius=0.014,
    size=17.6,
    color=text,
    z=14,
    linespacing=1.04,
    pad=0.006
)

# White-background bottleneck block
bottleneck_box_x = quantum_x + 0.027
bottleneck_box_y = quantum_y + 0.015
bottleneck_box_w = quantum_w - 0.050
bottleneck_box_h = 0.245

rounded_box_b(
    bottleneck_box_x,
    bottleneck_box_y,
    bottleneck_box_w,
    bottleneck_box_h,
    "",
    fc="#FAFAFA",
    #fc="#FFFFFF",
    ec="#C9C9C9",
    #ec=quantum_edge,
    lw=0.05,
    radius=0.014,
    z=16,
    pad=0.006
)

label_b(
    quantum_x + quantum_w / 1.92,
    bottleneck_box_y + bottleneck_box_h - 0.016,
    "Endpoint-controlling bottlenecks",
    size=17,
    weight="bold",
    color=dark,
    z=19,
    linespacing=1.20
)

# bottleneck_text = (
#     "embedded active space\n"
#     "transition-state region\n"
#     "surface site\n"
#     "catalytic active site\n"
#     "solvated subsystem\n"
#     "reduced multistate or open-system model\n"
#     "transition-state correlation\n"
#     "spin-state ambiguity\n"
#     "active-site electronics\n"
#     "solvent-sensitive reordering\n"
#     "estimator-limited observable\n"
#     "nonadiabatic crossing"
# )

bottleneck_text = (
    "embedded active spaces\n"
    "transition-state regions\n"
    "surface sites\n"
    "catalytic active sites\n"
    "solvated subsystems\n"
    "multistate / open-system models\n"
    "spin / correlation ambiguity\n"
    "estimator-limited observables\n"
    "nonadiabatic crossings"
)


label_b(
    bottleneck_box_x + 0.008,
    bottleneck_box_y + 0.117,
    bottleneck_text,
    size=17.8,
    weight="normal",
    color=text,
    ha="left",
    z=18,
    linespacing=1.5
)

# Arrow from classical context to quantum bottleneck
arrow_b(
    classical_x + classical_w + 0.024,
    0.495,
    quantum_x - 0.024,
    0.495,
    color=arrow_dark,
    lw=2.2,
    ms=22,
    z=12,
    shrinkA=0,
    shrinkB=0
)

label_b(
    (classical_x + classical_w + quantum_x) / 2,
    0.555,
    "bottleneck\nselection",
    size=22.4,
    color=muted,
    z=13,
    linespacing=1.05
)

# ============================================================
# Zone 3. Reaction decision boundary
# ============================================================

rounded_box_b(
    decision_x, decision_y, decision_w, decision_h, "",
    fc=decision_fill,
    ec=decision_edge,
    lw=1.35,
    radius=0.027,
    z=1,
    pad=0.012
)

label_b(
    decision_x + decision_w / 2,
    decision_y + decision_h - 0.02,
    "Reaction decision\nboundary",
    size=28.8,
    weight="bold",
    color=dark,
    z=4
)

label_b(
    decision_x + decision_w / 2,
    decision_y + decision_h - 0.070,
    "schematic decision coordinate",
    size=22.4,
    color=muted,
    z=4
)

# Decision plot
px0, py0 = decision_x + 0.025, decision_y + 0.220
pw, ph = decision_w - 0.050, 0.350

ax.add_patch(Rectangle(
    (px0, py0),
    pw,
    ph,
    facecolor=decision_plot_fill,
    edgecolor="#CBD2D9",
    linewidth=1.0,
    zorder=2
))

# Boundary / ambiguous region
boundary_center = px0 + pw * 0.52
boundary_w = pw * 0.112

ax.add_patch(Rectangle(
    (boundary_center - boundary_w / 2, py0),
    boundary_w,
    ph,
    facecolor=boundary_fill,
    edgecolor="none",
    alpha=0.90,
    zorder=3
))

ax.add_line(Line2D(
    [boundary_center, boundary_center],
    [py0, py0 + ph],
    color="#3D3328",
    linewidth=3.5,
    zorder=4
))

label_b(
    boundary_center,
    py0 + ph + 0.015,
    "ambiguous\nzone",
    size=16.0,
    weight="bold",
    color=boundary_edge,
    z=6,
    linespacing=0.98
)

# Endpoint axis
axis_y = py0 + 0.065

ax.add_line(Line2D(
    [px0 + 0.020, px0 + pw - 0.020],
    [axis_y, axis_y],
    color="#475467",
    linewidth=1.15,
    zorder=5
))

arrow_b(
    px0 + pw - 0.050,
    axis_y,
    px0 + pw - 0.010,
    axis_y,
    color="#475467",
    lw=1.10,
    ms=12,
    z=5,
    shrinkA=0,
    shrinkB=0
)

label_b(
    px0 + pw / 1.92,
    py0 - 0.03,
    "Reaction endpoint",
    size=20.8,
    color=text,
    z=6
)

label_b(
    px0 + 0.042,
    py0 + ph - 0.05,
    "Decision A",
    size=20.8,
    color=muted,
    z=6
)

label_b(
    px0 + pw - 0.036,
    py0 + ph - 0.05,
    "Decision B",
    size=20.8,
    color=muted,
    z=6
)

# Comparator interval crosses the boundary
comp_y = py0 + ph * 0.66

interval_bar_b(
    px0 + pw * 0.18,
    px0 + pw * 0.55,
    comp_y,
    comparator_col,
    "Comparator:\nambiguous",
    label_y=comp_y - 0.05,
    size=19,
    lw=5.2,
    z=10,
    linestyle=(0, (4, 2)),
    label_x_offset=-0.018
)

# Quantum-assisted interval is narrower/shifted to one side
quant_y = py0 + ph * 0.38

interval_bar_b(
    px0 + pw * 0.62,
    px0 + pw * 0.905,
    quant_y,
    quantum_col,
    "Quantum-assisted:\nclarified",
    label_y=quant_y - 0.047,
    size=18,
    lw=5.2,
    z=10,
    linestyle="-",
    label_x_offset=0.018
)

# Decision-effect statement
rounded_box_b(
    decision_x + 0.024,
    decision_y + 0.050,
    decision_w - 0.048,
    0.090,
    "Decision changed,\nstabilized, or\nalternative ruled out",
    fc="#F8FAFC",
    ec=decision_edge,
    lw=0.9,
    radius=0.016,
    size=22.4,
    weight="bold",
    color=dark,
    z=8,
    linespacing=1.04,
    pad=0.008
)

# Arrow from quantum bottleneck to decision panel
arrow_b(
    quantum_x + quantum_w + 0.024,
    0.495,
    decision_x - 0.024,
    0.495,
    color=arrow_quantum,
    lw=2.35,
    ms=23,
    z=20,
    shrinkA=0,
    shrinkB=0
)

label_b(
    (quantum_x + quantum_w + decision_x) / 2,
    0.555,
    "endpoint\npropagation",
    size=19.2,
    weight="bold",
    color=quantum_edge,
    z=21,
    linespacing=1.0
)

# Bottom operational statement
rounded_box_b(
    0.045,
    0.035,
    0.910,
    0.070,
    "Comparator-level ambiguity → localized quantum correction → endpoint propagation → decision-level resolution",
    fc="#FAFAFA",
    ec="#C9C9C9",
    lw=1.0,
    radius=0.018,
    size=24,
    weight="bold",
    color="#3F4650",
    z=5,
    pad=0.009
)
# ----------------------------
# Export
# ----------------------------
fig.savefig(OUTPUT_DIR / "Figure2_benchmarking_funnel_localized_quantum_leverage.pdf",
            bbox_inches="tight", facecolor="white")
fig.savefig(OUTPUT_DIR / "Figure2_benchmarking_funnel_localized_quantum_leverage.png",
            dpi=600, bbox_inches="tight", facecolor="white")
plt.close(fig)
