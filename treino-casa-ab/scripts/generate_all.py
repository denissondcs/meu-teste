import sys
sys.path.insert(0, ".")
from stickman import make_sequence, make_floor_sequence, panel, floor_panel, draw_floor, draw_pose
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from stickman import BRAND, BRAND_DARK, BAD, INK

OUT = "out/"
import os
os.makedirs(OUT, exist_ok=True)

# ============================================================= AGACHAMENTO
p_stand = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=4,
               shoulder_angle=6, elbow_angle=6)
p_desc = dict(front_ankle=(0, 0), front_shin=22, front_thigh=35, torso_angle=22,
              shoulder_angle=70, elbow_angle=95, object="dumbbell", shoulder_angle2=70, elbow_angle2=95)
p_bottom = dict(front_ankle=(0, 0), front_shin=38, front_thigh=70, torso_angle=32,
                shoulder_angle=78, elbow_angle=100, object="dumbbell", shoulder_angle2=78, elbow_angle2=100)
p_up = dict(front_ankle=(0, 0), front_shin=10, front_thigh=12, torso_angle=8,
            shoulder_angle=30, elbow_angle=60, object="dumbbell", shoulder_angle2=30, elbow_angle2=60)
p_valgus = dict(front_ankle=(0, 0), front_shin=40, front_thigh=68, torso_angle=30,
                shoulder_angle=76, elbow_angle=100, object="dumbbell", shoulder_angle2=76, elbow_angle2=100)
p_round = dict(front_ankle=(0, 0), front_shin=30, front_thigh=60, torso_angle=55,
               shoulder_angle=95, elbow_angle=110, object="dumbbell", shoulder_angle2=95, elbow_angle2=110)
make_sequence(OUT + "agachamento.png",
    [(p_stand, "1. Em pe, pes na largura\ndos ombros, peito aberto"),
     (p_desc, "2. Quadril vai para\ntras e para baixo"),
     (p_bottom, "3. Coxas paralelas ao chao,\njoelho alinhado ao pe"),
     (p_up, "4. Sobe empurrando o\nchao com os pes")],
    [(p_valgus, "Joelho cai para\ndentro (valgo)", ["knee"]),
     (p_round, "Coluna curva\npara frente", [])],
    title="AGACHAMENTO (livre / Goblet)")

# ============================================================= LEVANTAMENTO TERRA ROMENO / RDL
r_top = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=4,
             shoulder_angle=8, elbow_angle=5, object="dumbbell", shoulder_angle2=8, elbow_angle2=5)
r_mid = dict(front_ankle=(0, 0), front_shin=6, front_thigh=-16, torso_angle=48,
             shoulder_angle=10, elbow_angle=6, object="dumbbell", shoulder_angle2=10, elbow_angle2=6)
r_bottom = dict(front_ankle=(0, 0), front_shin=8, front_thigh=-20, torso_angle=70,
                shoulder_angle=10, elbow_angle=6, object="dumbbell", shoulder_angle2=10, elbow_angle2=6)
r_lockout = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=-4,
                  shoulder_angle=6, elbow_angle=4, object="dumbbell", shoulder_angle2=6, elbow_angle2=4)
r_round = dict(front_ankle=(0, 0), front_shin=8, front_thigh=-6, torso_angle=85,
               shoulder_angle=10, elbow_angle=6, object="dumbbell", shoulder_angle2=10, elbow_angle2=6)
r_squatty = dict(front_ankle=(0, 0), front_shin=45, front_thigh=15, torso_angle=25,
                 shoulder_angle=55, elbow_angle=70, object="dumbbell", shoulder_angle2=55, elbow_angle2=70)
make_sequence(OUT + "rdl.png",
    [(r_top, "1. Em pe, halteres\nna frente das coxas"),
     (r_mid, "2. Quadril vai para tras,\nhalteres deslizam nas pernas"),
     (r_bottom, "3. Tronco quase paralelo\nao chao, costas retas"),
     (r_lockout, "4. Estende o quadril,\naperta o gluteo em pe")],
    [(r_round, "Coluna arredonda\n(\"pegar do chao errado\")", []),
     (r_squatty, "Dobra o joelho em vez\ndo quadril (virou agachamento)", [])],
    title="LEVANTAMENTO TERRA ROMENO / RDL")

# ============================================================= AFUNDO
l_stand = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=4,
               shoulder_angle=6, elbow_angle=6)
l_step = dict(front_ankle=(0.55, 0), front_shin=8, front_thigh=30, torso_angle=6,
              shoulder_angle=6, elbow_angle=6)
l_bottom = dict(front_ankle=(0.55, 0), front_shin=10, front_thigh=55, torso_angle=6,
                shoulder_angle=6, elbow_angle=6)
l_knee = dict(front_ankle=(0.55, 0), front_shin=42, front_thigh=45, torso_angle=8,
              shoulder_angle=6, elbow_angle=6)
l_lean = dict(front_ankle=(0.55, 0), front_shin=10, front_thigh=55, torso_angle=35,
              shoulder_angle=40, elbow_angle=30)
make_sequence(OUT + "afundo.png",
    [(l_stand, "1. Em pe, tronco ereto"),
     (l_step, "2. Passo a frente,\ndesce na vertical\n(perna de tras se estende)"),
     (l_bottom, "3. Joelho de tras quase\ntoca o chao, tronco ereto")],
    [(l_knee, "Joelho da frente passa\nmuito da ponta do pe", ["knee"]),
     (l_lean, "Tronco inclina\npara frente", [])],
    title="AFUNDO (alternado / bulgaro)")

# ============================================================= REMADA CURVADA
w_setup = dict(front_ankle=(0, 0), front_shin=6, front_thigh=-10, torso_angle=50,
               shoulder_angle=8, elbow_angle=5, object="dumbbell", shoulder_angle2=8, elbow_angle2=5)
w_pull = dict(front_ankle=(0, 0), front_shin=6, front_thigh=-10, torso_angle=50,
              shoulder_angle=-30, elbow_angle=-75, object="dumbbell", shoulder_angle2=-30, elbow_angle2=-75)
w_round = dict(front_ankle=(0, 0), front_shin=6, front_thigh=-10, torso_angle=75,
               shoulder_angle=8, elbow_angle=5, object="dumbbell", shoulder_angle2=8, elbow_angle2=5)
w_momentum = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=10,
                   shoulder_angle=-15, elbow_angle=-60, object="dumbbell", shoulder_angle2=-15, elbow_angle2=-60)
make_sequence(OUT + "remada.png",
    [(w_setup, "1. Tronco a ~45 graus,\nbracos esticados"),
     (w_pull, "2. Puxa os cotovelos\npara tras/cima")],
    [(w_round, "Costas\narredondam", []),
     (w_momentum, "Usa impulso do corpo\npara levantar o peso", [])],
    title="REMADA CURVADA", fig_w=7.2)

# ============================================================= AGACHAMENTO COM SALTO
j_load = dict(front_ankle=(0, 0), front_shin=26, front_thigh=48, torso_angle=25,
              shoulder_angle=-60, elbow_angle=-30)
j_fly = dict(front_ankle=(0, 0.55), front_shin=8, front_thigh=8, torso_angle=4,
             shoulder_angle=-20, elbow_angle=-10)
j_land = dict(front_ankle=(0, 0), front_shin=24, front_thigh=46, torso_angle=22,
              shoulder_angle=-40, elbow_angle=-15)
j_hard = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=4,
              shoulder_angle=-10, elbow_angle=-5)
make_sequence(OUT + "jump_squat.png",
    [(j_load, "1. Agacha para\nganhar impulso"),
     (j_fly, "2. Salta explosivo,\nestica o corpo no ar"),
     (j_land, "3. Aterrissa \"macio\",\ndobrando os joelhos")],
    [(j_hard, "Aterrissa com as pernas\nesticadas e travadas", [])],
    title="AGACHAMENTO COM SALTO (jump squat)", fig_w=7.6)

# ============================================================= LEVANTAMENTO E ABRACO
b_down = dict(front_ankle=(0, 0), front_shin=28, front_thigh=62, torso_angle=20,
              shoulder_angle=-95, elbow_angle=-10, object="backpack")
b_hug = dict(front_ankle=(0, 0), front_shin=28, front_thigh=62, torso_angle=15,
             shoulder_angle=-140, elbow_angle=10, object="backpack")
b_rise = dict(front_ankle=(0, 0), front_shin=12, front_thigh=20, torso_angle=8,
              shoulder_angle=-140, elbow_angle=10, object="backpack")
b_stand = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=4,
               shoulder_angle=-140, elbow_angle=10, object="backpack")
b_backround = dict(front_ankle=(0, 0), front_shin=10, front_thigh=15, torso_angle=55,
                    shoulder_angle=-130, elbow_angle=10, object="backpack")
b_far = dict(front_ankle=(0, 0), front_shin=6, front_thigh=6, torso_angle=6,
             shoulder_angle=58, elbow_angle=18, object="backpack")
make_sequence(OUT + "levantamento_abraco.png",
    [(b_down, "1. Agacha bem perto,\ndobrando quadril e joelhos"),
     (b_hug, "2. Abraca o peso\njunto ao peito"),
     (b_rise, "3. Sobe usando\nas pernas"),
     (b_stand, "4. Em pe, tronco ereto,\npronto para andar")],
    [(b_backround, "Levanta curvando\na coluna", []),
     (b_far, "Segura o peso longe\ndo corpo", [])],
    title="LEVANTAMENTO E ABRACO (bear hug lift)")

# ============================================================= FARMER'S CARRY
f_ok = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=2,
            shoulder_angle=4, elbow_angle=3, object="dumbbell", shoulder_angle2=4, elbow_angle2=3)
f_slump = dict(front_ankle=(0, 0), front_shin=4, front_thigh=4, torso_angle=22,
               shoulder_angle=14, elbow_angle=8, object="dumbbell", shoulder_angle2=14, elbow_angle2=8)
make_sequence(OUT + "farmers_carry.png",
    [(f_ok, "Ombros para tras, peito aberto,\npasso curto e firme, halteres perto do corpo")],
    [(f_slump, "Ombros caem para frente,\nperde a postura ereta", [])],
    title="FARMER'S CARRY", fig_w=6.4, panel_h=3.05)

# ============================================================= FLEXAO DE BRACO (custom floor)
def pushup_points(variant):
    if variant == "top":
        return dict(shoulder=(-0.55, 0.85), elbow=None, hand=(-0.55, 0.32),
                     hip=(0.35, 0.85), ankle=(1.35, 0.32), head=(-0.85, 0.90))
    if variant == "bottom":
        return dict(shoulder=(-0.50, 0.52), elbow=(-0.74, 0.46), hand=(-0.55, 0.32),
                     hip=(0.35, 0.60), ankle=(1.35, 0.32), head=(-0.80, 0.57))
    if variant == "sag":
        return dict(shoulder=(-0.55, 0.72), elbow=None, hand=(-0.55, 0.32),
                     hip=(0.35, 0.42), ankle=(1.35, 0.32), head=(-0.85, 0.77))
    if variant == "pike":
        return dict(shoulder=(-0.55, 0.68), elbow=None, hand=(-0.55, 0.32),
                     hip=(0.35, 1.08), ankle=(1.35, 0.32), head=(-0.85, 0.73))

def draw_pushup(ax, variant):
    c = BRAND if variant in ("top", "bottom") else BAD
    pts = pushup_points(variant)
    lw = 3.2
    ax.axhline(0.32, color="#c9cdd3", lw=1.4, zorder=1)
    ax.plot([pts["shoulder"][0], pts["hip"][0]], [pts["shoulder"][1], pts["hip"][1]], color=c, lw=lw,
             solid_capstyle="round", zorder=3)
    ax.plot([pts["hip"][0], pts["ankle"][0]], [pts["hip"][1], pts["ankle"][1]], color=c, lw=lw,
             solid_capstyle="round", zorder=3)
    if pts["elbow"] is None:
        ax.plot([pts["shoulder"][0], pts["hand"][0]], [pts["shoulder"][1], pts["hand"][1]], color=c, lw=lw,
                 solid_capstyle="round", zorder=3)
    else:
        ax.plot([pts["shoulder"][0], pts["elbow"][0]], [pts["shoulder"][1], pts["elbow"][1]], color=c, lw=lw,
                 solid_capstyle="round", zorder=3)
        ax.plot([pts["elbow"][0], pts["hand"][0]], [pts["elbow"][1], pts["hand"][1]], color=c, lw=lw,
                 solid_capstyle="round", zorder=3)
    ax.plot([pts["ankle"][0], pts["ankle"][0] + 0.16], [pts["ankle"][1] - 0.03, pts["ankle"][1] + 0.12],
             color=c, lw=lw, solid_capstyle="round", zorder=3)
    ax.add_patch(Circle(pts["head"], 0.19, facecolor="white", edgecolor=c, lw=lw * 0.85, zorder=4))
    if variant == "sag":
        from matplotlib.patches import Arc
        ax.add_patch(Arc((0.0, 0.62), 0.7, 0.4, angle=0, theta1=200, theta2=345, color=BAD, lw=2.4, zorder=6))
    elif variant == "pike":
        from matplotlib.patches import Arc
        ax.add_patch(Arc((0.0, 0.95), 0.7, 0.4, angle=180, theta1=200, theta2=345, color=BAD, lw=2.4, zorder=6))

def pushup_panel(ax, variant, step_no=None, caption=None, mistake=False):
    draw_pushup(ax, variant)
    ax.set_xlim(-1.6, 1.6)
    ax.set_ylim(-0.15, 1.5)
    ax.set_aspect("equal")
    ax.axis("off")
    if step_no is not None:
        badge_color = BAD if mistake else BRAND_DARK
        ax.add_patch(Circle((-1.6 + 0.22, 1.5 - 0.18), 0.145, facecolor=badge_color, edgecolor="none", zorder=8))
        ax.text(-1.6 + 0.22, 1.5 - 0.18, str(step_no), color="white", fontsize=11, fontweight="bold",
                ha="center", va="center", zorder=9)
    if caption:
        ax.text(0, -0.13, caption, ha="center", va="bottom", fontsize=10.2,
                color=(BAD if mistake else INK), fontweight=("bold" if mistake else "normal"))

fig = plt.figure(figsize=(9.6, 2.35 * 2 + 0.55))
gs = fig.add_gridspec(2, 2, wspace=0.05, hspace=0.30, top=0.82, bottom=0.03, left=0.05, right=0.95)
pushup_panel(fig.add_subplot(gs[0, 0]), "top", 1, "1. Prancha alta, maos\nabaixo dos ombros")
pushup_panel(fig.add_subplot(gs[0, 1]), "bottom", 2, "2. Cotovelos a ~45,\nquase toca o chao")
pushup_panel(fig.add_subplot(gs[1, 0]), "sag", None, "✕ Quadril cai (lombar cede)", mistake=True)
pushup_panel(fig.add_subplot(gs[1, 1]), "pike", None, "✕ Quadril muito alto", mistake=True)
fig.suptitle("FLEXAO DE BRACO", fontsize=13.5, fontweight="bold", color=BRAND_DARK, y=0.97)
fig.savefig(OUT + "flexao.png", dpi=200, facecolor="white")
plt.close(fig)
print("saved flexao.png")

# ============================================================= PRANCHA FRONTAL
make_floor_sequence(OUT + "prancha.png",
    [("plank", "ok", "Corpo alinhado dos\nombros aos calcanhares")],
    [("plank", "sag", "Quadril cai (lombar cede)"),
     ("plank", "pike", "Quadril muito alto")],
    title="PRANCHA FRONTAL", fig_w=7.2)

# ============================================================= ELEVACAO PELVICA / PONTE DE GLUTEO
make_floor_sequence(OUT + "ponte.png",
    [("bridge", "down", "1. Deitado, joelhos\ndobrados, pes apoiados"),
     ("bridge", "up", "2. Sobe o quadril,\naperta o gluteo no topo")],
    [("bridge", "sag", "Hiperestende a lombar\n(sobe demais)")],
    title="ELEVACAO PELVICA (ponte de gluteo)", fig_w=7.2)

# ============================================================= DEAD BUG
make_floor_sequence(OUT + "deadbug.png",
    [("deadbug", "ok", "Lombar sempre encostada no chao\nbraco e perna opostos se estendem")],
    None, title="DEAD BUG", fig_w=5.6, panel_h=2.5)

# ============================================================= ABDOMINAL SUPRA
make_floor_sequence(OUT + "crunch.png",
    [("crunch", "down", "1. Deitado, joelhos\ndobrados"),
     ("crunch", "up", "2. Sobe so ate tirar\nas escapulas do chao")],
    None, title="ABDOMINAL SUPRA (crunch)", fig_w=6.0, panel_h=2.5)

print("done")
