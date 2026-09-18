import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, Circle, Arc

BRAND = "#0f6e5c"
BRAND_DARK = "#0a4f42"
BAD = "#c0392b"
BAD_SOFT = "#f6dcd8"
INK = "#1c2430"
MUTED = "#8a8f98"

# limb lengths (arbitrary units) - scaled to fit default panel ylim (-0.3, 2.9)
L_SHIN = 0.62
L_THIGH = 0.65
L_TORSO = 0.82
L_NECK = 0.10
HEAD_R = 0.19
L_UARM = 0.46
L_FARM = 0.43
FOOT = 0.34


def _dir(angle_deg, sign=1):
    r = math.radians(angle_deg)
    return (math.sin(r), sign * math.cos(r))


def _add(p, v, k=1.0):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def build_pose(p):
    """p: dict of pose parameters -> dict of computed joint points."""
    front_ankle = p.get("front_ankle", (0.0, 0.0))
    knee1 = _add(front_ankle, _dir(p["front_shin"], 1), L_SHIN)
    hip = _add(knee1, _dir(p["front_thigh"], 1), L_THIGH)

    pts = {"front_ankle": front_ankle, "front_knee": knee1, "hip": hip}

    if p.get("back_thigh") is not None:
        back_knee = _add(hip, _dir(p["back_thigh"], -1), L_THIGH)
        back_ankle = _add(back_knee, _dir(p["back_shin"], -1), L_SHIN)
        pts["back_knee"] = back_knee
        pts["back_ankle"] = back_ankle

    shoulder = _add(hip, _dir(p["torso_angle"], 1), L_TORSO)
    head_c = _add(shoulder, _dir(p["torso_angle"], 1), L_NECK + HEAD_R)
    pts["shoulder"] = shoulder
    pts["head"] = head_c

    elbow = _add(shoulder, _dir(p["shoulder_angle"], -1), L_UARM)
    hand = _add(elbow, _dir(p["elbow_angle"], -1), L_FARM)
    pts["elbow"] = elbow
    pts["hand"] = hand

    if p.get("shoulder_angle2") is not None:
        elbow2 = _add(shoulder, _dir(p["shoulder_angle2"], -1), L_UARM)
        hand2 = _add(elbow2, _dir(p["elbow_angle2"], -1), L_FARM)
        pts["elbow2"] = elbow2
        pts["hand2"] = hand2

    return pts


def draw_pose(ax, p, color=BRAND, lw=3.4, ground=0.0, alpha=1.0):
    pts = build_pose(p)

    def ln(a, b, **kw):
        kw.setdefault("alpha", alpha)
        ax.plot([pts[a][0], pts[b][0]], [pts[a][1], pts[b][1]],
                 color=color, lw=lw, solid_capstyle="round", zorder=3, **kw)

    # ground
    ax.axhline(ground, color="#c9cdd3", lw=1.4, zorder=1)

    # back leg first (behind)
    if "back_ankle" in pts:
        ln("hip", "back_knee", alpha=alpha * 0.55)
        ln("back_knee", "back_ankle", alpha=alpha * 0.55)
        fx, fy = pts["back_ankle"]
        ax.plot([fx, fx + FOOT * 0.8], [fy, fy], color=color, lw=lw, alpha=alpha * 0.55,
                 solid_capstyle="round", zorder=3)

    # front leg
    ln("front_ankle", "front_knee")
    ln("front_knee", "hip")
    fx, fy = pts["front_ankle"]
    ax.plot([fx, fx + FOOT], [fy, fy], color=color, lw=lw, alpha=alpha,
             solid_capstyle="round", zorder=3)

    # torso
    ln("hip", "shoulder")

    # arm(s)
    ln("shoulder", "elbow")
    ln("elbow", "hand")
    if "hand2" in pts:
        ln2a, ln2b = pts["shoulder"], pts["elbow2"]
        ax.plot([ln2a[0], ln2b[0]], [ln2a[1], ln2b[1]], color=color, lw=lw,
                 alpha=alpha, solid_capstyle="round", zorder=3)
        ax.plot([pts["elbow2"][0], pts["hand2"][0]], [pts["elbow2"][1], pts["hand2"][1]],
                 color=color, lw=lw, alpha=alpha, solid_capstyle="round", zorder=3)

    # head
    hx, hy = pts["head"]
    ax.add_patch(Circle((hx, hy), HEAD_R, facecolor="white", edgecolor=color,
                          lw=lw * 0.85, alpha=alpha, zorder=4))

    # held object
    obj = p.get("object")
    if obj == "dumbbell":
        for key in (["hand", "hand2"] if "hand2" in pts else ["hand"]):
            hxp, hyp = pts[key]
            ax.add_patch(mpatches.FancyBboxPatch((hxp - 0.055, hyp - 0.10), 0.11, 0.20,
                          boxstyle="round,pad=0.006,rounding_size=0.02",
                          facecolor=BRAND_DARK, edgecolor="none", alpha=alpha, zorder=5))
    elif obj == "goblet":
        hxp, hyp = pts["hand"]
        ax.add_patch(Circle((hxp, hyp - 0.03), 0.14, facecolor=BRAND_DARK,
                              edgecolor="none", alpha=alpha, zorder=5))
    elif obj == "backpack":
        hxp, hyp = pts["hand"]
        ax.add_patch(mpatches.FancyBboxPatch((hxp - 0.15, hyp - 0.18), 0.30, 0.36,
                      boxstyle="round,pad=0.006,rounding_size=0.05",
                      facecolor=BRAND_DARK, edgecolor="none", alpha=alpha, zorder=5))

    return pts


def mistake_marker(ax, pts, kind):
    """Draw a red highlight for a common mistake at a joint region."""
    if kind == "knee":
        k = pts["front_knee"]
        ax.add_patch(Circle(k, 0.155, facecolor="none", edgecolor=BAD, lw=2.4,
                              linestyle=(0, (3, 2)), zorder=6))
    elif kind == "hip_sag":
        hip = pts["hip"]
        ax.add_patch(Circle((hip[0], hip[1]), 0.12, facecolor="none", edgecolor=BAD,
                              lw=2.4, linestyle=(0, (3, 2)), zorder=6))
    elif kind == "heel":
        a = pts["front_ankle"]
        ax.add_patch(Circle((a[0] - 0.03, a[1]), 0.10, facecolor="none", edgecolor=BAD,
                              lw=2.4, linestyle=(0, (3, 2)), zorder=6))
    # "back_round" intentionally has no shape overlay: the red pose + caption already
    # communicate the mistake, and an arc along a rotating spine reads poorly at this scale.


def panel(ax, p, step_no=None, caption=None, mistake=False, mistakes=None, xlim=(-1.3, 2.1), ylim=(-0.3, 2.9)):
    color = BAD if mistake else BRAND
    pts = draw_pose(ax, p, color=color)
    if mistakes:
        for m in mistakes:
            mistake_marker(ax, pts, m)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if step_no is not None:
        badge_color = BAD if mistake else BRAND_DARK
        ax.add_patch(Circle((xlim[0] + 0.22, ylim[1] - 0.22), 0.165, facecolor=badge_color,
                              edgecolor="none", zorder=8))
        ax.text(xlim[0] + 0.22, ylim[1] - 0.22, str(step_no), color="white", fontsize=12,
                fontweight="bold", ha="center", va="center", zorder=9)
    if caption:
        ax.text((xlim[0] + xlim[1]) / 2, ylim[0] + 0.05, caption, ha="center", va="bottom",
                fontsize=10.2, color=(BAD if mistake else INK), wrap=True,
                fontweight=("bold" if mistake else "normal"))


def draw_floor(ax, kind, variant="ok", color=None, mistake=False):
    """Simple hand-placed poses for floor exercises (person lying/prone).
    Ground drawn as a horizontal line; body drawn with plain segments."""
    c = color or (BAD if mistake else BRAND)
    lw = 3.2

    def ln(a, b, **kw):
        ax.plot([a[0], b[0]], [a[1], b[1]], color=c, lw=lw, solid_capstyle="round", zorder=3, **kw)

    ax.axhline(0.32, color="#c9cdd3", lw=1.4, zorder=1)  # "floor" for lying poses

    if kind == "bridge":
        # lying on back, knees bent, hips down or up
        shoulder = (-0.9, 0.32)
        head_c = (-1.18, 0.32)
        hip_down = (0.0, 0.32)
        hip_up = (0.0, 0.62)
        hip_over = (0.0, 0.86)
        hip = {"up": hip_up, "sag": hip_over}.get(variant, hip_down)
        knee = (0.55, 0.62)
        foot = (0.85, 0.32)
        ln(shoulder, hip)
        ln(hip, knee)
        ln(knee, foot)
        ax.plot([foot[0] - 0.18, foot[0] + 0.05], [foot[1], foot[1]], color=c, lw=lw,
                 solid_capstyle="round", zorder=3)
        ax.add_patch(Circle(head_c, HEAD_R, facecolor="white", edgecolor=c, lw=lw * 0.85, zorder=4))
        if variant == "sag":
            ax.add_patch(Arc((-0.1, 0.42), 0.5, 0.35, angle=0, theta1=200, theta2=340,
                              color=BAD, lw=2.4, zorder=6))

    elif kind == "plank":
        shoulder = (-0.55, 0.85)
        elbow = (-0.55, 0.32)
        hip_y = {"ok": 0.85, "sag": 0.60, "pike": 1.15}[variant]
        hip = (0.35, hip_y)
        ankle = (1.35, 0.32)
        head_c = (-0.85, 0.90 if variant == "ok" else (0.68 if variant == "sag" else 1.18))
        ln(shoulder, elbow)
        ln(elbow, (elbow[0] - 0.05, 0.32), )
        ln(shoulder, hip)
        ln(hip, ankle)
        ax.plot([ankle[0], ankle[0] + 0.16], [ankle[1] - 0.05, ankle[1] + 0.10], color=c, lw=lw,
                 solid_capstyle="round", zorder=3)
        ax.add_patch(Circle(head_c, HEAD_R, facecolor="white", edgecolor=c, lw=lw * 0.85, zorder=4))
        if variant == "sag":
            ax.add_patch(Arc((0.0, 0.78), 0.7, 0.45, angle=0, theta1=200, theta2=345,
                              color=BAD, lw=2.4, zorder=6))
        elif variant == "pike":
            ax.add_patch(Arc((0.0, 1.0), 0.7, 0.45, angle=180, theta1=200, theta2=345,
                              color=BAD, lw=2.4, zorder=6))

    elif kind == "deadbug":
        shoulder = (-0.7, 0.32)
        head_c = (-0.98, 0.32)
        hip = (0.1, 0.32)
        # extended arm + opposite leg
        hand = (-0.35, 1.05)
        knee_bent = (0.35, 0.75)
        foot_bent = (0.15, 0.32)
        knee_ext = (0.75, 0.55)
        foot_ext = (1.25, 0.20)
        ln(shoulder, hip)
        ln(shoulder, hand)
        ln(hip, knee_bent)
        ln(knee_bent, foot_bent)
        ln(hip, knee_ext)
        ln(knee_ext, foot_ext)
        ax.add_patch(Circle(head_c, HEAD_R, facecolor="white", edgecolor=c, lw=lw * 0.85, zorder=4))

    elif kind == "crunch":
        hip = (0.15, 0.32)
        knee = (0.65, 0.72)
        foot = (1.05, 0.32)
        sh_down = (-0.55, 0.32)
        sh_up = (-0.42, 0.55)
        shoulder = sh_up if variant == "up" else sh_down
        head_c = (shoulder[0] - 0.30, shoulder[1] + (0.10 if variant == "up" else 0.0))
        ln(shoulder, hip)
        ln(hip, knee)
        ln(knee, foot)
        ax.add_patch(Circle(head_c, HEAD_R, facecolor="white", edgecolor=c, lw=lw * 0.85, zorder=4))


def floor_panel(ax, kind, variant="ok", step_no=None, caption=None, mistake=False,
                 xlim=(-1.6, 1.6), ylim=(-0.15, 1.5)):
    draw_floor(ax, kind, variant=variant, mistake=mistake)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    if step_no is not None:
        badge_color = BAD if mistake else BRAND_DARK
        ax.add_patch(Circle((xlim[0] + 0.22, ylim[1] - 0.18), 0.145, facecolor=badge_color,
                              edgecolor="none", zorder=8))
        ax.text(xlim[0] + 0.22, ylim[1] - 0.18, str(step_no), color="white", fontsize=11,
                fontweight="bold", ha="center", va="center", zorder=9)
    if caption:
        ax.text((xlim[0] + xlim[1]) / 2, ylim[0] + 0.02, caption, ha="center", va="bottom",
                fontsize=10.2, color=(BAD if mistake else INK),
                fontweight=("bold" if mistake else "normal"))


def make_floor_sequence(filename, steps, mistake_panels=None, fig_w=9.6, panel_h=2.35, title=None):
    """steps: list of (kind, variant, caption)."""
    n_correct = len(steps)
    n_wrong = len(mistake_panels) if mistake_panels else 0
    ncols = max(n_correct, n_wrong, 1)
    nrows = 2 if n_wrong else 1

    fig = plt.figure(figsize=(fig_w, panel_h * nrows + (0.55 if title else 0)))
    gs = fig.add_gridspec(nrows, ncols, wspace=0.05, hspace=0.30,
                           top=0.82 if title else 0.98, bottom=0.03, left=0.01, right=0.99)

    if n_correct == 1 and ncols > 1:
        ax = fig.add_subplot(gs[0, :])
        floor_panel(ax, steps[0][0], variant=steps[0][1], step_no=None, caption=steps[0][2],
                    xlim=(-1.6 * ncols / 2, 1.6 * ncols / 2))
    else:
        for i, (kind, variant, cap) in enumerate(steps):
            ax = fig.add_subplot(gs[0, i])
            floor_panel(ax, kind, variant=variant, step_no=i + 1, caption=cap)

    if mistake_panels:
        offset = (ncols - n_wrong) / 2.0
        for i, (kind, variant, cap) in enumerate(mistake_panels):
            col = int(round(offset + i))
            ax = fig.add_subplot(gs[1, col]) if ncols > 1 else fig.add_subplot(gs[1, 0])
            floor_panel(ax, kind, variant=variant, caption="✕ " + cap, mistake=True)

    if title:
        fig.suptitle(title, fontsize=13.5, fontweight="bold", color=BRAND_DARK, y=0.97)

    fig.savefig(filename, dpi=200, facecolor="white")
    plt.close(fig)
    print("saved", filename)


def make_sequence(filename, steps, mistake_panels=None, fig_w=9.6, panel_h=3.05, title=None):
    """steps: list of (pose_dict, caption). mistake_panels: list of (pose_dict, caption, [mistake kinds])."""
    n_correct = len(steps)
    n_wrong = len(mistake_panels) if mistake_panels else 0
    ncols = max(n_correct, 1)
    nrows = 2 if n_wrong else 1

    fig = plt.figure(figsize=(fig_w, panel_h * nrows + (0.55 if title else 0)))
    gs = fig.add_gridspec(nrows, ncols, wspace=0.05, hspace=0.25,
                           top=0.86 if title else 0.98, bottom=0.02, left=0.01, right=0.99)

    for i, (p, cap) in enumerate(steps):
        ax = fig.add_subplot(gs[0, i])
        panel(ax, p, step_no=i + 1, caption=cap)

    if mistake_panels:
        # center the mistake panels in row 2
        offset = (ncols - n_wrong) / 2.0
        for i, (p, cap, mk) in enumerate(mistake_panels):
            col = offset + i
            ax = fig.add_subplot(gs[1, int(round(col))]) if ncols > 1 else fig.add_subplot(gs[1, 0])
            panel(ax, p, caption="✕ " + cap, mistake=True, mistakes=mk)

    if title:
        fig.suptitle(title, fontsize=13.5, fontweight="bold", color=BRAND_DARK, y=0.98)

    fig.savefig(filename, dpi=200, facecolor="white")
    plt.close(fig)
    print("saved", filename)
