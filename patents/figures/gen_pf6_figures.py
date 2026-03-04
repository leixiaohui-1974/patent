"""
PF6系列专利图片生成脚本
在环测试与验证方法（5件×4图=20张）
统一配色：BLUE=#1565C0, GREEN=#4CAF50, PURPLE=#7B1FA2, ORANGE=#FF7043
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
import os

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
WHITE = '#FFFFFF'
DARK = '#212121'

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False

output_dir = os.path.dirname(os.path.abspath(__file__))

def save_fig(fig, name):
    path = os.path.join(output_dir, name)
    fig.savefig(path, dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  [OK] {name}")

def draw_box(ax, x, y, w, h, text, color, fontsize=9, textcolor='white'):
    box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                         facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(box)
    ax.text(x+w/2, y+h/2, text, ha='center', va='center',
            fontsize=fontsize, color=textcolor, fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color=GRAY):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.5))

# ===================== PF6-1 MIL测试平台 =====================

def pf6_1_fig1():
    """MIL平台总体架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-1 图1: MIL平台总体架构图', fontsize=14, fontweight='bold', pad=15)

    # 四大模块
    draw_box(ax, 0.5, 4, 3, 2, '被测控制器 C\n(MPC/DMPC)', BLUE, 11)
    draw_box(ax, 4.5, 4, 3, 2, '水动力仿真器 P\n(Saint-Venant)', GREEN, 11)
    draw_box(ax, 8.5, 4, 3, 2, '指标评估 E\n(六维评价)', PURPLE, 11)
    draw_box(ax, 4.5, 0.5, 3, 2, '场景管理 S\n(故障注入)', ORANGE, 11)

    # 闭环箭头
    draw_arrow(ax, 3.5, 5, 4.5, 5, BLUE)
    ax.text(4, 5.3, 'u_k', fontsize=9, color=BLUE, ha='center')
    draw_arrow(ax, 7.5, 5, 8.5, 5, GREEN)
    ax.text(8, 5.3, 'x_k', fontsize=9, color=GREEN, ha='center')
    draw_arrow(ax, 6, 4, 6, 2.5, ORANGE)
    ax.text(6.3, 3.2, 'd_k', fontsize=9, color=ORANGE)
    draw_arrow(ax, 4.5, 5.5, 3.5, 5.5, GRAY)
    ax.text(4, 5.8, 'y_k', fontsize=9, color=GRAY, ha='center')

    # 闭环标注
    draw_arrow(ax, 10, 4, 10, 3, PURPLE)
    ax.text(10.5, 3.5, 'J向量', fontsize=9, color=PURPLE)
    draw_box(ax, 8.5, 0.5, 3, 2, '测试报告\n(版本化归档)', GRAY, 10, 'white')
    draw_arrow(ax, 10, 3, 10, 2.5, PURPLE)

    # 公式
    ax.text(6, 6.7, 'u_k = C(x_k, r_k),  x_{k+1} = P(x_k, u_k, d_k)',
            fontsize=10, ha='center', style='italic', color=DARK,
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.5))

    save_fig(fig, 'PF6-1_fig1.png')

def pf6_1_fig2():
    """场景库管理与故障注入流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-1 图2: 场景库管理与故障注入流程图', fontsize=14, fontweight='bold', pad=15)

    # 场景类型
    y_top = 4.5
    draw_box(ax, 0.5, y_top, 3, 1, '正常工况场景\n(稳态跟踪/变流)', GREEN, 9)
    draw_box(ax, 4.5, y_top, 3, 1, '极端工况场景\n(突增/突降/阶跃)', ORANGE, 9)
    draw_box(ax, 8.5, y_top, 3, 1, '故障注入场景\n(传感器/执行器/通信)', PURPLE, 9)

    # 汇聚
    for x in [2, 6, 10]:
        draw_arrow(ax, x, y_top, 6, 3.5, GRAY)
    draw_box(ax, 4, 2.5, 4, 1, '标准化场景库\n(编号/边界/阈值/约束)', BLUE, 10)

    # 输出
    draw_arrow(ax, 6, 2.5, 6, 1.5, BLUE)
    draw_box(ax, 3, 0.3, 6, 1, '自动加载 -> 闭环仿真 -> 日志采集 -> 指标计算',
             DARK, 9, 'white')

    save_fig(fig, 'PF6-1_fig2.png')

def pf6_1_fig3():
    """闭环仿真与指标评估数据流图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-1 图3: 闭环仿真与指标评估数据流图', fontsize=14, fontweight='bold', pad=15)

    # 六维指标
    metrics = ['e_track\n跟踪误差', 't_settle\n调节时间', 'OS\n超调量',
               'IAE\n误差积分', 'E_ctrl\n控制能耗', 'R_safe\n安全违规率']
    colors = [BLUE, BLUE, ORANGE, BLUE, GREEN, PURPLE]

    for i, (m, c) in enumerate(zip(metrics, colors)):
        x = 0.5 + i * 1.9
        draw_box(ax, x, 3.5, 1.7, 1.2, m, c, 8)

    # 汇聚到评估
    draw_box(ax, 3, 1.5, 6, 1, 'J = [e_track, t_settle, OS, IAE, E_ctrl, R_safe]',
             DARK, 10, 'white')
    for i in range(6):
        x = 1.35 + i * 1.9
        draw_arrow(ax, x, 3.5, 6, 2.5, GRAY)

    # 判定
    draw_arrow(ax, 6, 1.5, 6, 0.8, DARK)
    ax.text(6, 0.4, 'R_safe=0 AND J<=Threshold -> [通过]  |  else -> [未通过]+原因清单',
            fontsize=9, ha='center', color=DARK,
            bbox=dict(boxstyle='round', facecolor=LIGHT_GREEN, alpha=0.5))

    save_fig(fig, 'PF6-1_fig3.png')

def pf6_1_fig4():
    """测试报告生成与归档流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('PF6-1 图4: 测试报告生成与归档流程图', fontsize=14, fontweight='bold', pad=15)

    steps = [
        ('场景配置\n快照', BLUE),
        ('关键曲线\n生成', GREEN),
        ('指标统计\n汇总', PURPLE),
        ('故障响应\n分析', ORANGE),
        ('版本化\n归档', DARK),
    ]
    for i, (s, c) in enumerate(steps):
        x = 0.5 + i * 2.3
        draw_box(ax, x, 2, 1.8, 1.5, s, c, 9)
        if i < len(steps)-1:
            draw_arrow(ax, x+1.8, 2.75, x+2.3, 2.75, GRAY)

    # 底部标注
    ax.text(6, 0.8, '测试报告 = {版本号, 时间戳, 参数快照, 审批签名}',
            fontsize=10, ha='center', color=DARK,
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.5))

    save_fig(fig, 'PF6-1_fig4.png')

# ===================== PF6-2 HIL测试系统 =====================

def pf6_2_fig1():
    """HIL系统总体架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF6-2 图1: HIL系统总体架构图', fontsize=14, fontweight='bold', pad=15)

    # 六大模块
    draw_box(ax, 0.5, 5.5, 3.5, 1.5, '实时仿真器 Pr\n(明渠/管网水动力)', GREEN, 10)
    draw_box(ax, 5, 5.5, 3.5, 1.5, '被测硬件 H\n(PLC/RTU/SCADA)', BLUE, 10)
    draw_box(ax, 0.5, 3, 3.5, 1.5, '协议适配 A\n(OPC-UA/Modbus/IEC104)', ORANGE, 9)
    draw_box(ax, 5, 3, 3.5, 1.5, '时间同步 Ts\n(主从时钟+缓冲补偿)', PURPLE, 9)
    draw_box(ax, 0.5, 0.5, 3.5, 1.5, '故障注入 Fi\n(通信/设备/计算)', ORANGE, 10)
    draw_box(ax, 5, 0.5, 3.5, 1.5, '评估归档 E\n(指标+报告)', GRAY, 10)

    # 闭环箭头
    draw_arrow(ax, 4, 6.25, 5, 6.25, BLUE)
    ax.text(4.5, 6.6, 'y_k', fontsize=9, color=GREEN)
    draw_arrow(ax, 5, 6, 4, 6, GREEN)
    ax.text(4.5, 5.7, 'u_k', fontsize=9, color=BLUE)

    # 连接线
    draw_arrow(ax, 2.25, 4.5, 2.25, 5.5, ORANGE)
    draw_arrow(ax, 6.75, 4.5, 6.75, 5.5, PURPLE)
    draw_arrow(ax, 2.25, 2, 2.25, 3, ORANGE)
    draw_arrow(ax, 6.75, 2, 6.75, 3, GRAY)

    # 右侧标注
    ax.text(10, 6.5, '闭环交互:\nu_k = H(y_k)\nx_{k+1} = Pr(x_k,u_k,d_k)',
            fontsize=9, color=DARK, va='center',
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.5))
    ax.text(10, 3.5, '同步条件:\n|dt_s - dt_h| <= eps_t',
            fontsize=9, color=DARK, va='center',
            bbox=dict(boxstyle='round', facecolor=LIGHT_PURPLE, alpha=0.5))

    save_fig(fig, 'PF6-2_fig1.png')

def pf6_2_fig2():
    """硬件-仿真闭环交互时序图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-2 图2: 硬件-仿真闭环交互时序图', fontsize=14, fontweight='bold', pad=15)

    # 时间轴
    lanes = ['仿真器Pr', '协议适配A', '被测硬件H', '同步模块Ts']
    lane_colors = [GREEN, ORANGE, BLUE, PURPLE]
    for i, (lane, lc) in enumerate(zip(lanes, lane_colors)):
        y = 4.5 - i * 1.2
        ax.plot([1, 11], [y, y], color=lc, lw=2, alpha=0.6)
        ax.text(0.3, y, lane, fontsize=9, color=lc, fontweight='bold', va='center')

    # 时间步标注
    for t in range(5):
        x = 2 + t * 2
        ax.plot([x, x], [0.5, 5], color=GRAY, lw=0.5, ls='--', alpha=0.3)
        ax.text(x, 0.3, f't={t}', fontsize=8, ha='center', color=GRAY)

        # 交互箭头
        y_sim = 4.5
        y_proto = 3.3
        y_hw = 2.1
        y_sync = 0.9

        if t < 4:
            # Pr -> A -> H
            ax.annotate('', xy=(x+0.5, y_proto), xytext=(x+0.1, y_sim),
                        arrowprops=dict(arrowstyle='->', color=GREEN, lw=1))
            ax.annotate('', xy=(x+1, y_hw), xytext=(x+0.6, y_proto),
                        arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1))
            # H -> A -> Pr
            ax.annotate('', xy=(x+1.5, y_proto), xytext=(x+1.1, y_hw),
                        arrowprops=dict(arrowstyle='->', color=BLUE, lw=1))
            ax.annotate('', xy=(x+1.8, y_sim), xytext=(x+1.6, y_proto),
                        arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1))

    save_fig(fig, 'PF6-2_fig2.png')

def pf6_2_fig3():
    """时间同步与步长协调流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-2 图3: 时间同步与步长协调流程图', fontsize=14, fontweight='bold', pad=15)

    # 三级策略
    draw_box(ax, 1, 5, 3, 1.2, '计算偏差\ndrift = t_sim - t_hw', BLUE, 9)
    draw_arrow(ax, 4, 5.6, 5, 5.6, BLUE)

    # 判断框
    draw_box(ax, 5, 5, 3, 1.2, '|drift| <= eps_t ?', GRAY, 10, DARK)
    draw_arrow(ax, 8, 5.6, 9, 5.6, GREEN)
    ax.text(8.5, 5.9, 'Yes', fontsize=8, color=GREEN)
    draw_box(ax, 9, 5, 2.5, 1.2, '直接传递\n(正常同步)', GREEN, 9)

    draw_arrow(ax, 6.5, 5, 6.5, 4, ORANGE)
    ax.text(6.8, 4.5, 'No', fontsize=8, color=ORANGE)

    draw_box(ax, 5, 2.8, 3, 1.2, '|drift| <= 3*eps_t ?', GRAY, 10, DARK)
    draw_arrow(ax, 8, 3.4, 9, 3.4, ORANGE)
    ax.text(8.5, 3.7, 'Yes', fontsize=8, color=ORANGE)
    draw_box(ax, 9, 2.8, 2.5, 1.2, '缓冲插值补偿\n(从环形缓冲区)', ORANGE, 9)

    draw_arrow(ax, 6.5, 2.8, 6.5, 1.8, PURPLE)
    ax.text(6.8, 2.3, 'No', fontsize=8, color=PURPLE)

    draw_box(ax, 5, 0.5, 3, 1.2, '步长重整\ndt_s_new = dt_s +\nsign(drift)*min(...)', PURPLE, 8)

    save_fig(fig, 'PF6-2_fig3.png')

def pf6_2_fig4():
    """故障注入、评估判定与报告归档流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-2 图4: 故障注入、评估判定与报告归档', fontsize=14, fontweight='bold', pad=15)

    # 故障类型
    faults = ['通信故障\n(延迟/丢包/乱序)', '设备故障\n(漂移/卡滞/掉线)', '计算故障\n(过载/超时)']
    fcolors = [ORANGE, PURPLE, BLUE]
    for i, (f, c) in enumerate(zip(faults, fcolors)):
        draw_box(ax, 0.3 + i * 3.8, 4, 3.2, 1.2, f, c, 8)
        draw_arrow(ax, 1.9 + i * 3.8, 4, 6, 3.2, GRAY)

    # 评估
    draw_box(ax, 3.5, 2, 5, 1.2, 'J = [L_rt, P_loss, T_recover, R_safe, E_ctrl, S_stab]',
             DARK, 9, 'white')
    draw_arrow(ax, 6, 2, 6, 1.2, DARK)

    # 判定
    ax.text(6, 0.6, 'R_safe=0 -> [通过]+报告归档  |  R_safe>0 -> [未通过]+薄弱环节+整改建议',
            fontsize=9, ha='center', color=DARK,
            bbox=dict(boxstyle='round', facecolor=LIGHT_ORANGE, alpha=0.5))

    save_fig(fig, 'PF6-2_fig4.png')

# ===================== PF6-3 ODD分级测试 =====================

def pf6_3_fig1():
    """ODD参数空间定义与分级映射关系图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-3 图1: ODD参数空间与WNAL分级映射', fontsize=14, fontweight='bold', pad=15)

    # ODD五维
    dims = ['Xi_f\n流量水位域', 'Xi_q\n水质域', 'Xi_m\n设备健康域',
            'Xi_e\n环境扰动域', 'Xi_c\n通信计算域']
    dcolors = [BLUE, GREEN, ORANGE, PURPLE, GRAY]
    for i, (d, c) in enumerate(zip(dims, dcolors)):
        draw_box(ax, 0.3, 5.5 - i * 1.2, 2.5, 0.9, d, c, 8)

    # 中间箭头
    for i in range(5):
        draw_arrow(ax, 2.8, 5.95 - i * 1.2, 4, 3.5, GRAY)

    # ODD空间
    draw_box(ax, 4, 2.8, 3, 1.4, 'ODD参数空间\nXi = [Xi_f,...,Xi_c]', BLUE, 10)

    # 右侧WNAL等级
    draw_arrow(ax, 7, 3.5, 8, 3.5, BLUE)
    levels = ['L0 人工', 'L1 监控', 'L2 部分', 'L3 条件', 'L4 高度', 'L5 完全']
    lcolors = [GRAY, LIGHT_BLUE, BLUE, GREEN, PURPLE, ORANGE]
    for i, (l, c) in enumerate(zip(levels, lcolors)):
        y = 5.8 - i * 0.9
        draw_box(ax, 8.5, y, 3, 0.7, l, c, 8, DARK if c in [LIGHT_BLUE, GRAY] else 'white')

    save_fig(fig, 'PF6-3_fig1.png')

def pf6_3_fig2():
    """WNAL分级测试场景生成流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-3 图2: 分级测试场景生成流程图', fontsize=14, fontweight='bold', pad=15)

    steps = [
        ('确定目标\n等级L_l', BLUE),
        ('划分子域\n正常/边界/故障', GREEN),
        ('分层采样\nLHS+边界加密', ORANGE),
        ('可行性\n筛选', PURPLE),
        ('覆盖率\n检查补充', BLUE),
    ]
    for i, (s, c) in enumerate(steps):
        x = 0.5 + i * 2.3
        draw_box(ax, x, 3, 1.8, 1.5, s, c, 9)
        if i < len(steps) - 1:
            draw_arrow(ax, x + 1.8, 3.75, x + 2.3, 3.75, GRAY)

    # 输出
    draw_arrow(ax, 6, 3, 6, 1.8, DARK)
    draw_box(ax, 3.5, 0.5, 5, 1.2, '测试场景集 S = {s_1,...,s_N}\n(参数+阈值+约束)',
             DARK, 10, 'white')

    save_fig(fig, 'PF6-3_fig2.png')

def pf6_3_fig3():
    """三维评估指标计算与判定流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-3 图3: 三维评估与等级判定', fontsize=14, fontweight='bold', pad=15)

    # 三个维度
    draw_box(ax, 0.5, 5, 3, 1.2, 'C_cov 场景覆盖率\n(alpha=0.3)', BLUE, 9)
    draw_box(ax, 4.5, 5, 3, 1.2, 'P_pass 性能达标率\n(beta=0.3)', GREEN, 9)
    draw_box(ax, 8.5, 5, 3, 1.2, 'S_safe 安全零违规率\n(gamma=0.4)', PURPLE, 9)

    # 汇聚
    for x in [2, 6, 10]:
        draw_arrow(ax, x, 5, 6, 4.2, GRAY)
    draw_box(ax, 3.5, 3, 5, 1.2, 'Score_l = 0.3*C_cov + 0.3*P_pass + 0.4*S_safe',
             DARK, 10, 'white')

    # 判定
    draw_arrow(ax, 6, 3, 6, 2.2, DARK)
    draw_box(ax, 1, 0.5, 4.5, 1.5, 'C_cov>=C_l_th\nP_pass>=P_l_th\nS_safe=1\n-> [通过]认证', GREEN, 9)
    draw_box(ax, 6.5, 0.5, 4.5, 1.5, '不满足\n-> [未通过]\n输出原因+整改建议', ORANGE, 9)
    draw_arrow(ax, 4.5, 2.2, 3.25, 2, GREEN)
    draw_arrow(ax, 7.5, 2.2, 8.75, 2, ORANGE)

    save_fig(fig, 'PF6-3_fig3.png')

def pf6_3_fig4():
    """等级认证结果归档与整改闭环图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-3 图4: 等级认证与整改闭环', fontsize=14, fontweight='bold', pad=15)

    # 流程
    steps = [
        ('执行测试', BLUE, 1, 4),
        ('三维评估', GREEN, 3.5, 4),
        ('等级判定', PURPLE, 6, 4),
    ]
    for s, c, x, y in steps:
        draw_box(ax, x, y, 2, 1, s, c, 10)
    draw_arrow(ax, 3, 4.5, 3.5, 4.5, GRAY)
    draw_arrow(ax, 5.5, 4.5, 6, 4.5, GRAY)

    # 通过
    draw_arrow(ax, 8, 4.5, 9, 4.5, GREEN)
    draw_box(ax, 9, 4, 2.5, 1, '[通过]\n等级证书', GREEN, 9)

    # 未通过->整改->复测
    draw_arrow(ax, 7, 4, 7, 2.8, ORANGE)
    draw_box(ax, 5.5, 1.5, 3, 1.2, '整改建议\n(参数优化/阈值调整)', ORANGE, 9)
    draw_arrow(ax, 5.5, 2.1, 4.5, 2.1, PURPLE)
    draw_box(ax, 2.5, 1.5, 2, 1.2, '策略修改\n+复测', PURPLE, 9)
    draw_arrow(ax, 2, 2.7, 2, 4, BLUE)

    save_fig(fig, 'PF6-3_fig4.png')

# ===================== PF6-4 场景自动生成 =====================

def pf6_4_fig1():
    """ODD参数空间定义与分层采样流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-4 图1: ODD参数空间与分层采样', fontsize=14, fontweight='bold', pad=15)

    # 参数维度
    params = ['zeta_h\n水力工况', 'zeta_d\n需求扰动', 'zeta_a\n执行器能力',
              'zeta_c\n通信条件', 'zeta_f\n故障注入']
    pcolors = [BLUE, GREEN, ORANGE, PURPLE, GRAY]
    for i, (p, c) in enumerate(zip(params, pcolors)):
        draw_box(ax, 0.3 + i * 2.3, 5, 2, 1, p, c, 8)

    # 汇聚到采样
    for i in range(5):
        draw_arrow(ax, 1.3 + i * 2.3, 5, 6, 4.2, GRAY)

    draw_box(ax, 4, 3, 4, 1.2, 'LHS分层采样\nN_0=3000', BLUE, 10)
    draw_arrow(ax, 6, 3, 6, 2.2, BLUE)

    draw_box(ax, 4, 1, 4, 1.2, '约束筛选\n(物理+设备+安全)', ORANGE, 10)
    draw_arrow(ax, 4, 1.6, 3, 1.6, ORANGE)

    ax.text(1.5, 1.6, '不可行场景\n(剔除)', fontsize=9, ha='center', color=ORANGE,
            bbox=dict(boxstyle='round', facecolor=LIGHT_ORANGE, alpha=0.5))
    draw_arrow(ax, 8, 1.6, 9, 1.6, GREEN)
    ax.text(10, 1.6, '可行场景集\nS_f', fontsize=9, ha='center', color=GREEN,
            bbox=dict(boxstyle='round', facecolor=LIGHT_GREEN, alpha=0.5))

    save_fig(fig, 'PF6-4_fig1.png')

def pf6_4_fig2():
    """对抗场景搜索与薄弱点挖掘流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-4 图2: 差分进化对抗场景搜索', fontsize=14, fontweight='bold', pad=15)

    # DE流程
    steps_de = [
        ('初始化种群\nNP=50', BLUE, 0.5, 5),
        ('变异\nv=r1+F*(r2-r3)', GREEN, 3.5, 5),
        ('交叉\nCR=0.9', ORANGE, 6.5, 5),
        ('可行性修复\n+约束检查', PURPLE, 9.5, 5),
    ]
    for s, c, x, y in steps_de:
        draw_box(ax, x, y, 2.5, 1.2, s, c, 8)
    for i in range(3):
        x1 = 3 + i * 3
        draw_arrow(ax, x1, 5.6, x1 + 0.5, 5.6, GRAY)

    # 选择+迭代
    draw_arrow(ax, 10.75, 5, 10.75, 4, PURPLE)
    draw_box(ax, 9, 2.8, 2.5, 1.2, '贪心选择\nmax(J_adv)', BLUE, 9)
    draw_arrow(ax, 9, 3.4, 8, 3.4, GRAY)

    ax.text(7, 3.4, '迭代\nG=120', fontsize=9, ha='center', color=DARK)
    draw_arrow(ax, 6, 3.4, 3.5, 5, GRAY)

    # 目标函数
    draw_box(ax, 1, 2.5, 5, 1.5, 'J_adv = w1*e_track + w2*OS\n+ w3*T_recover - w4*R_safe\n(最大化挑战度)',
             DARK, 9, 'white')

    # 输出
    draw_arrow(ax, 6, 2.5, 6, 1.2, DARK)
    draw_box(ax, 4, 0, 4, 1, '对抗场景集 S_adv\n(160个高挑战场景)', ORANGE, 10)

    save_fig(fig, 'PF6-4_fig2.png')

def pf6_4_fig3():
    """场景有效性评估、聚类去重与覆盖优化流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 6))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 6)
    ax.axis('off')
    ax.set_title('PF6-4 图3: 有效性评估与聚类去重', fontsize=14, fontweight='bold', pad=15)

    # 三维评分
    metrics = ['C_real\n工程真实性', 'C_chall\n挑战度', 'C_div\n多样性']
    mcolors = [GREEN, ORANGE, PURPLE]
    for i, (m, c) in enumerate(zip(metrics, mcolors)):
        draw_box(ax, 0.5 + i * 3.8, 4, 3, 1, m, c, 9)

    for i in range(3):
        draw_arrow(ax, 2 + i * 3.8, 4, 6, 3.2, GRAY)

    draw_box(ax, 4, 2, 4, 1.2, 'V(s) = lambda_1*C_real\n+ lambda_2*C_chall + lambda_3*C_div',
             DARK, 9, 'white')
    draw_arrow(ax, 6, 2, 6, 1.2, DARK)

    draw_box(ax, 3, 0, 6, 1, '聚类去重(delta=0.12) -> 覆盖优化 -> 920个精简场景',
             BLUE, 9)

    save_fig(fig, 'PF6-4_fig3.png')

def pf6_4_fig4():
    """标准化场景库版本管理与回归复用流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 5))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 5)
    ax.axis('off')
    ax.set_title('PF6-4 图4: 场景库版本管理与回归复用', fontsize=14, fontweight='bold', pad=15)

    # 版本链
    versions = ['v1.0\n(920场景)', 'v1.1\n(+增量更新)', 'v2.0\n(+新ODD扩展)']
    for i, v in enumerate(versions):
        x = 1 + i * 3.5
        draw_box(ax, x, 3, 2.5, 1.2, v, BLUE, 9)
        if i < 2:
            draw_arrow(ax, x + 2.5, 3.6, x + 3.5, 3.6, GRAY)

    # 回归测试
    draw_arrow(ax, 6, 3, 6, 2, GREEN)
    draw_box(ax, 3.5, 0.8, 5, 1.2, '回归测试复用\n(去重合并+覆盖验证+测试时长缩短34%)',
             GREEN, 9)

    # 标注
    ax.text(10.5, 1.5, '应用:\n- MIL测试\n- HIL测试\n- WNAL认证',
            fontsize=9, color=DARK, va='center',
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.5))

    save_fig(fig, 'PF6-4_fig4.png')

# ===================== PF6-5 MBD设计验证 =====================

def pf6_5_fig1():
    """MBD设计验证一体化总体架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF6-5 图1: MBD设计验证一体化总体架构', fontsize=14, fontweight='bold', pad=15)

    # 六步流程 (上下两行)
    steps = [
        ('S1: MBD主模型\n(对象集E)', BLUE, 0.5, 5.5),
        ('S2: 多精度模型族\n(PDE/IDZ/SS/Stat)', GREEN, 4, 5.5),
        ('S3: V模型链\n(设计-验证)', PURPLE, 7.5, 5.5),
        ('S4: 分层验证\n(MIL/SIL/HIL)', ORANGE, 0.5, 2.5),
        ('S5: 灵敏度矩阵\n(S_ij=dTheta/dp)', BLUE, 4, 2.5),
        ('S6: 优化回写\n(SQP+版本化)', GREEN, 7.5, 2.5),
    ]
    for s, c, x, y in steps:
        draw_box(ax, x, y, 3, 1.5, s, c, 9)

    # 连接箭头
    draw_arrow(ax, 3.5, 6.25, 4, 6.25, GRAY)
    draw_arrow(ax, 7, 6.25, 7.5, 6.25, GRAY)
    draw_arrow(ax, 9, 5.5, 9, 4.5, GRAY)
    ax.annotate('', xy=(1.5, 4), xytext=(9, 4.3),
                arrowprops=dict(arrowstyle='->', color=GRAY, lw=1.5, connectionstyle='arc3,rad=0.2'))
    draw_arrow(ax, 3.5, 3.25, 4, 3.25, GRAY)
    draw_arrow(ax, 7, 3.25, 7.5, 3.25, GRAY)

    # 回写闭环
    ax.annotate('', xy=(2, 5.5), xytext=(9, 2.5),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2, ls='--',
                                connectionstyle='arc3,rad=-0.4'))
    ax.text(10.5, 4.5, '设计回写\n闭环', fontsize=9, color=ORANGE, fontweight='bold',
            bbox=dict(boxstyle='round', facecolor=LIGHT_ORANGE, alpha=0.5))

    save_fig(fig, 'PF6-5_fig1.png')

def pf6_5_fig2():
    """V模型流程与里程碑对应"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-5 图2: V模型设计-验证流程', fontsize=14, fontweight='bold', pad=15)

    # V形状 - 左支(设计)
    left_steps = ['需求分解', '方案设计', '详细设计']
    for i, s in enumerate(left_steps):
        x = 0.5 + i * 1.5
        y = 5.5 - i * 1.5
        draw_box(ax, x, y, 2, 0.9, s, BLUE, 9)
        if i < 2:
            draw_arrow(ax, x + 2, y + 0.45, x + 1.5, y - 0.6, BLUE)

    # V底部
    draw_box(ax, 4.5, 1.5, 3, 0.9, '编码实现', DARK, 9, 'white')

    # 右支(验证)
    right_steps = ['MIL验证', 'SIL验证', 'HIL验证']
    rcolors = [GREEN, ORANGE, PURPLE]
    for i, (s, c) in enumerate(zip(right_steps, rcolors)):
        x = 7.5 + i * 0.5
        y = 2.5 + i * 1.5
        draw_box(ax, x, y, 2, 0.9, s, c, 9)
        if i < 2:
            draw_arrow(ax, x + 1, y + 0.9, x + 1.5, y + 1.5, c)

    # V底部连接
    draw_arrow(ax, 5, 1.5, 8, 2.5, GRAY)

    # 横向对应线(虚线)
    for i in range(3):
        y = 5.95 - i * 1.5
        x_left = 2.5 + i * 1.5
        x_right = 7.5 + (2-i) * 0.5
        ax.plot([x_left, x_right + 2], [y, y], color=GRAY, ls=':', lw=1, alpha=0.5)
        ax.text((x_left + x_right + 2) / 2, y + 0.15, f'Gamma_{i+1}<=eps_{i+1}',
                fontsize=7, ha='center', color=GRAY)

    # 验收回写
    draw_arrow(ax, 10, 5.5, 11, 6, ORANGE)
    draw_box(ax, 9.5, 6, 2, 0.8, '验收回写', ORANGE, 9)

    save_fig(fig, 'PF6-5_fig2.png')

def pf6_5_fig3():
    """多精度模型族构建与跨层参数映射"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-5 图3: 多精度模型族与跨层映射', fontsize=14, fontweight='bold', pad=15)

    # 模型层级(上到下精度递减)
    models = [
        ('M_pde: PDE水动力模型\n(Saint-Venant方程)', BLUE),
        ('M_idz: IDZ传递函数模型\n(G(s)=(1+tau_m*s)*exp(-tau_d*s)/(A_s*s))', GREEN),
        ('M_ss: 稳态质量平衡模型', ORANGE),
        ('M_stat: 统计代理模型', PURPLE),
    ]
    for i, (m, c) in enumerate(models):
        y = 5.5 - i * 1.3
        draw_box(ax, 1, y, 5.5, 1, m, c, 9)
        if i < 3:
            draw_arrow(ax, 3.75, y, 3.75, y - 0.3, GRAY)

    # 映射矩阵
    draw_box(ax, 7.5, 2.5, 4, 3, '映射矩阵 Pi\n\n渠池: n,B,S0,L\n-> A_s, tau_d, tau_m\n\n'
             '闸门: Cd,W,y0\n-> alpha, beta_up, beta_dn\n\n泵站: 特性曲线映射',
             DARK, 8, 'white')

    # 连接线
    for i in range(4):
        y = 6 - i * 1.3
        draw_arrow(ax, 6.5, y, 7.5, 4, GRAY)

    # 标注
    ax.text(6, 0.5, '精度递减, 计算速度递增', fontsize=10, ha='center', color=GRAY,
            style='italic')
    ax.annotate('', xy=(2, 0.8), xytext=(10, 0.8),
                arrowprops=dict(arrowstyle='<->', color=GRAY, lw=1))

    save_fig(fig, 'PF6-5_fig3.png')

def pf6_5_fig4():
    """灵敏度分析与优化回写流程"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF6-5 图4: 灵敏度分析与SQP优化回写', fontsize=14, fontweight='bold', pad=15)

    # 灵敏度计算
    draw_box(ax, 0.5, 5, 3, 1.2, '设计参数集\nP = {p_1,...,p_m}', BLUE, 9)
    draw_arrow(ax, 3.5, 5.6, 4.5, 5.6, BLUE)
    draw_box(ax, 4.5, 5, 3.5, 1.2, '有限差分\nS_ij = dTheta_i/dp_j', GREEN, 9)
    draw_arrow(ax, 8, 5.6, 9, 5.6, GREEN)
    draw_box(ax, 9, 5, 2.5, 1.2, '关键参数集\nP* (前30%)', PURPLE, 9)

    # SQP优化
    draw_arrow(ax, 10.25, 5, 10.25, 4, PURPLE)
    draw_box(ax, 4, 2.5, 5, 1.5, 'SQP约束优化\nmin J = a1*E_track + a2*E_energy + a3*T_recover\n'
             's.t. R_safe=0, p_min<=p<=p_max', DARK, 9, 'white')
    draw_arrow(ax, 9, 3.25, 9.5, 3.25, GRAY)

    # 回写
    draw_arrow(ax, 6.5, 2.5, 6.5, 1.5, DARK)
    draw_box(ax, 4, 0.3, 5, 1, '设计回写 -> DesignPackage-v{n}\n-> 回归MIL/SIL/HIL验证',
             ORANGE, 9)

    # 回写箭头
    ax.annotate('', xy=(1, 5), xytext=(4, 0.8),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2, ls='--',
                                connectionstyle='arc3,rad=0.3'))
    ax.text(1, 3, '参数\n更新', fontsize=9, color=ORANGE, fontweight='bold')

    save_fig(fig, 'PF6-5_fig4.png')


# ===================== 主函数 =====================

if __name__ == '__main__':
    print("=" * 60)
    print("PF6系列专利图片生成 (5件x4图=20张)")
    print("=" * 60)

    print("\n[PF6-1] MIL测试平台")
    pf6_1_fig1()
    pf6_1_fig2()
    pf6_1_fig3()
    pf6_1_fig4()

    print("\n[PF6-2] HIL测试系统")
    pf6_2_fig1()
    pf6_2_fig2()
    pf6_2_fig3()
    pf6_2_fig4()

    print("\n[PF6-3] ODD分级测试")
    pf6_3_fig1()
    pf6_3_fig2()
    pf6_3_fig3()
    pf6_3_fig4()

    print("\n[PF6-4] 场景自动生成")
    pf6_4_fig1()
    pf6_4_fig2()
    pf6_4_fig3()
    pf6_4_fig4()

    print("\n[PF6-5] MBD设计验证")
    pf6_5_fig1()
    pf6_5_fig2()
    pf6_5_fig3()
    pf6_5_fig4()

    print("\n" + "=" * 60)
    print("全部20张图片生成完毕!")
    print("=" * 60)
