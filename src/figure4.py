"""Generate Figure 4: decision-stable reaction endpoints.

This script was derived from the original notebook:
notebooks/Benchmarking_quantum_computation_for_chemical_reactivity.ipynb
"""
from pathlib import Path
import matplotlib
matplotlib.use("Agg", force=True)

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "figures"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Polygon, FancyArrowPatch, Rectangle
import matplotlib as mpl
import numpy as np

# ============================================================
# Figure 4
# Roadmap to decision-stable reaction endpoints
#
# Hybrid redesign:
# - Uses concise terms and stronger left-to-right visual structure
# - Uses a middle wedge shape for endpoint propagation
# - Clearly separates:
#   A. Conceptual outcome
#   B. Operational mechanism
#
# No image is rendered or saved unless RENDER=True or SAVE=True.
# ============================================================

RENDER = False
SAVE = False

# Move everything down except the title
SHIFT_DOWN = 0.10
def Y(y):
    return y - SHIFT_DOWN

# ----------------------------
# Vector-friendly settings
# ----------------------------
mpl.rcParams["font.family"] = "DejaVu Sans"
mpl.rcParams["pdf.fonttype"] = 42
mpl.rcParams["ps.fonttype"] = 42
mpl.rcParams["svg.fonttype"] = "none"

# ----------------------------
# Canvas
# ----------------------------
fig = plt.figure(figsize=(18, 11.6), dpi=400)
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, 1)

# Extended lower limit so the shifted-down footer and frame are not clipped.
ax.set_ylim(-0.12, 1)

ax.axis("off")

# ----------------------------
# Palette
# ----------------------------
dark = "#111111"
text = "#242A33"
muted = "#5F6670"
mid = "#5F6670"
soft = "#737B85"

outer_edge = "#D4D8DD"
grid_edge = "#D8DDE3"
blue_edge = "#6F93BB"
arrow_edge = "#A9B8C9"

wedge_fill = "#E8EFF7"
wedge_inner = "#F7FAFD"
card_fill = "#FFFFFF"
funnel_fill = "#EAF1F8"
chip_fill = "#FFFFFF"
gate_fill = "#DDE8F4"
footer_fill = "#FAFAFA"

# ----------------------------
# Helpers
# ----------------------------
def label(x, y, s, size=16, weight="normal", color=text,
          ha="center", va="center", linespacing=1.15, z=20,
          rotation=0, rotation_mode=None):
    ax.text(
        x, y, s,
        fontsize=size,
        fontweight=weight,
        color=color,
        ha=ha,
        va=va,
        linespacing=linespacing,
        zorder=z,
        clip_on=False,
        rotation=rotation,
        rotation_mode=rotation_mode
    )

def rounded_box(x, y, w, h, s="", fs=15, weight="normal",
                fc="white", ec=grid_edge, lw=1.0,
                radius=0.012, pad=0.004, color=text,
                linespacing=1.13, z=5):
    box = FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad={pad},rounding_size={radius}",
        facecolor=fc,
        edgecolor=ec,
        linewidth=lw,
        zorder=z,
        clip_on=False
    )
    ax.add_patch(box)

    if s:
        label(
            x + w / 2,
            y + h / 2,
            s,
            size=fs,
            weight=weight,
            color=color,
            linespacing=linespacing,
            z=z + 1
        )
    return box

def arrow(x1, y1, x2, y2, color=arrow_edge, lw=1.25, ms=12, z=10,
          connectionstyle="arc3,rad=0.0"):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1), (x2, y2),
            arrowstyle="-|>",
            mutation_scale=ms,
            linewidth=lw,
            color=color,
            connectionstyle=connectionstyle,
            zorder=z,
            clip_on=False
        )
    )

def draw_check(cx, cy, scale=1.0, color=blue_edge, lw=1.6):
    ax.plot(
        [cx - 0.010 * scale, cx - 0.002 * scale, cx + 0.012 * scale],
        [cy - 0.002 * scale, cy - 0.012 * scale, cy + 0.012 * scale],
        color=color,
        linewidth=lw,
        zorder=20,
        clip_on=False
    )

# ============================================================
# Icon functions
# ============================================================

def icon_representation(cx, cy, scale=1.0):
    w, h = 0.030 * scale, 0.022 * scale
    for i, alpha in enumerate([1.0, 0.8, 0.6]):
        ax.add_patch(
            Rectangle(
                (cx - w / 2 + i * 0.007 * scale, cy - h / 2 + i * 0.005 * scale),
                w,
                h,
                facecolor="none",
                edgecolor=blue_edge,
                linewidth=1.2,
                alpha=alpha,
                zorder=15,
                clip_on=False
            )
        )

def icon_measurement(cx, cy, scale=1.0):
    for r in [0.020, 0.012, 0.004]:
        ax.add_patch(
            Circle(
                (cx, cy),
                r * scale,
                facecolor="none",
                edgecolor=blue_edge,
                linewidth=1.2,
                zorder=15,
                clip_on=False
            )
        )
    ax.plot(
        [cx - 0.019 * scale, cx - 0.010 * scale],
        [cy + 0.017 * scale, cy + 0.010 * scale],
        color=blue_edge,
        linewidth=1.1,
        zorder=15,
        clip_on=False
    )

def icon_environment(cx, cy, scale=1.0):
    ax.add_patch(
        Circle(
            (cx, cy),
            0.008 * scale,
            facecolor=blue_edge,
            edgecolor=blue_edge,
            linewidth=1.0,
            zorder=15,
            clip_on=False
        )
    )
    for ang in np.linspace(0, 2 * np.pi, 7, endpoint=False):
        ax.add_patch(
            Circle(
                (
                    cx + 0.022 * scale * np.cos(ang),
                    cy + 0.018 * scale * np.sin(ang)
                ),
                0.0048 * scale,
                facecolor="white",
                edgecolor=blue_edge,
                linewidth=1.0,
                zorder=15,
                clip_on=False
            )
        )

def icon_sensitivity(cx, cy, scale=1.0):
    ax.plot(
        [cx - 0.028 * scale, cx + 0.032 * scale],
        [cy - 0.016 * scale, cy + 0.016 * scale],
        color=blue_edge,
        linewidth=1.4,
        zorder=15,
        clip_on=False
    )
    ax.plot(
        [cx - 0.028 * scale, cx + 0.032 * scale],
        [cy + 0.003 * scale, cy + 0.003 * scale],
        color=blue_edge,
        linewidth=1.0,
        linestyle="--",
        zorder=15,
        clip_on=False
    )
    ax.add_patch(
        Circle(
            (cx + 0.018 * scale, cy + 0.010 * scale),
            0.0055 * scale,
            facecolor="white",
            edgecolor=blue_edge,
            linewidth=1.1,
            zorder=16,
            clip_on=False
        )
    )

def icon_dynamics(cx, cy, scale=1.0):
    ax.plot(
        [cx - 0.030 * scale, cx - 0.005 * scale],
        [cy, cy],
        color=blue_edge,
        linewidth=1.4,
        zorder=15,
        clip_on=False
    )
    for dy in [0.018, 0.0, -0.018]:
        ax.plot(
            [cx - 0.005 * scale, cx + 0.028 * scale],
            [cy, cy + dy * scale],
            color=blue_edge,
            linewidth=1.4,
            zorder=15,
            clip_on=False
        )
        ax.add_patch(
            Circle(
                (cx + 0.028 * scale, cy + dy * scale),
                0.0048 * scale,
                facecolor="white",
                edgecolor=blue_edge,
                linewidth=1.0,
                zorder=16,
                clip_on=False
            )
        )
    ax.add_patch(
        Circle(
            (cx - 0.030 * scale, cy),
            0.0048 * scale,
            facecolor="white",
            edgecolor=blue_edge,
            linewidth=1.0,
            zorder=16,
            clip_on=False
        )
    )

# ============================================================
# Outer frame and title
# ============================================================

rounded_box(
    0.025, Y(0.055), 0.950, 0.941, "",
    fc="#FFFFFF",
    ec=outer_edge,
    lw=1.0,
    radius=0.022,
    z=0
)

# Title is intentionally NOT shifted down.
label(
    0.5,
    0.940,
    "Roadmap to decision-stable reaction endpoints",
    size=24,
    weight="medium",
    color=mid
)

# ============================================================
# A. Conceptual outcome
# ============================================================

label(
    0.025,
    Y(0.970),
    "a) Conceptual outcome",
    size=12.8,
    weight="bold",
    color=soft,
    ha="left"
)

label(
    0.5,
    Y(0.955),
    "Decision-level uncertainty narrows",
    size=18,
    weight="bold",
    color=mid
)

rounded_box(
    0.052,
    Y(0.715),
    0.170,
    0.115,
    "Current\nuncertainty",
    fs=18.0,
    weight="bold",
    fc="#FFFFFF",
    ec=dark,
    lw=1.0,
    radius=0.020
)

rounded_box(
    0.778,
    Y(0.715),
    0.180,
    0.115,
    "Decision-stable\nendpoint",
    fs=18.0,
    weight="bold",
    fc="#FFFFFF",
    ec=dark,
    lw=1.0,
    radius=0.020
)

# Very enlarged conceptual wedge
x0, x1 = 0.245, 0.765
yc = Y(0.772)

top_wedge = Polygon(
    [
        (x0, yc + 0.170),
        (x1, yc + 0.050),
        (x1, yc - 0.050),
        (x0, yc - 0.170),
    ],
    closed=True,
    facecolor=wedge_fill,
    edgecolor=blue_edge,
    linewidth=1.35,
    zorder=2,
    clip_on=False
)
ax.add_patch(top_wedge)

top_inner = Polygon(
    [
        (x0 + 0.030, yc + 0.040),
        (x1 - 0.020, yc + 0.017),
        (x1 - 0.020, yc - 0.017),
        (x0 + 0.030, yc - 0.040),
    ],
    closed=True,
    facecolor=wedge_inner,
    edgecolor="none",
    zorder=3,
    clip_on=False
)
ax.add_patch(top_inner)

arrow(
    x0 + 0.065,
    yc,
    x1 - 0.060,
    yc,
    color=arrow_edge,
    lw=1.9,
    ms=22,
    z=4
)

# Larger and more spread outcome dots
for px, py in [
    (0.300, Y(0.850)),
    (0.345, Y(0.810)),
    (0.305, Y(0.730)),
    (0.385, Y(0.835)),
    (0.340, Y(0.760)),
]:
    ax.add_patch(
        Circle(
            (px, py),
            0.0112,
            facecolor="white",
            edgecolor=blue_edge,
            linewidth=1.0,
            zorder=5,
            clip_on=False
        )
    )

ax.add_patch(
    Circle(
        (0.730, yc),
        0.0128,
        facecolor="white",
        edgecolor=blue_edge,
        linewidth=1.1,
        zorder=5,
        clip_on=False
    )
)

label(
    0.337,
    Y(0.890),
    "multiple plausible outcomes",
    size=14.5,
    weight="bold",
    color=muted
)

label(
    0.860,
    Y(0.890),
    "stable conclusion",
    size=14.5,
    weight="bold",
    color=muted
)

# label(
#     0.868,
#     Y(0.680),
#     "Useful accuracy is\ndecision-relative.",
#     size=13.8,
#     weight="normal",
#     color=muted,
#     linespacing=1.22
# )


label(
    0.868,
    Y(0.680),
    "Useful accuracy is decision-relative,\nnot a universal numerical cutoff.",
    size=11.6,
    weight="normal",
    color=muted,
    linespacing=1.18
)



# ============================================================
# B. Operational mechanism
# ============================================================

# label(
#     0.025,
#     Y(0.530),
#     "b) Operational mechanism",
#     size=14.0,
#     weight="bold",
#     color=soft,
#     ha="left"
# )

label(
    0.025,
    Y(0.530),
    "b) Operational claim standard",
    size=14.0,
    weight="bold",
    color=soft,
    ha="left"
)



# Short section labels
label(0.185, Y(0.480), "Bottleneck sources", size=15, weight="bold", color=muted)
label(0.420, Y(0.480), "Corrective moves", size=15, weight="bold", color=muted)
label(0.755, Y(0.480), "Endpoint tests", size=15, weight="bold", color=muted)

# ------------------------------------------------------------
# Left input bank: bottleneck sources
# ------------------------------------------------------------

cards = [
    {
        "y": Y(0.420),
        "name": "Representation",
        "icon": icon_representation,
        "chip": "Faithful reduction"
    },
    {
        "y": Y(0.365),
        "name": "Measurement \n& resources",
        "icon": icon_measurement,
        "chip": "Endpoint estimation"
    },
    {
        "y": Y(0.310),
        "name": "Environment",
        "icon": icon_environment,
        "chip": "Context propagation"
    },
    {
        "y": Y(0.255),
        "name": "Endpoint \nsensitivity",
        "icon": icon_sensitivity,
        "chip": "Uncertainty propagation"
    },
    {
        "y": Y(0.200),
        "name": "Multistate / \nopen-system",
        "icon": icon_dynamics,
        "chip": "Dynamical treatment"
    },
]

card_x = 0.065
card_w = 0.230
card_h = 0.040

for card in cards:
    y = card["y"]

    rounded_box(
        card_x,
        y,
        card_w,
        card_h,
        "",
        fc=card_fill,
        ec=grid_edge,
        lw=0.9,
        radius=0.012,
        z=5
    )

    card["icon"](
        card_x + 0.035,
        y + card_h / 2,
        scale=0.78
    )

    label(
        card_x + 0.120,
        y + card_h / 2,
        card["name"],
        size=13,
        weight="bold",
        color=text,
        linespacing=1.3,
        z=10
    )

# ------------------------------------------------------------
# Central wedge: endpoint propagation with concise corrective-move terms
# ------------------------------------------------------------

funnel_left = 0.355
funnel_right = 0.610
funnel_top = Y(0.450)
funnel_bottom = Y(0.210)
funnel_mid_y = Y(0.330)

# Keep the wedge shape from the stronger visual version
middle_wedge = Polygon(
    [
        (funnel_left, funnel_top),
        (funnel_right, Y(0.400)),
        (funnel_right, Y(0.250)),
        (funnel_left, funnel_bottom),
    ],
    closed=True,
    facecolor=funnel_fill,
    edgecolor=blue_edge,
    linewidth=1.25,
    zorder=3,
    clip_on=False
)
ax.add_patch(middle_wedge)

# Inner horizontal propagation spine
rounded_box(
    funnel_left + 0.045,
    funnel_mid_y - 0.028,
    funnel_right - funnel_left - 0.085,
    0.056,
    "",
    fc="#F7FAFD",
    ec="none",
    lw=0,
    radius=0.010,
    z=4
)

arrow(
    funnel_left + 0.065,
    funnel_mid_y,
    funnel_right - 0.055,
    funnel_mid_y,
    color=arrow_edge,
    lw=1.6,
    ms=18,
    z=5
)

label(
    0.550,
    Y(0.330),
    "Endpoint\npropagation",
    size=15.0,
    weight="bold",
    color=text,
    linespacing=2.0,
    z=10
)

label(
    0.480,
    Y(0.195),
    "decision-carrying reaction observable",
    size=13,
    weight="normal",
    color=muted,
    z=10
)

# Corrective-move chips: terms from the first figure, not the overly long second version
chip_x = 0.370
chip_w = 0.135
chip_h = 0.038

move_chips = [
    ("Faithful reduction", Y(0.400)),
    ("Endpoint estimation", Y(0.364)),
    ("Context propagation", Y(0.328)),
    ("Uncertainty propagation", Y(0.292)),
    ("Dynamical treatment", Y(0.256)),
]

for txt, cy in move_chips:
    rounded_box(
        chip_x,
        cy - chip_h / 2,
        chip_w,
        chip_h,
        txt,
        fs=12.8,
        weight="bold",
        fc=chip_fill,
        ec="#C9D3DE",
        lw=0.8,
        radius=0.009,
        color=muted,
        linespacing=0.90,
        z=7
    )

# Arrows from bottleneck sources into matching corrective chips
for card, (_, chip_y) in zip(cards, move_chips):
    start_x = card_x + card_w + 0.010
    start_y = card["y"] + card_h / 2
    end_x = chip_x - 0.010
    end_y = chip_y

    arrow(
        start_x,
        start_y,
        end_x,
        end_y,
        color="#BAC5D1",
        lw=0.95,
        ms=8,
        z=2
    )

# ------------------------------------------------------------
# Endpoint-test gates
# ------------------------------------------------------------

gate_x = 0.690
gate_w = 0.165
gate_h = 0.050

gates = [
    {
        "y": Y(0.360),
        "text": "Comparator\nmatched"
    },
    {
        "y": Y(0.300),
        "text": "Uncertainty\nbounded"
    },
    {
        "y": Y(0.240),
        "text": "Conclusion\nstable"
    },
]

for gate in gates:
    y = gate["y"]

    rounded_box(
        gate_x,
        y,
        gate_w,
        gate_h,
        "",
        fc=gate_fill,
        ec=blue_edge,
        lw=1.25,
        radius=0.014,
        z=5
    )

    draw_check(
        gate_x + 0.030,
        y + gate_h / 2 + 0.002,
        scale=0.80,
        color=blue_edge,
        lw=1.4
    )

    label(
        gate_x + 0.092,
        y + gate_h / 2,
        gate["text"],
        size=14,
        weight="bold",
        color=text,
        linespacing=1.3,
        z=10
    )

# Arrow from middle wedge to endpoint tests
arrow(
    funnel_right + 0.010,
    funnel_mid_y,
    gate_x - 0.015,
    funnel_mid_y,
    color="#BAC5D1",
    lw=1.2,
    ms=11,
    z=5
)

# ------------------------------------------------------------
# Final endpoint-supported claim
# ------------------------------------------------------------

claim_x = 0.875
claim_y = Y(0.285)
claim_w = 0.085
claim_h = 0.080

rounded_box(
    claim_x,
    claim_y,
    claim_w,
    claim_h,
    "Endpoint-\nsupported\nclaim",
    fs=14.5,
    weight="bold",
    fc="#FFFFFF",
    ec=dark,
    lw=1.0,
    radius=0.016,
    linespacing=1.3,
    z=6
)

arrow(
    gate_x + gate_w + 0.015,
    funnel_mid_y,
    claim_x - 0.012,
    claim_y + claim_h / 2,
    color="#BAC5D1",
    lw=1.2,
    ms=11,
    z=5
)

# ============================================================
# Footer
# ============================================================

rounded_box(
    0.075,
    Y(0.075),
    0.850,
    0.055,
    "",
    fc=footer_fill,
    ec="#D0D4D9",
    lw=1.0,
    radius=0.012,
    z=4
)

# label(
#     0.5,
#     Y(0.090),
#     "Requirements for reaction-endpoint utility, not capability claims.",
#     size=15.5,
#     weight="bold",
#     color=text
# )


label(
    0.5,
    Y(0.100),
    "Evidence and endpoint tests for reaction-endpoint utility claims, not a claim of established reaction-endpoint capability.",
    size=13.2,
    weight="bold",
    color=text
)
# ----------------------------
# Export
# ----------------------------
fig.savefig(OUTPUT_DIR / "Figure4_decision_stable_reaction_endpoints.pdf",
            bbox_inches="tight", facecolor="white")
fig.savefig(OUTPUT_DIR / "Figure4_decision_stable_reaction_endpoints.png",
            dpi=600, bbox_inches="tight", facecolor="white")
plt.close(fig)
