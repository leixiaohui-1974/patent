"""
PF3系列专利配图生成脚本
PF3：安全边界与ODD管理（5件）
每件生成3张图
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import os

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

BLUE = '#1565C0'
GREEN = '#4CAF50'
PURPLE = '#7B1FA2'
ORANGE = '#FF7043'
GRAY = '#9E9E9E'
LIGHT_BLUE = '#BBDEFB'
LIGHT_GREEN = '#C8E6C9'
LIGHT_PURPLE = '#E1BEE7'
LIGHT_ORANGE = '#FFCCBC'
RED = '#D32F2F'
YELLOW = '#FFC107'

outdir = os.path.dirname(os.path.abspath(__file__))

def save(fig, name):
    fig.savefig(os.path.join(outdir, name), dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved {name}")

# ===== PF3-1: Dynamic Safety Boundaries =====
def pf3_1_fig1():
    """三色动态安全边界示意"""
    fig, ax = plt.subplots(figsize=(10, 6))
    t = np.linspace(0, 72, 500)

    # Design level and dynamic boundaries
    design = 62.5 * np.ones_like(t)
    # Seasonal adjustment: boundaries widen slightly in non-flood
    season_factor = 1.0 + 0.1 * np.sin(2*np.pi*t/72)  # simplified

    green_up = 63.2 * season_factor
    green_dn = 61.8 / season_factor
    yellow_up = 63.8 * season_factor
    yellow_dn = 61.2 / season_factor
    red_up = 64.5 * np.ones_like(t)
    red_dn = 60.5 * np.ones_like(t)

    # Actual water level with some events
    level = 62.5 + 0.3*np.sin(0.2*t) + np.random.normal(0, 0.05, len(t))
    # Event at t=24: level rises toward yellow
    idx24 = np.argmin(np.abs(t-24))
    for i in range(idx24, min(idx24+80, len(t))):
        level[i] += 0.8 * np.exp(-0.03*(t[i]-24))

    ax.fill_between(t, red_dn, yellow_dn, alpha=0.15, color=RED, label='Red zone (emergency)')
    ax.fill_between(t, yellow_dn, green_dn, alpha=0.15, color=YELLOW, label='Yellow zone (warning)')
    ax.fill_between(t, green_dn, green_up, alpha=0.15, color=GREEN, label='Green zone (normal)')
    ax.fill_between(t, green_up, yellow_up, alpha=0.15, color=YELLOW)
    ax.fill_between(t, yellow_up, red_up, alpha=0.15, color=RED)

    ax.plot(t, level, color=BLUE, linewidth=1.5, label='Actual level')
    ax.plot(t, design, 'k--', linewidth=1, alpha=0.5, label='Design level')
    ax.plot(t, green_up, '-', color=GREEN, linewidth=1, alpha=0.7)
    ax.plot(t, green_dn, '-', color=GREEN, linewidth=1, alpha=0.7)
    ax.plot(t, yellow_up, '-', color=YELLOW, linewidth=1, alpha=0.7)
    ax.plot(t, yellow_dn, '-', color=YELLOW, linewidth=1, alpha=0.7)
    ax.plot(t, red_up, '-', color=RED, linewidth=1.5, alpha=0.7)
    ax.plot(t, red_dn, '-', color=RED, linewidth=1.5, alpha=0.7)

    ax.set_xlabel('Time (h)', fontsize=11)
    ax.set_ylabel('Water level (m)', fontsize=11)
    ax.set_title('PF3-1 Fig 1: Three-color dynamic safety boundary', fontsize=13, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 72)

    save(fig, 'PF3-1_fig1.png')

def pf3_1_fig2():
    """Safety boundary adaptive adjustment flow"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF3-1 Fig 2: Safety boundary adaptive adjustment process', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('S1\nMonitor', 'Real-time SCADA\ndata collection', BLUE, 0.5, 4.5),
        ('S2\nContext', 'Season/flow/\nequipment state', GREEN, 3.0, 4.5),
        ('S3\nCalculate', 'Boundary formula\nadjustment', PURPLE, 5.5, 4.5),
        ('S4\nValidate', 'History check\n+ safety verify', ORANGE, 8.0, 4.5),
        ('S5\nUpdate', 'Push new\nboundaries', BLUE, 3.0, 1.5),
        ('S6\nLearn', 'Near-miss event\nlibrary update', GREEN, 5.5, 1.5),
    ]

    for title, desc, color, x, y in steps:
        rect = FancyBboxPatch((x, y), 2.0, 1.8, boxstyle="round,pad=0.1",
                               facecolor=f'{color}22', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+1.0, y+1.3, title, ha='center', va='center', fontsize=10, fontweight='bold', color=color)
        ax.text(x+1.0, y+0.5, desc, ha='center', va='center', fontsize=8)

    # Arrows
    for (x1,y1), (x2,y2) in [((2.5,5.4),(3.0,5.4)), ((5.0,5.4),(5.5,5.4)), ((7.5,5.4),(8.0,5.4)),
                               ((8.0,4.5),(5.5,3.3)), ((5.0,2.4),(3.0,2.4))]:
        ax.annotate('', xy=(x2,y2), xytext=(x1,y1), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))

    # Loop
    ax.annotate('Continuous\ncycle', xy=(0.5, 5.4), xytext=(3.0, 1.5),
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=1, linestyle='dashed', connectionstyle='arc3,rad=0.5'),
               fontsize=8, color=GRAY)

    save(fig, 'PF3-1_fig2.png')

def pf3_1_fig3():
    """Performance comparison: static vs dynamic boundaries"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('PF3-1 Fig 3: Static vs dynamic boundary performance', fontsize=13, fontweight='bold')

    categories = ['False\nalarms', 'Missed\nevents', 'Response\ntime (min)', 'Operator\ninterventions']
    static_vals = [15, 3, 8.5, 120]
    dynamic_vals = [3, 1, 2.1, 35]

    x = np.arange(len(categories))
    ax1.bar(x-0.2, static_vals, 0.35, color=GRAY, alpha=0.7, label='Static boundary')
    ax1.bar(x+0.2, dynamic_vals, 0.35, color=GREEN, alpha=0.8, label='Dynamic boundary')
    ax1.set_xticks(x)
    ax1.set_xticklabels(categories, fontsize=9)
    ax1.set_ylabel('Count / Minutes', fontsize=10)
    ax1.legend(fontsize=9)
    ax1.set_title('Monthly metrics comparison', fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')

    # Boundary adaptation over seasons
    months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
    static_width = [1.4]*12
    dynamic_width = [1.6, 1.5, 1.4, 1.3, 1.2, 1.0, 0.9, 0.9, 1.0, 1.2, 1.4, 1.5]

    ax2.plot(months, static_width, 'o--', color=GRAY, linewidth=1.5, label='Static green zone width')
    ax2.plot(months, dynamic_width, 's-', color=GREEN, linewidth=2, label='Dynamic green zone width')
    ax2.set_ylabel('Green zone width (m)', fontsize=10)
    ax2.set_title('Seasonal boundary adaptation', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)
    ax2.tick_params(axis='x', rotation=45)

    plt.tight_layout()
    save(fig, 'PF3-1_fig3.png')

# ===== PF3-2: ODD Formal Definition =====
def pf3_2_fig1():
    """ODD multi-dimensional boundary visualization"""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_xlim(-1.5, 1.5)
    ax.set_ylim(-1.5, 1.5)
    ax.set_aspect('equal')
    ax.set_title('PF3-2 Fig 1: ODD boundary in normalized parameter space', fontsize=13, fontweight='bold')

    # Concentric boundaries
    angles = np.linspace(0, 2*np.pi, 100)

    # Verified ODD (solid green)
    r_verified = 0.7 + 0.1*np.sin(3*angles)
    ax.fill(r_verified*np.cos(angles), r_verified*np.sin(angles), alpha=0.2, color=GREEN)
    ax.plot(r_verified*np.cos(angles), r_verified*np.sin(angles), color=GREEN, linewidth=2, label='Verified ODD')

    # Candidate ODD (dashed yellow)
    r_candidate = 1.0 + 0.05*np.sin(5*angles)
    ax.plot(r_candidate*np.cos(angles), r_candidate*np.sin(angles), '--', color=YELLOW, linewidth=2, label='Candidate ODD')

    # Unverified (dotted red)
    r_unverified = 1.3
    ax.plot(r_unverified*np.cos(angles), r_unverified*np.sin(angles), ':', color=RED, linewidth=2, label='Unverified boundary')

    # Current operating point
    ax.plot(0.2, 0.3, 'o', color=BLUE, markersize=12, label='Current state', zorder=5)
    ax.annotate('d=0.73\n(safe)', xy=(0.2, 0.3), xytext=(0.6, 0.8),
               arrowprops=dict(arrowstyle='->', color=BLUE), fontsize=10, fontweight='bold', color=BLUE)

    # Warning point
    ax.plot(-0.5, 0.5, '^', color=ORANGE, markersize=10, label='Warning state', zorder=5)
    ax.annotate('d=0.18\n(warning!)', xy=(-0.5, 0.5), xytext=(-1.1, 1.0),
               arrowprops=dict(arrowstyle='->', color=ORANGE), fontsize=10, fontweight='bold', color=ORANGE)

    ax.set_xlabel('Flow dimension (normalized)', fontsize=10)
    ax.set_ylabel('Equipment dimension (normalized)', fontsize=10)
    ax.legend(fontsize=9, loc='lower right')
    ax.grid(True, alpha=0.3)

    save(fig, 'PF3-2_fig1.png')

def pf3_2_fig2():
    """ODD distance monitoring timeline"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle('PF3-2 Fig 2: ODD distance real-time monitoring', fontsize=13, fontweight='bold')

    t = np.linspace(0, 48, 500)
    # ODD distance
    d = 0.7 + 0.1*np.sin(0.3*t) + np.random.normal(0, 0.02, len(t))
    # Event at t=20: approach ODD boundary
    idx20 = np.argmin(np.abs(t-20))
    for i in range(idx20, min(idx20+100, len(t))):
        d[i] -= 0.5 * np.exp(-0.05*(t[i]-20)) * (1 - np.exp(-0.3*(t[i]-20)))
    d = np.maximum(d, 0.05)

    ax1.plot(t, d, color=BLUE, linewidth=1.5)
    ax1.axhline(y=0.3, color=YELLOW, linestyle='--', linewidth=1.5, label='Yellow warning (d<0.3)')
    ax1.axhline(y=0.1, color=RED, linestyle='--', linewidth=1.5, label='Auto downgrade (d<0.1)')
    ax1.fill_between(t, 0, 0.1, alpha=0.1, color=RED)
    ax1.fill_between(t, 0.1, 0.3, alpha=0.1, color=YELLOW)
    ax1.set_ylabel('ODD distance d', fontsize=10)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    ax1.set_ylim(0, 1.0)

    # WNAL level
    wnal = np.where(d > 0.3, 3, np.where(d > 0.1, 2, 1))
    ax2.step(t, wnal, color=PURPLE, linewidth=2, where='post')
    ax2.set_ylabel('WNAL level', fontsize=10)
    ax2.set_xlabel('Time (h)', fontsize=10)
    ax2.set_yticks([1, 2, 3])
    ax2.set_yticklabels(['L1', 'L2', 'L3'])
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(0.5, 3.5)

    plt.tight_layout()
    save(fig, 'PF3-2_fig2.png')

def pf3_2_fig3():
    """ODD parameter space and xIL verification"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF3-2 Fig 3: ODD verification and expansion protocol', fontsize=13, fontweight='bold', pad=15)

    # ODD definition box
    rect = FancyBboxPatch((0.3, 3.5), 3.0, 3.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
    ax.add_patch(rect)
    ax.text(1.8, 6.0, 'ODD Definition', ha='center', fontsize=11, fontweight='bold', color=GREEN)
    dims = ['Flow: [50,150] m3/s', 'WQ: pH [6.5,8.5]', 'Weather: T>-5C', 'Equip: >90% avail',
            'Comms: <1% loss', 'Season: all', 'Demand: [30,120]%', 'Time: 24/7']
    for i, d in enumerate(dims):
        ax.text(0.5, 5.5 - i*0.3, d, fontsize=7, color=GREEN)

    # xIL verification
    rect = FancyBboxPatch((4.0, 3.5), 2.5, 3.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5.25, 6.0, 'xIL Verification', ha='center', fontsize=11, fontweight='bold', color=BLUE)
    ax.text(5.25, 5.3, 'MiL: 1000 scenarios', ha='center', fontsize=8)
    ax.text(5.25, 4.8, 'SiL: 500 scenarios', ha='center', fontsize=8)
    ax.text(5.25, 4.3, 'HiL: 100 scenarios', ha='center', fontsize=8)
    ax.text(5.25, 3.8, 'Pass rate > 99.5%', ha='center', fontsize=9, fontweight='bold', color=GREEN)

    # Expansion protocol
    rect = FancyBboxPatch((7.2, 3.5), 2.5, 3.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
    ax.add_patch(rect)
    ax.text(8.45, 6.0, 'ODD Expansion', ha='center', fontsize=11, fontweight='bold', color=PURPLE)
    ax.text(8.45, 5.3, '90-day trial at\nboundary', ha='center', fontsize=8)
    ax.text(8.45, 4.5, 'Zero safety events\nrequired', ha='center', fontsize=8)
    ax.text(8.45, 3.8, 'Expand by 5%', ha='center', fontsize=9, fontweight='bold', color=PURPLE)

    # Arrows
    ax.annotate('', xy=(4.0, 5.0), xytext=(3.3, 5.0), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))
    ax.annotate('', xy=(7.2, 5.0), xytext=(6.5, 5.0), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))

    # Bottom: timeline
    ax.text(5.0, 2.5, 'ODD lifecycle: Define -> Verify (xIL) -> Deploy -> Monitor -> Expand -> Re-verify',
            ha='center', fontsize=9, color=GRAY,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor=GRAY))

    save(fig, 'PF3-2_fig3.png')

# ===== PF3-3: Multi-level Safety Interlocks =====
def pf3_3_fig1():
    """Four-level interlock architecture"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF3-3 Fig 1: Four-level safety interlock hierarchy', fontsize=13, fontweight='bold', pad=15)

    levels = [
        ('L3: Human\nIntervention', '>minutes', 'Decision support\n+ notification', LIGHT_PURPLE, PURPLE),
        ('L2: Coordinated\nProtection', 'minutes', 'Multi-pool\ncoordinated response', LIGHT_BLUE, BLUE),
        ('L1: Auto Safety\nActions', 'seconds', 'Pattern detection\n-> preset response', LIGHT_GREEN, GREEN),
        ('L0: PLC Hardwired\nInterlocks', 'milliseconds', 'Absolute limits\n-> emergency action', LIGHT_ORANGE, ORANGE),
    ]

    for i, (name, time, desc, bg, fg) in enumerate(levels):
        y = 1.0 + i * 1.6
        w = 9.0 - i * 0.3
        x = 0.5 + i * 0.15

        rect = FancyBboxPatch((x, y), w, 1.3, boxstyle="round,pad=0.1",
                               facecolor=bg, edgecolor=fg, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+1.2, y+0.65, name, ha='center', va='center', fontsize=10, fontweight='bold', color=fg)
        ax.text(x+3.5, y+0.65, f'Response: {time}', ha='center', va='center', fontsize=9, color=fg)
        ax.text(x+w-1.5, y+0.65, desc, ha='center', va='center', fontsize=8, color=fg)

    # Independence annotation
    ax.text(9.5, 4.0, 'Each level\noperates\nindependently', fontsize=9, fontweight='bold', color=RED,
            ha='center', rotation=90,
            bbox=dict(boxstyle='round,pad=0.3', facecolor='#FFCDD2', edgecolor=RED))

    ax.text(5.0, 0.5, 'Key principle: lower levels NEVER depend on higher levels',
            fontsize=10, ha='center', color=RED, fontweight='bold')

    save(fig, 'PF3-3_fig1.png')

def pf3_3_fig2():
    """Pipe burst scenario response timeline"""
    fig, ax = plt.subplots(figsize=(10, 5))

    events = [
        (0.05, 'L0: Pressure drop\ndetected', ORANGE, 'L0'),
        (0.2, 'L0: Isolation valve\nclosed', ORANGE, ''),
        (3, 'L1: Burst location\nidentified', GREEN, 'L1'),
        (5, 'L1: Upstream flow\nadjusted', GREEN, ''),
        (30, 'L2: 5-pool coordinated\nresponse', BLUE, 'L2'),
        (120, 'L2: System\nstabilized', BLUE, ''),
        (300, 'L3: Operator notified\nwith assessment', PURPLE, 'L3'),
    ]

    ax.set_xlim(-10, 400)
    ax.set_ylim(-0.5, 4.5)
    ax.set_title('PF3-3 Fig 2: Pipe burst multi-level response timeline', fontsize=13, fontweight='bold')

    # Timeline
    ax.axhline(y=0, color=GRAY, linewidth=2)

    y_map = {'L0': 0.8, 'L1': 1.8, 'L2': 2.8, 'L3': 3.8}

    for t_val, label, color, level in events:
        y = y_map.get(level, 0.8)
        ax.plot(t_val, 0, 'v', color=color, markersize=10)
        ax.plot([t_val, t_val], [0, y], '-', color=color, linewidth=1, alpha=0.5)
        ax.text(t_val, y+0.15, label, ha='center', fontsize=8, color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color, alpha=0.8))

    ax.set_xlabel('Time (seconds)', fontsize=10)
    ax.set_yticks([])

    # Level labels on left
    for level, y in y_map.items():
        ax.text(-8, y, level, fontsize=10, fontweight='bold', ha='right',
                color={'L0':ORANGE,'L1':GREEN,'L2':BLUE,'L3':PURPLE}[level])

    ax.grid(True, alpha=0.2, axis='x')
    save(fig, 'PF3-3_fig2.png')

def pf3_3_fig3():
    """Interlock testing requirements"""
    fig, ax = plt.subplots(figsize=(8, 6))

    levels = ['L0\nPLC', 'L1\nAuto', 'L2\nCoord', 'L3\nHuman']
    test_freq = [12, 4, 2, 1]  # times per year
    response_req = [0.2, 3, 120, 600]  # seconds

    colors = [ORANGE, GREEN, BLUE, PURPLE]

    ax2 = ax.twinx()
    bars = ax.bar(np.arange(4)-0.15, test_freq, 0.3, color=colors, alpha=0.7, label='Test frequency (/year)')
    line = ax2.semilogy(np.arange(4)+0.15, response_req, 'D-', color=RED, markersize=10, linewidth=2, label='Response requirement (s)')

    ax.set_xticks(np.arange(4))
    ax.set_xticklabels(levels, fontsize=11)
    ax.set_ylabel('Test frequency (times/year)', fontsize=10)
    ax2.set_ylabel('Max response time (s)', fontsize=10, color=RED)
    ax2.tick_params(axis='y', labelcolor=RED)

    ax.set_title('PF3-3 Fig 3: Interlock testing requirements', fontsize=13, fontweight='bold')

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, fontsize=9, loc='upper right')

    ax.grid(True, alpha=0.3, axis='y')
    save(fig, 'PF3-3_fig3.png')

# ===== PF3-4: Scenario Library Diagnosis =====
def pf3_4_fig1():
    """Scenario matching architecture"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF3-4 Fig 1: Scenario-based auto-diagnosis architecture', fontsize=13, fontweight='bold', pad=15)

    # Input: SCADA data
    rect = FancyBboxPatch((0.3, 3.5), 2.0, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(rect)
    ax.text(1.3, 5.0, 'SCADA\nReal-time data', ha='center', fontsize=10, fontweight='bold', color=BLUE)
    ax.text(1.3, 3.9, 'Feature\nextraction', ha='center', fontsize=8)

    # Scenario library
    rect = FancyBboxPatch((3.2, 2.5), 2.5, 3.5, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=2)
    ax.add_patch(rect)
    ax.text(4.45, 5.5, 'Scenario Library', ha='center', fontsize=11, fontweight='bold', color=GREEN)
    ax.text(4.45, 4.8, 'Category-Type-\nSeverity-Location', ha='center', fontsize=8)
    ax.text(4.45, 3.8, '500+ encoded\nscenarios', ha='center', fontsize=9, color=GREEN)
    ax.text(4.45, 3.0, 'Incremental\nlearning', ha='center', fontsize=8, color=ORANGE)

    # Matching engine
    rect = FancyBboxPatch((6.5, 3.5), 2.0, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
    ax.add_patch(rect)
    ax.text(7.5, 5.0, 'Similarity\nMatching', ha='center', fontsize=10, fontweight='bold', color=PURPLE)
    ax.text(7.5, 3.9, 'Cosine + DTW\nConfidence', ha='center', fontsize=8)

    # Output
    rect = FancyBboxPatch((6.5, 0.8), 3.0, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=2)
    ax.add_patch(rect)
    ax.text(8.0, 2.3, 'Response', ha='center', fontsize=10, fontweight='bold', color=ORANGE)
    ax.text(8.0, 1.5, '>0.85: Auto-execute\n0.6-0.85: Recommend\n<0.6: Flag unknown', ha='center', fontsize=8)

    # Arrows
    ax.annotate('', xy=(3.2, 4.5), xytext=(2.3, 4.5), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))
    ax.annotate('', xy=(6.5, 4.5), xytext=(5.7, 4.5), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))
    ax.annotate('', xy=(7.5, 3.5), xytext=(7.5, 2.8), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))

    # Feedback loop
    ax.annotate('Post-event\nupdate', xy=(5.7, 2.5), xytext=(7.0, 0.8),
               arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, linestyle='dashed', connectionstyle='arc3,rad=-0.3'),
               fontsize=8, color=GREEN)

    save(fig, 'PF3-4_fig1.png')

def pf3_4_fig2():
    """Scenario library growth over time"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('PF3-4 Fig 2: Scenario library growth and performance', fontsize=13, fontweight='bold')

    months = np.arange(0, 25)
    scenarios = 500 + 30 * months + np.random.randint(0, 10, len(months))

    ax1.plot(months, scenarios, 'o-', color=GREEN, linewidth=2, markersize=5)
    ax1.set_xlabel('Months since deployment', fontsize=10)
    ax1.set_ylabel('Scenario count', fontsize=10)
    ax1.set_title('Library growth', fontsize=11)
    ax1.grid(True, alpha=0.3)

    # Accuracy improvement
    accuracy = 0.75 + 0.2 * (1 - np.exp(-months/8)) + np.random.normal(0, 0.01, len(months))
    response_time = 12 - 8 * (1 - np.exp(-months/6)) + np.random.normal(0, 0.3, len(months))
    response_time = np.maximum(response_time, 2)

    ax2.plot(months, accuracy*100, 's-', color=BLUE, linewidth=2, markersize=5, label='Match accuracy (%)')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(months, response_time, 'D-', color=ORANGE, linewidth=2, markersize=5, label='Diagnosis time (s)')

    ax2.set_xlabel('Months', fontsize=10)
    ax2.set_ylabel('Accuracy (%)', fontsize=10, color=BLUE)
    ax2_twin.set_ylabel('Time (s)', fontsize=10, color=ORANGE)
    ax2.set_title('Performance improvement', fontsize=11)

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1+lines2, labels1+labels2, fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF3-4_fig2.png')

def pf3_4_fig3():
    """Scenario encoding example"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF3-4 Fig 3: Scenario encoding and classification system', fontsize=13, fontweight='bold', pad=15)

    # Level 1: Category
    categories = [('H', 'Hydraulic', BLUE), ('M', 'Mechanical', GREEN), ('E', 'Electrical', PURPLE), ('W', 'Weather', ORANGE)]
    for i, (code, name, color) in enumerate(categories):
        x = 0.5 + i * 2.4
        rect = FancyBboxPatch((x, 4.2), 2.0, 1.2, boxstyle="round,pad=0.1",
                               facecolor=f'{color}22', edgecolor=color, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+1.0, 4.9, f'{code}: {name}', ha='center', fontsize=9, fontweight='bold', color=color)
        ax.text(x+1.0, 4.5, f'{["OV/UF/LK/BL","GF/PF/VF","PO/CO/SF","FL/IC/DR"][i]}', ha='center', fontsize=7, color=color)

    ax.text(5.0, 5.6, 'Level 1: Category', fontsize=10, fontweight='bold', ha='center', color=GRAY)

    # Example encoding
    rect = FancyBboxPatch((1.5, 1.0), 7.0, 2.5, boxstyle="round,pad=0.1",
                           facecolor='lightyellow', edgecolor=GRAY, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(5.0, 3.0, 'Example: H-OV-2-P035', fontsize=12, fontweight='bold', ha='center', color=RED)
    ax.text(5.0, 2.4, 'H=Hydraulic | OV=Overflow | 2=Medium severity | P035=Pool 35', fontsize=9, ha='center')
    ax.text(5.0, 1.8, 'Feature vector: [dH/dt, dQ/dt, delta_P, ...] (12 dimensions)', fontsize=9, ha='center', color=GRAY)
    ax.text(5.0, 1.3, 'Matched response: Close upstream gate 20%, open downstream gate 10%, notify L2', fontsize=8, ha='center', color=GREEN)

    save(fig, 'PF3-4_fig3.png')

# ===== PF3-5: Reachability Analysis =====
def pf3_5_fig1():
    """Reachable set visualization"""
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.set_title('PF3-5 Fig 1: Backward reachable set and safety margin', fontsize=13, fontweight='bold')

    # Safe target set
    theta = np.linspace(0, 2*np.pi, 100)
    safe_x = 1.2 * np.cos(theta)
    safe_y = 1.0 * np.sin(theta)
    ax.fill(safe_x, safe_y, alpha=0.15, color=GREEN)
    ax.plot(safe_x, safe_y, color=GREEN, linewidth=2, label='Safe target set')

    # Backward reachable set (larger)
    reach_x = 1.8 * np.cos(theta) + 0.1*np.sin(3*theta)
    reach_y = 1.5 * np.sin(theta) + 0.1*np.cos(3*theta)
    ax.fill(reach_x, reach_y, alpha=0.1, color=BLUE)
    ax.plot(reach_x, reach_y, color=BLUE, linewidth=2, linestyle='--', label='Backward reachable set (6h)')

    # Current state (safe)
    ax.plot(0.3, 0.2, 'o', color=BLUE, markersize=15, zorder=5)
    ax.text(0.5, 0.4, 'Current\nmargin=0.73', fontsize=9, color=BLUE, fontweight='bold')

    # State after failure (warning)
    ax.plot(1.4, 1.1, '^', color=RED, markersize=15, zorder=5)
    ax.text(1.6, 1.3, 'After 2 gates fail\nmargin=0.12', fontsize=9, color=RED, fontweight='bold')

    # Shrunk reachable set after failure
    shrunk_x = 1.2 * np.cos(theta) + 0.05*np.sin(3*theta)
    shrunk_y = 1.0 * np.sin(theta) + 0.05*np.cos(3*theta)
    ax.plot(shrunk_x, shrunk_y, color=RED, linewidth=1.5, linestyle=':', label='Shrunk set (after failure)')

    ax.set_xlabel('Water level state h1 (m)', fontsize=10)
    ax.set_ylabel('Water level state h2 (m)', fontsize=10)
    ax.legend(fontsize=9, loc='lower left')
    ax.grid(True, alpha=0.3)
    ax.set_aspect('equal')
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-2.0, 2.0)

    save(fig, 'PF3-5_fig1.png')

def pf3_5_fig2():
    """Safety margin evolution"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle('PF3-5 Fig 2: Safety margin real-time evolution', fontsize=13, fontweight='bold')

    t = np.linspace(0, 24, 300)
    margin = 0.7 + 0.05*np.sin(0.5*t) + np.random.normal(0, 0.01, len(t))

    # Gate failure at t=8
    idx8 = np.argmin(np.abs(t-8))
    for i in range(idx8, len(t)):
        margin[i] -= 0.5 * (1 - np.exp(-0.3*(t[i]-8)))
    # Recovery at t=14
    idx14 = np.argmin(np.abs(t-14))
    for i in range(idx14, len(t)):
        margin[i] += 0.4 * (1 - np.exp(-0.2*(t[i]-14)))
    margin = np.maximum(margin, 0.05)

    ax1.plot(t, margin, color=BLUE, linewidth=1.5)
    ax1.axhline(y=0.5, color=YELLOW, linestyle='--', label='Yellow warning')
    ax1.axhline(y=0.2, color=ORANGE, linestyle='--', label='Red warning')
    ax1.axhline(y=0.05, color=RED, linestyle='--', label='Emergency')
    ax1.fill_between(t, 0, 0.05, alpha=0.1, color=RED)
    ax1.fill_between(t, 0.05, 0.2, alpha=0.1, color=ORANGE)
    ax1.fill_between(t, 0.2, 0.5, alpha=0.1, color=YELLOW)
    ax1.set_ylabel('Safety margin', fontsize=10)
    ax1.legend(fontsize=8, ncol=3)
    ax1.grid(True, alpha=0.3)

    # Events
    ax2.axvline(x=8, color=RED, linewidth=2, alpha=0.5, label='Gate failure')
    ax2.axvline(x=14, color=GREEN, linewidth=2, alpha=0.5, label='Repair complete')
    ax2.set_xlabel('Time (h)', fontsize=10)
    ax2.set_ylabel('Events', fontsize=10)
    ax2.legend(fontsize=9)
    ax2.set_yticks([])

    plt.tight_layout()
    save(fig, 'PF3-5_fig2.png')

def pf3_5_fig3():
    """Reachability computation flow"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF3-5 Fig 3: Reachability analysis computation pipeline', fontsize=13, fontweight='bold', pad=15)

    steps = [
        ('IDZ Model', 'Linear state-space\nfrom PF1-1', BLUE, 0.3),
        ('Zonotope\nApprox', 'Polyhedral\nset representation', GREEN, 2.5),
        ('Backward\nReach', 'T-step backward\nset computation', PURPLE, 4.7),
        ('Margin\nCalc', 'Distance to\nset boundary', ORANGE, 6.9),
    ]

    for title, desc, color, x in steps:
        rect = FancyBboxPatch((x, 2.0), 1.8, 2.5, boxstyle="round,pad=0.1",
                               facecolor=f'{color}22', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+0.9, 3.8, title, ha='center', fontsize=10, fontweight='bold', color=color)
        ax.text(x+0.9, 2.6, desc, ha='center', fontsize=8)

    for i in range(3):
        x1 = steps[i][3] + 1.8
        x2 = steps[i+1][3]
        ax.annotate('', xy=(x2, 3.25), xytext=(x1, 3.25), arrowprops=dict(arrowstyle='->', color=GRAY, lw=2))

    # Output
    rect = FancyBboxPatch((6.9, 0.3), 2.8, 1.2, boxstyle="round,pad=0.1",
                           facecolor='#FFCDD2', edgecolor=RED, linewidth=2)
    ax.add_patch(rect)
    ax.text(8.3, 0.9, 'Warning System\nmargin<0.5:Yellow | <0.2:Red | <0.05:Emergency', ha='center', fontsize=8, color=RED)
    ax.annotate('', xy=(8.3, 1.5), xytext=(8.3, 2.0), arrowprops=dict(arrowstyle='->', color=RED, lw=1.5))

    ax.text(5.0, 5.2, 'Update every 5 minutes | Uses IDZ model for speed (O(n^3) per step)',
            fontsize=9, ha='center', color=GRAY)

    save(fig, 'PF3-5_fig3.png')

if __name__ == '__main__':
    print("Generating PF3 series figures...")

    print("\nPF3-1: Dynamic safety boundaries")
    pf3_1_fig1()
    pf3_1_fig2()
    pf3_1_fig3()

    print("\nPF3-2: ODD formal definition")
    pf3_2_fig1()
    pf3_2_fig2()
    pf3_2_fig3()

    print("\nPF3-3: Multi-level interlocks")
    pf3_3_fig1()
    pf3_3_fig2()
    pf3_3_fig3()

    print("\nPF3-4: Scenario library diagnosis")
    pf3_4_fig1()
    pf3_4_fig2()
    pf3_4_fig3()

    print("\nPF3-5: Reachability analysis")
    pf3_5_fig1()
    pf3_5_fig2()
    pf3_5_fig3()

    print(f"\nDone! 15 figures generated for PF3 series.")
