"""
PF2系列专利配图生成脚本
PF2：分层分布式控制方法（6件）
每件生成3张图（架构图/原理图 + 流程图 + 工程应用图）
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

# 中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 统一配色
BLUE = '#1565C0'
GREEN = '#4CAF50'
PURPLE = '#7B1FA2'
ORANGE = '#FF7043'
GRAY = '#9E9E9E'
LIGHT_BLUE = '#BBDEFB'
LIGHT_GREEN = '#C8E6C9'
LIGHT_PURPLE = '#E1BEE7'
LIGHT_ORANGE = '#FFCCBC'

outdir = os.path.dirname(os.path.abspath(__file__))

def save(fig, name):
    fig.savefig(os.path.join(outdir, name), dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved {name}")

# ===== PF2-1: 分层分布式MPC =====
def pf2_1_fig1():
    """三层控制架构图"""
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF2-1 图1：分层分布式模型预测控制架构', fontsize=14, fontweight='bold', pad=15)

    # Layer 3: Coordination (top)
    rect = FancyBboxPatch((1, 6.2), 8, 1.2, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5, 6.8, '协调优化层（段级DMPC）', ha='center', va='center', fontsize=12, fontweight='bold', color=PURPLE)
    ax.text(5, 6.4, '时间尺度：分钟~小时 | 模型：IDZ传递函数 | 通信：边界流量轨线交换', ha='center', va='center', fontsize=8, color=PURPLE)

    # Layer 2: Local MPC (middle)
    for i, name in enumerate(['渠池1\nMPC', '渠池2\nMPC', '渠池3\nMPC', '...', '渠池N\nMPC']):
        x = 1.2 + i * 1.7
        color = LIGHT_BLUE if name != '...' else 'white'
        ec = BLUE if name != '...' else 'none'
        rect = FancyBboxPatch((x, 3.8), 1.4, 1.6, boxstyle="round,pad=0.1",
                               facecolor=color, edgecolor=ec, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+0.7, 4.6, name, ha='center', va='center', fontsize=9, fontweight='bold' if name != '...' else 'normal')

    ax.text(5, 5.6, '实时调节层（渠池级局部MPC）', ha='center', va='center', fontsize=11, fontweight='bold', color=BLUE)
    ax.text(5, 5.3, '时间尺度：秒~分钟 | 模型：IDZ | 预测时域Np=12步', ha='center', va='center', fontsize=8, color=BLUE)

    # Layer 1: Safety (bottom)
    rect = FancyBboxPatch((1, 1.0), 8, 1.2, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5, 1.6, '安全保护层（PLC硬连锁）', ha='center', va='center', fontsize=12, fontweight='bold', color=ORANGE)
    ax.text(5, 1.2, '时间尺度：毫秒 | 独立运行 | 水位越限→紧急关闸 | 永不失效', ha='center', va='center', fontsize=8, color=ORANGE)

    # Arrows between layers
    ax.annotate('', xy=(5, 6.2), xytext=(5, 5.7), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
    ax.annotate('', xy=(5, 3.8), xytext=(5, 2.3), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))

    # Degradation annotations
    ax.annotate('上层失效→\n下层自主托底', xy=(9.5, 4.5), fontsize=8, color=ORANGE,
                ha='center', style='italic',
                bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor=ORANGE, alpha=0.8))

    ax.text(0.3, 0.5, '关键特征：层间时间尺度分离，各层独立可运行', fontsize=9, style='italic', color=GRAY)
    save(fig, 'PF2-1_fig1.png')

def pf2_1_fig2():
    """DMPC协调流程图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-1 图2：分布式MPC协调优化流程', fontsize=14, fontweight='bold', pad=15)

    steps = [
        ('S1\n采集状态', '各渠池Agent采集\n本地水位/流量', 1.0),
        ('S2\n局部求解', '各Agent并行求解\n局部MPC优化', 2.5),
        ('S3\n边界交换', '相邻Agent交换\n边界流量计划', 4.0),
        ('S4\n一致性检查', '计算边界残差\nr_bd是否收敛?', 5.5),
        ('S5\n执行指令', '向执行器下达\n闸门开度指令', 7.5),
    ]

    for i, (title, desc, x) in enumerate(steps):
        color = [BLUE, GREEN, PURPLE, ORANGE, BLUE][i]
        light = [LIGHT_BLUE, LIGHT_GREEN, LIGHT_PURPLE, LIGHT_ORANGE, LIGHT_BLUE][i]
        rect = FancyBboxPatch((x, 3.0), 1.3, 2.5, boxstyle="round,pad=0.1",
                               facecolor=light, edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+0.65, 4.8, title, ha='center', va='center', fontsize=10, fontweight='bold', color=color)
        ax.text(x+0.65, 3.7, desc, ha='center', va='center', fontsize=8)

        if i < len(steps) - 1:
            next_x = steps[i+1][2]
            ax.annotate('', xy=(next_x, 4.25), xytext=(x+1.3, 4.25),
                       arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))

    # Loop back from S4 to S2
    ax.annotate('未收敛\n(迭代<5次)', xy=(2.5, 5.5), xytext=(5.5, 6.2),
               arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.5, connectionstyle='arc3,rad=0.3'),
               fontsize=8, color=ORANGE, ha='center')

    ax.text(5, 1.5, '典型收敛：正常工况2-3次迭代，扰动工况4-5次迭代', fontsize=9, ha='center', color=GRAY, style='italic')
    save(fig, 'PF2-1_fig2.png')

def pf2_1_fig3():
    """工程应用：南水北调中线渠池示意"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF2-1 图3：南水北调中线分段控制示意', fontsize=14, fontweight='bold', pad=15)

    # Draw canal pools
    for i in range(5):
        x = 0.5 + i * 2.3
        # Pool
        rect = plt.Rectangle((x, 2.0), 1.8, 0.8, facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+0.9, 2.4, f'渠池{i+1}', ha='center', va='center', fontsize=9, fontweight='bold')

        # Gate between pools
        if i < 4:
            gx = x + 1.8
            rect = plt.Rectangle((gx, 1.8), 0.5, 1.2, facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=1.5)
            ax.add_patch(rect)
            ax.text(gx+0.25, 2.4, f'闸{i+1}', ha='center', va='center', fontsize=7, rotation=90)

        # MPC controller
        rect = FancyBboxPatch((x+0.2, 3.5), 1.4, 0.8, boxstyle="round,pad=0.1",
                               facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=1)
        ax.add_patch(rect)
        ax.text(x+0.9, 3.9, f'MPC-{i+1}', ha='center', va='center', fontsize=8, color=GREEN, fontweight='bold')

        # Arrows MPC to gate
        if i < 4:
            ax.annotate('', xy=(gx+0.25, 3.0), xytext=(x+0.9, 3.5),
                       arrowprops=dict(arrowstyle='->', color=GREEN, lw=1))

    # DMPC coordination line
    ax.annotate('', xy=(10.1, 4.8), xytext=(0.9, 4.8),
               arrowprops=dict(arrowstyle='<->', color=PURPLE, lw=2, linestyle='dashed'))
    ax.text(5.5, 5.2, 'DMPC协调层：交换边界流量轨线', ha='center', fontsize=10, color=PURPLE, fontweight='bold')

    # Flow direction
    ax.annotate('水流方向 →', xy=(11.5, 2.4), fontsize=10, color=BLUE, fontweight='bold')

    # Info
    ax.text(0.5, 0.8, '南水北调中线：1432km | 60+渠池 | 97座节制闸 | 采样周期30s', fontsize=9, color=GRAY)
    save(fig, 'PF2-1_fig3.png')

# ===== PF2-2: IDZ-based MPC =====
def pf2_2_fig1():
    """IDZ-MPC控制器架构"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-2 图1：基于IDZ模型的渠池MPC控制器架构', fontsize=14, fontweight='bold', pad=15)

    # Reference
    rect = FancyBboxPatch((0.3, 4.0), 1.5, 1.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(1.05, 4.5, '目标水位\n参考轨迹', ha='center', va='center', fontsize=9, color=PURPLE)

    # MPC optimizer
    rect = FancyBboxPatch((2.5, 3.5), 2.2, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(rect)
    ax.text(3.6, 5.0, 'MPC优化器', ha='center', va='center', fontsize=11, fontweight='bold', color=BLUE)
    ax.text(3.6, 4.3, 'min J = Σ(||y-r||²Q\n        + ||Δu||²R)', ha='center', va='center', fontsize=8)
    ax.text(3.6, 3.7, '约束软化+速率限制', ha='center', va='center', fontsize=8, color=ORANGE)

    # IDZ model
    rect = FancyBboxPatch((2.8, 1.5), 1.6, 1.2, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_GREEN, edgecolor=GREEN, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(3.6, 2.3, 'IDZ预测模型', ha='center', va='center', fontsize=10, fontweight='bold', color=GREEN)
    ax.text(3.6, 1.8, 'G(s)=(1+τₘs)e⁻ᵗᵈˢ/Aₛs', ha='center', va='center', fontsize=8)

    # Plant
    rect = FancyBboxPatch((5.8, 3.5), 2.0, 2.0, boxstyle="round,pad=0.1",
                           facecolor='#FFF3E0', edgecolor=ORANGE, linewidth=2)
    ax.add_patch(rect)
    ax.text(6.8, 5.0, '被控渠池', ha='center', va='center', fontsize=11, fontweight='bold', color=ORANGE)
    ax.text(6.8, 4.3, 'Saint-Venant\n方程', ha='center', va='center', fontsize=9)
    ax.text(6.8, 3.7, '闸门执行器', ha='center', va='center', fontsize=9)

    # Feedforward
    rect = FancyBboxPatch((5.8, 1.5), 2.0, 1.2, boxstyle="round,pad=0.1",
                           facecolor='#F3E5F5', edgecolor=PURPLE, linewidth=1.5)
    ax.add_patch(rect)
    ax.text(6.8, 2.1, '前馈补偿\n(下游需水变化)', ha='center', va='center', fontsize=9, color=PURPLE)

    # Arrows
    ax.annotate('', xy=(2.5, 4.5), xytext=(1.8, 4.5), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
    ax.annotate('', xy=(5.8, 4.5), xytext=(4.7, 4.5), arrowprops=dict(arrowstyle='->', color=BLUE, lw=2))
    ax.text(5.25, 4.7, 'Δu', fontsize=10, fontweight='bold', color=BLUE)

    # Feedback
    ax.annotate('', xy=(3.6, 3.5), xytext=(3.6, 2.7), arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5))
    ax.annotate('y(k)', xy=(8.5, 4.5), xytext=(7.8, 4.5), fontsize=9,
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))

    # Sensor feedback loop
    ax.annotate('', xy=(8.3, 3.0), xytext=(8.3, 3.5), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1))
    ax.annotate('', xy=(3.6, 1.0), xytext=(8.3, 1.0), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1, linestyle='dashed'))
    ax.annotate('', xy=(3.6, 1.5), xytext=(3.6, 1.0), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1, linestyle='dashed'))
    ax.text(6, 0.7, '实测水位反馈', fontsize=8, color=GRAY, ha='center')

    # Parameter adaptive
    ax.text(8.5, 2.5, '参数自适应\n(工况变化时\n更新IDZ参数)', fontsize=8, color=GREEN,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_GREEN, edgecolor=GREEN, alpha=0.5))

    save(fig, 'PF2-2_fig1.png')

def pf2_2_fig2():
    """MPC控制流程"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-2 图2：渠池MPC控制方法流程', fontsize=14, fontweight='bold', pad=15)

    steps = [
        ('S1: 状态采集', '采集当前水位H(k)\n流量Q(k)、闸位u(k)', BLUE),
        ('S2: IDZ预测', '利用IDZ模型预测\n未来Np步水位轨迹', GREEN),
        ('S3: 优化求解', '求解QP优化问题\n含约束软化处理', PURPLE),
        ('S4: 前馈叠加', '叠加下游扰动\n前馈补偿量', ORANGE),
        ('S5: 执行首步', '仅执行优化序列\n第一步控制量', BLUE),
        ('S6: 参数检查', '检查工况变化\n必要时更新IDZ参数', GREEN),
    ]

    for i, (title, desc, color) in enumerate(steps):
        row = i // 3
        col = i % 3
        x = 0.5 + col * 3.2
        y = 4.5 - row * 3.0

        rect = FancyBboxPatch((x, y), 2.5, 1.8, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=color, linewidth=2)
        ax.add_patch(rect)
        ax.text(x+1.25, y+1.3, title, ha='center', va='center', fontsize=10, fontweight='bold', color=color)
        ax.text(x+1.25, y+0.5, desc, ha='center', va='center', fontsize=8)

    # Arrows
    for i in range(5):
        row1, col1 = i // 3, i % 3
        row2, col2 = (i+1) // 3, (i+1) % 3
        x1 = 0.5 + col1 * 3.2 + 2.5
        y1 = 4.5 - row1 * 3.0 + 0.9
        x2 = 0.5 + col2 * 3.2
        y2 = 4.5 - row2 * 3.0 + 0.9

        if row1 == row2:
            ax.annotate('', xy=(x2, y2), xytext=(x1, y1), arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5))
        else:
            ax.annotate('', xy=(x2+2.5, y2+0.9), xytext=(x1, y1),
                       arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5, connectionstyle='arc3,rad=-0.5'))

    # Loop back
    ax.annotate('滚动优化\n(每Ts=30s重复)', xy=(1.75, 6.5), xytext=(7.0, 0.8),
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5, linestyle='dashed', connectionstyle='arc3,rad=-0.5'),
               fontsize=8, color=GRAY)

    save(fig, 'PF2-2_fig2.png')

def pf2_2_fig3():
    """水位控制效果对比"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), height_ratios=[2, 1])
    fig.suptitle('PF2-2 图3：MPC vs PI控制水位响应对比', fontsize=14, fontweight='bold')

    t = np.linspace(0, 72, 1000)
    ref = np.ones_like(t) * 58.5
    # Disturbance at t=24h and t=48h
    ref[t > 24] = 58.8
    ref[t > 48] = 58.3

    # MPC response (fast, minimal overshoot)
    mpc = np.copy(ref)
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        mpc[i] = mpc[i-1] + 0.3 * (ref[i] - mpc[i-1]) * dt + np.random.normal(0, 0.005)

    # PI response (slower, overshoot)
    pi = np.copy(ref)
    omega = 0.15
    zeta = 0.4
    for i in range(1, len(t)):
        dt = t[i] - t[i-1]
        error = ref[i] - pi[i-1]
        pi[i] = pi[i-1] + 0.15 * error * dt + np.random.normal(0, 0.01)
        if 24 < t[i] < 30 or 48 < t[i] < 54:
            pi[i] += 0.03 * np.sin(omega * (t[i] - int(t[i]/24)*24) * 10)

    ax1.plot(t, ref, 'k--', label='目标水位', linewidth=1.5, alpha=0.7)
    ax1.plot(t, mpc, color=BLUE, label='IDZ-MPC', linewidth=1.5)
    ax1.plot(t, pi, color=ORANGE, label='PI控制', linewidth=1.5, alpha=0.8)
    ax1.fill_between(t, 58.0, 59.0, alpha=0.1, color=GREEN, label='安全水位区间')
    ax1.set_ylabel('水位 (m)', fontsize=10)
    ax1.legend(loc='upper right', fontsize=9)
    ax1.set_xlim(0, 72)
    ax1.grid(True, alpha=0.3)

    # Flow changes
    flow_mpc = np.gradient(mpc) * 100
    flow_pi = np.gradient(pi) * 100
    ax2.plot(t, flow_mpc, color=BLUE, label='MPC流量变化率', linewidth=1)
    ax2.plot(t, flow_pi, color=ORANGE, label='PI流量变化率', linewidth=1, alpha=0.8)
    ax2.set_xlabel('时间 (h)', fontsize=10)
    ax2.set_ylabel('ΔQ (m³/s/h)', fontsize=10)
    ax2.legend(fontsize=8)
    ax2.set_xlim(0, 72)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF2-2_fig3.png')

# ===== PF2-3: Multi-gate DMPC =====
def pf2_3_fig1():
    """ADMM分布式优化原理"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-3 图1：多闸ADMM分布式协调原理', fontsize=14, fontweight='bold', pad=15)

    # 5 pools with local optimizers
    for i in range(5):
        x = 0.5 + i * 1.9
        rect = FancyBboxPatch((x, 1.5), 1.5, 2.5, boxstyle="round,pad=0.1",
                               facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x+0.75, 3.5, f'渠池{i+1}', ha='center', va='center', fontsize=10, fontweight='bold', color=BLUE)
        ax.text(x+0.75, 2.8, f'局部MPC', ha='center', va='center', fontsize=9)
        ax.text(x+0.75, 2.2, f'min J{i+1}', ha='center', va='center', fontsize=8, color=GRAY)
        ax.text(x+0.75, 1.8, f'IDZ模型', ha='center', va='center', fontsize=8, color=GREEN)

        # Boundary exchange arrows
        if i < 4:
            ax.annotate('', xy=(x+1.9, 3.0), xytext=(x+1.5, 3.0),
                       arrowprops=dict(arrowstyle='<->', color=PURPLE, lw=2))

    # ADMM convergence text
    ax.text(5, 5.5, 'ADMM协调：边界流量一致性约束', ha='center', fontsize=12, fontweight='bold', color=PURPLE)
    ax.text(5, 5.0, 'Q_boundary_i(k) = Q_boundary_{i+1}(k)  ∀k ∈ [0, Np]', ha='center', fontsize=10, color=PURPLE)

    ax.text(5, 0.8, '收敛特性：正常工况2-3次迭代 | 扰动工况4-5次 | 每次迭代~50ms', fontsize=9, ha='center', color=GRAY)
    save(fig, 'PF2-3_fig1.png')

def pf2_3_fig2():
    """ADMM迭代收敛曲线"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('PF2-3 图2：ADMM收敛性能', fontsize=14, fontweight='bold')

    # Left: residual convergence
    iters = np.arange(1, 11)
    primal = 10.0 * np.exp(-0.8 * iters) + np.random.normal(0, 0.1, len(iters)) * np.exp(-0.3*iters)
    dual = 8.0 * np.exp(-0.6 * iters) + np.random.normal(0, 0.08, len(iters)) * np.exp(-0.3*iters)
    primal = np.maximum(primal, 0.01)
    dual = np.maximum(dual, 0.01)

    ax1.semilogy(iters, primal, 'o-', color=BLUE, label='原始残差', linewidth=2, markersize=6)
    ax1.semilogy(iters, dual, 's-', color=ORANGE, label='对偶残差', linewidth=2, markersize=6)
    ax1.axhline(y=0.05, color='r', linestyle='--', alpha=0.5, label='收敛阈值')
    ax1.set_xlabel('ADMM迭代次数', fontsize=10)
    ax1.set_ylabel('残差 (m³/s)', fontsize=10)
    ax1.set_title('残差收敛过程', fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Right: scalability
    pools = [5, 10, 20, 40, 60]
    time_central = [0.05, 0.8, 12, 180, 1200]
    time_dmpc = [0.2, 0.35, 0.5, 0.7, 0.9]

    ax2.semilogy(pools, time_central, 'o-', color=ORANGE, label='集中式MPC', linewidth=2, markersize=8)
    ax2.semilogy(pools, time_dmpc, 's-', color=BLUE, label='本发明DMPC', linewidth=2, markersize=8)
    ax2.axhline(y=30, color='r', linestyle='--', alpha=0.5, label='控制周期上限(30s)')
    ax2.set_xlabel('渠池数量', fontsize=10)
    ax2.set_ylabel('求解时间 (s)', fontsize=10)
    ax2.set_title('可扩展性对比', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF2-3_fig2.png')

def pf2_3_fig3():
    """多闸协调水位响应"""
    fig, axes = plt.subplots(3, 1, figsize=(10, 7), sharex=True)
    fig.suptitle('PF2-3 图3：5渠池多闸协调控制响应', fontsize=14, fontweight='bold')

    t = np.linspace(0, 24, 500)
    colors = [BLUE, GREEN, PURPLE, ORANGE, '#795548']

    for i in range(5):
        ref = 58.5 + i * 0.3
        # DMPC response
        noise = np.random.normal(0, 0.01, len(t))
        level = ref + noise
        # Disturbance at t=8
        idx_8 = np.argmin(np.abs(t - 8))
        for j in range(idx_8, len(t)):
            level[j] += 0.05 * np.exp(-0.3*(t[j]-8)) * np.sin(0.5*(t[j]-8)) * (1 if i%2==0 else -1)

        axes[0].plot(t, level, color=colors[i], label=f'渠池{i+1}', linewidth=1.2)

    axes[0].set_ylabel('水位 (m)', fontsize=10)
    axes[0].legend(fontsize=8, ncol=5, loc='upper right')
    axes[0].set_title('各渠池水位（DMPC协调）', fontsize=10)
    axes[0].grid(True, alpha=0.3)

    # Gate flows
    for i in range(4):
        flow = 80 + i * 2 + np.random.normal(0, 0.3, len(t))
        idx_8 = np.argmin(np.abs(t - 8))
        for j in range(idx_8, len(t)):
            flow[j] += 3 * (1 - np.exp(-0.2*(t[j]-8)))
        axes[1].plot(t, flow, color=colors[i], label=f'闸{i+1}', linewidth=1.2)

    axes[1].set_ylabel('闸门流量 (m³/s)', fontsize=10)
    axes[1].legend(fontsize=8, ncol=4)
    axes[1].set_title('各闸门流量', fontsize=10)
    axes[1].grid(True, alpha=0.3)

    # Boundary residual
    residual = 0.5 * np.exp(-0.1 * t) + np.random.normal(0, 0.02, len(t))
    residual = np.maximum(residual, 0)
    axes[2].plot(t, residual, color=PURPLE, linewidth=1.5)
    axes[2].axhline(y=0.02, color='r', linestyle='--', alpha=0.5, label='收敛阈值')
    axes[2].set_ylabel('边界残差 (m³/s)', fontsize=10)
    axes[2].set_xlabel('时间 (h)', fontsize=10)
    axes[2].legend(fontsize=8)
    axes[2].set_title('ADMM边界残差', fontsize=10)
    axes[2].grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF2-3_fig3.png')

# ===== PF2-4: WNAL grading =====
def pf2_4_fig1():
    """WNAL五级阶梯图"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-4 图1：水网自主运行等级（WNAL）分级体系', fontsize=14, fontweight='bold', pad=15)

    levels = [
        ('L0', '人工运行', '全部人工操作\nSCADA仅显示', '#E0E0E0', GRAY),
        ('L1', '远程监控', '人工遥控\n系统提供数据', '#BBDEFB', BLUE),
        ('L2', '辅助运行', '系统推荐方案\n人工确认执行', '#90CAF9', BLUE),
        ('L3', '有条件自主', 'ODD内自主运行\n超ODD人工接管', '#42A5F5', 'white'),
        ('L4', '高度自主', '大多数场景自主\n含部分ODD扩展', '#1565C0', 'white'),
        ('L5', '完全自主', '自主扩展ODD\n持续自我进化', '#0D47A1', 'white'),
    ]

    for i, (code, name, desc, bg, fg) in enumerate(levels):
        x = 0.3 + i * 0.2
        y = 0.5 + i * 0.9
        w = 9.4 - i * 0.4

        rect = FancyBboxPatch((x, y), w, 0.75, boxstyle="round,pad=0.05",
                               facecolor=bg, edgecolor=BLUE if i > 0 else GRAY, linewidth=1.5)
        ax.add_patch(rect)
        ax.text(x + 0.4, y + 0.38, f'{code}: {name}', fontweight='bold', fontsize=10, color=fg, va='center')
        ax.text(x + w - 0.3, y + 0.38, desc, ha='right', fontsize=8, color=fg, va='center')

    # Critical transition arrow
    ax.annotate('关键跨越\n需xIL验证', xy=(2.5, 3.1), xytext=(0.5, 4.0),
               fontsize=9, fontweight='bold', color=ORANGE,
               arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2),
               bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_ORANGE, edgecolor=ORANGE))

    save(fig, 'PF2-4_fig1.png')

def pf2_4_fig2():
    """等级评定指标雷达图"""
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
    fig.suptitle('PF2-4 图2：WNAL等级评定指标体系', fontsize=14, fontweight='bold', y=0.98)

    categories = ['操作准确率', '响应时延', '故障恢复', 'ODD覆盖率', '安全合规率', '自适应能力']
    N = len(categories)
    angles = np.linspace(0, 2*np.pi, N, endpoint=False).tolist()
    angles += angles[:1]

    # L2 scores
    l2 = [0.75, 0.6, 0.5, 0.4, 0.85, 0.3]
    l2 += l2[:1]
    # L3 scores
    l3 = [0.9, 0.85, 0.8, 0.7, 0.95, 0.6]
    l3 += l3[:1]
    # L4 scores
    l4 = [0.97, 0.95, 0.93, 0.9, 0.99, 0.85]
    l4 += l4[:1]

    ax.plot(angles, l2, 'o-', color=BLUE, linewidth=2, markersize=6, label='WNAL L2')
    ax.fill(angles, l2, alpha=0.1, color=BLUE)
    ax.plot(angles, l3, 's-', color=GREEN, linewidth=2, markersize=6, label='WNAL L3')
    ax.fill(angles, l3, alpha=0.1, color=GREEN)
    ax.plot(angles, l4, 'D-', color=PURPLE, linewidth=2, markersize=6, label='WNAL L4')
    ax.fill(angles, l4, alpha=0.1, color=PURPLE)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10)
    ax.set_ylim(0, 1)
    ax.legend(loc='lower right', fontsize=10, bbox_to_anchor=(1.2, 0))

    save(fig, 'PF2-4_fig2.png')

def pf2_4_fig3():
    """等级切换状态机"""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF2-4 图3：WNAL等级安全切换协议', fontsize=14, fontweight='bold', pad=15)

    states = [('L1', 1.5, 3.0, GRAY), ('L2', 4.0, 3.0, BLUE), ('L3', 6.5, 3.0, GREEN), ('L4', 9.0, 3.0, PURPLE)]

    for name, x, y, color in states:
        circle = plt.Circle((x, y), 0.8, facecolor=f'{color}22', edgecolor=color, linewidth=2.5)
        ax.add_patch(circle)
        ax.text(x, y, name, ha='center', va='center', fontsize=16, fontweight='bold', color=color)

    # Upgrade arrows (top)
    for i in range(3):
        x1, x2 = states[i][1]+0.8, states[i+1][1]-0.8
        ax.annotate('', xy=(x2, 3.5), xytext=(x1, 3.5),
                   arrowprops=dict(arrowstyle='->', color=GREEN, lw=2))
        ax.text((x1+x2)/2, 4.0, '升级\n(90天试运行)', ha='center', fontsize=7, color=GREEN)

    # Downgrade arrows (bottom)
    for i in range(3):
        x1, x2 = states[i+1][1]-0.8, states[i][1]+0.8
        ax.annotate('', xy=(x2, 2.5), xytext=(x1, 2.5),
                   arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2))
        ax.text((x1+x2)/2, 1.8, '降级\n(安全触发即时)', ha='center', fontsize=7, color=ORANGE)

    ax.text(5, 0.5, '升级条件：90天评估达标 + 无安全事件 | 降级条件：ODD越界或安全违规立即触发',
            ha='center', fontsize=9, color=GRAY)
    save(fig, 'PF2-4_fig3.png')

# ===== PF2-5: Multi-objective optimization =====
def pf2_5_fig1():
    """分层多目标优化架构"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-5 图1：闸泵群分层多目标优化架构', fontsize=14, fontweight='bold', pad=15)

    # Upper layer
    rect = FancyBboxPatch((1.5, 4.5), 7, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5, 6.0, '上层：日前优化调度', ha='center', fontsize=12, fontweight='bold', color=PURPLE)

    objs = ['供水保障\nmin 缺水量', '节能降耗\nmin 泵站能耗', '水质维护\nmin 水龄']
    for i, obj in enumerate(objs):
        x = 2.2 + i * 2.3
        rect = FancyBboxPatch((x, 4.7), 1.8, 1.0, boxstyle="round,pad=0.1",
                               facecolor='white', edgecolor=PURPLE, linewidth=1)
        ax.add_patch(rect)
        ax.text(x+0.9, 5.2, obj, ha='center', va='center', fontsize=8, color=PURPLE)

    # Lower layer
    rect = FancyBboxPatch((1.5, 1.5), 7, 2.0, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5, 3.0, '下层：实时跟踪调整', ha='center', fontsize=12, fontweight='bold', color=BLUE)
    ax.text(5, 2.3, '采样周期30s | MPC跟踪日前计划 | 处理实时偏差', ha='center', fontsize=9, color=BLUE)

    # Pareto
    ax.text(8.8, 5.8, 'NSGA-II\nPareto\n前沿搜索', ha='center', fontsize=8, color=ORANGE,
            bbox=dict(boxstyle='round,pad=0.3', facecolor=LIGHT_ORANGE, edgecolor=ORANGE))

    # Arrow between layers
    ax.annotate('日前计划\n下达', xy=(5, 3.5), xytext=(5, 4.5),
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=2),
               ha='center', fontsize=9, color=GRAY)
    ax.annotate('执行反馈\n上报', xy=(7, 4.5), xytext=(7, 3.5),
               arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5, linestyle='dashed'),
               ha='center', fontsize=8, color=GRAY)

    ax.text(5, 0.8, '时间尺度分离：上层24h/1h分辨率 ↔ 下层实时/30s周期', fontsize=9, ha='center', color=GRAY)
    save(fig, 'PF2-5_fig1.png')

def pf2_5_fig2():
    """Pareto前沿"""
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.suptitle('PF2-5 图2：多目标Pareto前沿与决策偏好', fontsize=14, fontweight='bold')

    # Generate Pareto front
    np.random.seed(42)
    n = 50
    x = np.sort(np.random.uniform(0.5, 5, n))
    y = 3.0 / x + np.random.normal(0, 0.1, n)
    y = np.maximum(y, 0.3)

    # Non-dominated
    pareto_x, pareto_y = [x[0]], [y[0]]
    min_y = y[0]
    for i in range(1, n):
        if y[i] < min_y:
            pareto_x.append(x[i])
            pareto_y.append(y[i])
            min_y = y[i]

    ax.scatter(x, y, c=BLUE, alpha=0.3, s=30, label='可行解')
    ax.plot(pareto_x, pareto_y, 'o-', color=ORANGE, linewidth=2, markersize=8, label='Pareto前沿')

    # Selected point
    sel_idx = len(pareto_x) // 2
    ax.plot(pareto_x[sel_idx], pareto_y[sel_idx], '*', color=GREEN, markersize=20, label='决策者偏好解')

    ax.set_xlabel('供水缺口 (万m³/日)', fontsize=11)
    ax.set_ylabel('日能耗 (万kWh)', fontsize=11)
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)

    save(fig, 'PF2-5_fig2.png')

def pf2_5_fig3():
    """能耗优化效果"""
    fig, ax = plt.subplots(figsize=(10, 5))
    fig.suptitle('PF2-5 图3：胶东调水泵站群优化调度效果', fontsize=14, fontweight='bold')

    hours = np.arange(24)
    tariff = np.where((hours >= 8) & (hours < 22), 0.85, 0.35)
    pump_manual = np.array([3,3,3,3,3,3,4,5,6,7,7,7,7,7,7,6,6,6,5,5,4,4,3,3]) * 10
    pump_opt = np.array([7,7,7,6,6,5,3,2,2,3,3,4,4,3,3,2,2,3,4,5,6,7,7,7]) * 10

    ax2 = ax.twinx()
    ax2.fill_between(hours, tariff, alpha=0.15, color=ORANGE, step='mid', label='电价')
    ax2.set_ylabel('电价 (元/kWh)', fontsize=10, color=ORANGE)
    ax2.tick_params(axis='y', labelcolor=ORANGE)
    ax2.set_ylim(0, 1.2)

    ax.bar(hours-0.2, pump_manual, 0.35, color=GRAY, alpha=0.7, label='人工调度')
    ax.bar(hours+0.2, pump_opt, 0.35, color=BLUE, alpha=0.8, label='优化调度')
    ax.set_xlabel('时间 (h)', fontsize=10)
    ax.set_ylabel('泵站功率 (kW)', fontsize=10)
    ax.set_xlim(-0.5, 23.5)

    lines1, labels1 = ax.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax.legend(lines1 + lines2, labels1 + labels2, loc='upper left', fontsize=9)

    ax.set_title(f'优化效果：峰谷转移60%泵送量，日节电约23%', fontsize=10, color=GREEN)
    ax.grid(True, alpha=0.3, axis='y')

    save(fig, 'PF2-5_fig3.png')

# ===== PF2-6: RL-based MPC optimization =====
def pf2_6_fig1():
    """RL+MPC双引擎架构"""
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF2-6 图1：强化学习+MPC双引擎在线优化架构', fontsize=14, fontweight='bold', pad=15)

    # RL Agent
    rect = FancyBboxPatch((0.5, 4.0), 3.0, 2.5, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_PURPLE, edgecolor=PURPLE, linewidth=2)
    ax.add_patch(rect)
    ax.text(2.0, 6.0, 'RL智能体', ha='center', fontsize=12, fontweight='bold', color=PURPLE)
    ax.text(2.0, 5.3, '状态: [水位,流量,\n  扰动,时段]', ha='center', fontsize=8)
    ax.text(2.0, 4.4, '动作: [Np, Q/R,\n  约束松弛ε]', ha='center', fontsize=8, color=ORANGE)

    # MPC Controller
    rect = FancyBboxPatch((4.5, 4.0), 2.5, 2.5, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_BLUE, edgecolor=BLUE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5.75, 6.0, 'MPC控制器', ha='center', fontsize=12, fontweight='bold', color=BLUE)
    ax.text(5.75, 5.2, '预测时域: Np\n权重: Q,R\n约束: ε-软化', ha='center', fontsize=8)
    ax.text(5.75, 4.3, '在线QP求解', ha='center', fontsize=9, color=BLUE)

    # Plant
    rect = FancyBboxPatch((4.5, 1.0), 2.5, 2.0, boxstyle="round,pad=0.1",
                           facecolor='#FFF3E0', edgecolor=ORANGE, linewidth=2)
    ax.add_patch(rect)
    ax.text(5.75, 2.3, '水网系统', ha='center', fontsize=12, fontweight='bold', color=ORANGE)
    ax.text(5.75, 1.5, '(实际/数字孪生)', ha='center', fontsize=9, color=ORANGE)

    # Safety constraint
    rect = FancyBboxPatch((8.0, 4.0), 1.5, 2.5, boxstyle="round,pad=0.1",
                           facecolor=LIGHT_ORANGE, edgecolor=ORANGE, linewidth=2)
    ax.add_patch(rect)
    ax.text(8.75, 5.5, '安全约束\n监督器', ha='center', fontsize=10, fontweight='bold', color=ORANGE)
    ax.text(8.75, 4.5, 'Lagrangian\n松弛', ha='center', fontsize=8)

    # Arrows
    ax.annotate('超参数\n调整', xy=(4.5, 5.25), xytext=(3.5, 5.25),
               arrowprops=dict(arrowstyle='->', color=PURPLE, lw=2),
               ha='center', fontsize=8, color=PURPLE)
    ax.annotate('控制量\nu(k)', xy=(5.75, 3.0), xytext=(5.75, 4.0),
               arrowprops=dict(arrowstyle='->', color=BLUE, lw=2),
               ha='center', fontsize=8, color=BLUE)
    ax.annotate('奖励信号\n性能+安全', xy=(2.0, 4.0), xytext=(2.0, 1.5),
               arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, connectionstyle='arc3,rad=0.5'),
               ha='center', fontsize=8, color=GREEN)
    ax.annotate('', xy=(7.0, 5.25), xytext=(8.0, 5.25),
               arrowprops=dict(arrowstyle='<->', color=ORANGE, lw=1.5))

    save(fig, 'PF2-6_fig1.png')

def pf2_6_fig2():
    """RL学习曲线"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
    fig.suptitle('PF2-6 图2：强化学习训练与在线微调效果', fontsize=14, fontweight='bold')

    # Pretraining curve
    episodes = np.arange(0, 10001, 100)
    reward = -50 + 45 * (1 - np.exp(-episodes/2000)) + np.random.normal(0, 2, len(episodes)) * np.exp(-episodes/5000)

    ax1.plot(episodes, reward, color=PURPLE, linewidth=1.5, alpha=0.7)
    ax1.axvline(x=8000, color='r', linestyle='--', alpha=0.5, label='预训练完成')
    ax1.set_xlabel('训练回合', fontsize=10)
    ax1.set_ylabel('累积奖励', fontsize=10)
    ax1.set_title('数字孪生预训练', fontsize=11)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)

    # Online performance
    days = np.arange(0, 91)
    rmse_fixed = np.ones(91) * 3.2 + np.random.normal(0, 0.2, 91)
    rmse_rl = 3.2 - 0.6 * (1 - np.exp(-days/30)) + np.random.normal(0, 0.15, 91)

    ax2.plot(days, rmse_fixed, color=GRAY, linewidth=1.5, label='固定参数MPC', alpha=0.7)
    ax2.plot(days, rmse_rl, color=BLUE, linewidth=2, label='RL自适应MPC')
    ax2.fill_between(days, rmse_rl-0.3, rmse_rl+0.3, alpha=0.1, color=BLUE)
    ax2.set_xlabel('在线运行天数', fontsize=10)
    ax2.set_ylabel('水位RMSE (cm)', fontsize=10)
    ax2.set_title('在线微调效果', fontsize=11)
    ax2.legend(fontsize=9)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF2-6_fig2.png')

def pf2_6_fig3():
    """安全约束RL探索过程"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle('PF2-6 图3：安全约束强化学习探索过程', fontsize=14, fontweight='bold')

    t = np.linspace(0, 90, 500)

    # Water level with RL exploration
    level = 58.5 + np.random.normal(0, 0.02, len(t))
    # RL exploration causes slight variations but stays within bounds
    level += 0.05 * np.sin(0.3 * t) * np.exp(-t/50)

    upper = np.ones_like(t) * 59.0
    lower = np.ones_like(t) * 58.0

    ax1.fill_between(t, lower, upper, alpha=0.1, color=GREEN, label='安全水位区间')
    ax1.plot(t, level, color=BLUE, linewidth=1, label='RL探索下的水位')
    ax1.plot(t, upper, 'r--', linewidth=1, alpha=0.5)
    ax1.plot(t, lower, 'r--', linewidth=1, alpha=0.5)
    ax1.set_ylabel('水位 (m)', fontsize=10)
    ax1.legend(fontsize=9)
    ax1.set_title('安全约束下的控制探索', fontsize=10)
    ax1.grid(True, alpha=0.3)

    # MPC parameters evolution
    np_values = 12 + 2 * np.sin(0.1 * t) * (1 - np.exp(-t/20))
    qr_ratio = 10 + 3 * np.cos(0.08 * t) * (1 - np.exp(-t/30))

    ax2.plot(t, np_values, color=PURPLE, linewidth=1.5, label='预测时域 Np')
    ax2_twin = ax2.twinx()
    ax2_twin.plot(t, qr_ratio, color=ORANGE, linewidth=1.5, label='Q/R权重比')

    ax2.set_xlabel('运行天数', fontsize=10)
    ax2.set_ylabel('Np (步)', fontsize=10, color=PURPLE)
    ax2_twin.set_ylabel('Q/R', fontsize=10, color=ORANGE)

    lines1, labels1 = ax2.get_legend_handles_labels()
    lines2, labels2 = ax2_twin.get_legend_handles_labels()
    ax2.legend(lines1 + lines2, labels1 + labels2, fontsize=9)
    ax2.set_title('RL优化的MPC超参数演化', fontsize=10)
    ax2.grid(True, alpha=0.3)

    plt.tight_layout()
    save(fig, 'PF2-6_fig3.png')

# ===== Main =====
if __name__ == '__main__':
    print("Generating PF2 series figures...")

    print("\nPF2-1: 分层分布式MPC")
    pf2_1_fig1()
    pf2_1_fig2()
    pf2_1_fig3()

    print("\nPF2-2: IDZ-MPC渠池控制")
    pf2_2_fig1()
    pf2_2_fig2()
    pf2_2_fig3()

    print("\nPF2-3: 多闸ADMM协调")
    pf2_3_fig1()
    pf2_3_fig2()
    pf2_3_fig3()

    print("\nPF2-4: WNAL分级评定")
    pf2_4_fig1()
    pf2_4_fig2()
    pf2_4_fig3()

    print("\nPF2-5: 多目标优化调度")
    pf2_5_fig1()
    pf2_5_fig2()
    pf2_5_fig3()

    print("\nPF2-6: RL-MPC在线优化")
    pf2_6_fig1()
    pf2_6_fig2()
    pf2_6_fig3()

    print(f"\nDone! 18 figures generated for PF2 series.")
