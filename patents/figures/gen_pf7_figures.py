"""
PF7系列专利图片生成脚本
水网操作系统与平台（4件x4图=16张）
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

# ===================== PF7-1 HydroOS架构与资源管理 =====================

def pf7_1_fig1():
    """HydroOS四层架构与层间接口关系图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF7-1 图1: HydroOS四层架构与层间接口关系图', fontsize=14, fontweight='bold', pad=15)

    # 四层从上到下
    layers = [
        (1, 6, 10, 1.2, '决策层 Ld\nHDC/DMPC + 优化决策 + 安全评估', PURPLE),
        (1, 4.3, 10, 1.2, '模型层 Lm\n多精度数字孪生 + 模型服务(PDE/IDZ/稳态)', BLUE),
        (1, 2.6, 10, 1.2, '感知层 Lp\n多源数据采集 + 时空融合 + 质量评估', GREEN),
        (1, 0.9, 10, 1.2, '执行层 Le\n指令下发 + PLC联锁 + 状态回传', ORANGE),
    ]
    for x, y, w, h, text, color in layers:
        draw_box(ax, x, y, w, h, text, color, 10)

    # 层间接口箭头
    for i in range(3):
        y_top = layers[i][1]
        y_bot = layers[i+1][1] + layers[i+1][3]
        mid_x = 6
        draw_arrow(ax, mid_x-0.3, y_top, mid_x-0.3, y_bot+0.05, DARK)
        draw_arrow(ax, mid_x+0.3, y_bot+0.05, mid_x+0.3, y_top, DARK)

    # 统一API标注
    ax.text(0.3, 4.9, '统一\nAPI', fontsize=9, color=DARK, ha='center', va='center',
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, edgecolor=BLUE, alpha=0.7))

    # 右侧：外部应用
    draw_box(ax, 11.2, 4.3, 0.6, 3.0, '上\n层\n应\n用', GRAY, 9)
    draw_arrow(ax, 11, 5.8, 11.2, 5.8, GRAY)

    save_fig(fig, 'PF7-1_fig1.png')

def pf7_1_fig2():
    """统一服务注册、发现与编排流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-1 图2: 统一服务注册、发现与编排流程图', fontsize=14, fontweight='bold', pad=15)

    # 服务提供者
    providers = ['算法服务', '模型服务', '设备驱动', '应用服务']
    for i, name in enumerate(providers):
        draw_box(ax, 0.3+i*2.5, 5, 2, 1, name, BLUE, 9)
        draw_arrow(ax, 1.3+i*2.5, 5, 1.3+i*2.5, 4.2, BLUE)

    # 服务注册中心
    draw_box(ax, 2, 2.8, 8, 1.2, '服务注册中心\nPsi = (id, type, latency, priority, qos, security)', GREEN, 10)

    # 下方流程
    steps = ['服务发现', '服务匹配', '服务编排', '运行监控']
    colors = [LIGHT_BLUE, LIGHT_GREEN, LIGHT_PURPLE, LIGHT_ORANGE]
    edge_colors = [BLUE, GREEN, PURPLE, ORANGE]
    for i, (step, c, ec) in enumerate(zip(steps, colors, edge_colors)):
        x = 0.8 + i*2.8
        draw_box(ax, x, 0.5, 2.2, 1, step, ec, 10)
        draw_arrow(ax, x+1.1, 2.8, x+1.1, 1.5, ec)
        if i < 3:
            draw_arrow(ax, x+2.2, 1.0, x+2.8, 1.0, GRAY)

    save_fig(fig, 'PF7-1_fig2.png')

def pf7_1_fig3():
    """计算-通信-存储资源池与优先级调度流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF7-1 图3: 资源池与优先级调度流程图', fontsize=14, fontweight='bold', pad=15)

    # 资源池
    resources = [('计算 Rc', BLUE, 1), ('通信 Rn', GREEN, 4), ('存储 Rs', PURPLE, 7)]
    for name, color, x in resources:
        draw_box(ax, x, 6, 2.5, 1.2, name, color, 11)

    ax.text(6, 7.5, 'R(t) = [Rc(t), Rn(t), Rs(t)]', fontsize=11, ha='center',
            color=DARK, fontweight='bold')

    # 优先级队列
    queues = [
        ('Q0: 安全联锁\n(最高优先/抢占)', ORANGE, 0.5),
        ('Q1: 实时控制\n(带宽保底>=35%)', BLUE, 3.5),
        ('Q2: 优化分析\n(时间片轮转)', GREEN, 6.5),
        ('Qk: 后台任务\n(尽力而为)', GRAY, 9.5),
    ]
    for text, color, x in queues:
        draw_box(ax, x, 3.5, 2.5, 1.2, text, color, 8)
        draw_arrow(ax, x+1.25, 6, x+1.25, 4.7, color)

    # 调度目标
    draw_box(ax, 2, 0.5, 8, 1.5, 'min J = b1*Tdelay + b2*Pdrop + b3*Uenergy\n'
             's.t. Dcrit<=Dmax, Bctrl>=Bmin, Csafe=1', DARK, 10)
    for x in [1.75, 4.75, 7.75, 10.75]:
        draw_arrow(ax, x, 3.5, 6, 2.0, GRAY)

    save_fig(fig, 'PF7-1_fig3.png')

def pf7_1_fig4():
    """故障降级托底运行与系统健康度闭环优化"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-1 图4: 故障降级与健康度闭环优化', fontsize=14, fontweight='bold', pad=15)

    # WNAL等级阶梯
    levels = ['L5', 'L4', 'L3', 'L2', 'L1']
    colors_l = ['#0D47A1', '#1565C0', '#1976D2', '#42A5F5', '#90CAF9']
    for i, (lv, c) in enumerate(zip(levels, colors_l)):
        draw_box(ax, 0.5+i*1.5, 5-i*0.5, 1.2, 0.8, lv, c, 11)
    ax.text(4.5, 6.2, 'WNAL等级', fontsize=11, ha='center', fontweight='bold')

    # 降级箭头
    for i in range(4):
        draw_arrow(ax, 1.7+i*1.5, 5.1-i*0.5, 2.0+i*1.5, 4.8-i*0.5, ORANGE)
    ax.text(4.5, 3.8, 'Lambda: Li -> Li-1', fontsize=9, color=ORANGE, ha='center',
            bbox=dict(facecolor=LIGHT_ORANGE, edgecolor=ORANGE, boxstyle='round'))

    # 健康度闭环
    draw_box(ax, 7, 4.5, 4.5, 1.5, '系统健康度\nH = n1*Aavail + n2*Rrecover + n3*Sstab', GREEN, 9)
    draw_box(ax, 7, 2, 4.5, 1.5, '参数优化\n调度参数 + 资源配额\n周期更新', PURPLE, 9)
    draw_arrow(ax, 9.25, 4.5, 9.25, 3.5, GREEN)
    draw_arrow(ax, 9.8, 3.5, 9.8, 4.5, PURPLE)

    # 运行日志输入
    draw_box(ax, 7, 0.3, 4.5, 1, '运行日志 + 调度绩效 + 告警记录', GRAY, 9)
    draw_arrow(ax, 9.25, 1.3, 9.25, 2, GRAY)

    # 降级触发条件
    triggers = ['通信中断', '服务超时', '资源越限']
    for i, t in enumerate(triggers):
        ax.text(0.5+i*2.2, 2.5, t, fontsize=8, color=ORANGE, ha='center',
                bbox=dict(facecolor=LIGHT_ORANGE, edgecolor=ORANGE, boxstyle='round,pad=0.2'))

    ax.text(3.5, 1.8, '降级触发条件', fontsize=9, ha='center', fontweight='bold')

    save_fig(fig, 'PF7-1_fig4.png')

# ===================== PF7-2 数据采集质量评估与融合 =====================

def pf7_2_fig1():
    """多源异构数据统一接入与协议适配架构图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-2 图1: 多源异构数据统一接入架构图', fontsize=14, fontweight='bold', pad=15)

    # 数据源
    sources = [
        ('SCADA\n(OPC-UA)', BLUE, 0.3),
        ('IoT\n(MQTT)', GREEN, 2.5),
        ('视频\n(HTTP)', PURPLE, 4.7),
        ('气象\n(File)', ORANGE, 6.9),
        ('人工报送\n(API)', GRAY, 9.1),
    ]
    for name, color, x in sources:
        draw_box(ax, x, 5.5, 2, 1, name, color, 9)

    # 协议适配层
    draw_box(ax, 0.5, 3.5, 11, 1.2, '协议适配层\nOPC-UA / MQTT / HTTP / File / API --> 统一数据模型 U', BLUE, 10)
    for name, color, x in sources:
        draw_arrow(ax, x+1, 5.5, x+1, 4.7, color)

    # 输出
    draw_box(ax, 2, 1, 8, 1.5, '统一数据总线\n时间对齐 + 语义归一化 + 质量标签', GREEN, 11)
    draw_arrow(ax, 6, 3.5, 6, 2.5, GREEN)

    save_fig(fig, 'PF7-2_fig1.png')

def pf7_2_fig2():
    """数据时间同步、语义对齐与质量评估流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-2 图2: 时间同步、语义对齐与质量评估流程', fontsize=14, fontweight='bold', pad=15)

    # 流程步骤
    steps = [
        ('原始数据流\n(多源异构)', GRAY, 0.5, 5),
        ("时间同步\ntau'=tau+Dtau", BLUE, 3, 5),
        ('语义对齐\n量纲/坐标/编码', GREEN, 5.5, 5),
        ('四维质量评估', PURPLE, 8, 5),
    ]
    for text, color, x, y in steps:
        draw_box(ax, x, y, 2.2, 1.2, text, color, 9)
    for i in range(3):
        draw_arrow(ax, steps[i][2]+2.2, 5.6, steps[i+1][2], 5.6, DARK)

    # 四维评估细节
    dims = [('Qc\n完整性', BLUE), ('Qk\n一致性', GREEN), ('Qt\n时效性', ORANGE), ('Qa\n精度', PURPLE)]
    for i, (d, c) in enumerate(dims):
        x = 1.5 + i*2.7
        draw_box(ax, x, 2, 2, 1, d, c, 9)
        if i < 2:
            draw_arrow(ax, 9.1, 5, 9.1-(4-i)*0.5, 3.0, GRAY)

    # 综合评分
    draw_box(ax, 3.5, 0.3, 5, 0.9, 'Qall = w1*Qc + w2*Qk + w3*Qt + w4*Qa', DARK, 10)
    for i in range(4):
        draw_arrow(ax, 2.5+i*2.7, 2, 6, 1.2, GRAY)

    save_fig(fig, 'PF7-2_fig2.png')

def pf7_2_fig3():
    """异常检测、缺失修复与质量标签生成流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-2 图3: 异常检测与缺失修复流程', fontsize=14, fontweight='bold', pad=15)

    # 联合检测
    methods = [('规则阈值', BLUE, 1), ('统计检验', GREEN, 4), ('时序模型', PURPLE, 7)]
    for name, color, x in methods:
        draw_box(ax, x, 5.5, 2.5, 1, name, color, 10)

    draw_box(ax, 3, 3.5, 6, 1.2, '联合异常检测\n突跳/漂移/卡死/重复/乱序', ORANGE, 10)
    for name, color, x in methods:
        draw_arrow(ax, x+1.25, 5.5, x+1.25, 4.7, color)

    # 分层修复
    draw_box(ax, 0.5, 1.2, 3.5, 1.5, '短缺失(<30s)\n线性/样条插值', BLUE, 9)
    draw_box(ax, 4.5, 1.2, 3.5, 1.5, '长缺失(>=30s)\n状态空间预测', GREEN, 9)
    draw_box(ax, 8.5, 1.2, 3, 1.5, '质量标签\nnormal/\nwarning/bad', PURPLE, 9)

    draw_arrow(ax, 4.5, 3.5, 2.25, 2.7, BLUE)
    draw_arrow(ax, 7.5, 3.5, 6.25, 2.7, GREEN)
    draw_arrow(ax, 9, 3.5, 10, 2.7, PURPLE)

    save_fig(fig, 'PF7-2_fig3.png')

def pf7_2_fig4():
    """质量自适应卡尔曼融合与闭环优化流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF7-2 图4: 质量自适应卡尔曼融合与闭环优化', fontsize=14, fontweight='bold', pad=15)

    # 核心公式
    draw_box(ax, 1, 6, 10, 1.2, '质量自适应融合核心\nRk = R0 * exp(gamma*(1-Qall))', BLUE, 11)

    # 融合流程
    draw_box(ax, 0.5, 3.8, 3, 1.5, '状态预测\nx_pred = F*x\nP_pred = F*P*F^T+Q', GREEN, 9)
    draw_box(ax, 4.5, 3.8, 3, 1.5, '质量调节\n高Qall->小Rk(信任)\n低Qall->大Rk(降权)', ORANGE, 9)
    draw_box(ax, 8.5, 3.8, 3, 1.5, '状态更新\nK = P*H^T*S^(-1)\nx = x_pred+K*v', PURPLE, 9)

    draw_arrow(ax, 3.5, 4.5, 4.5, 4.5, DARK)
    draw_arrow(ax, 7.5, 4.5, 8.5, 4.5, DARK)
    draw_arrow(ax, 6, 6, 6, 5.3, BLUE)

    # 闭环
    draw_box(ax, 3, 1, 6, 1.5, '闭环优化\n历史误差反馈 --> 更新w_i/阈值/参数', DARK, 10)
    draw_arrow(ax, 10, 3.8, 10, 2.8, PURPLE)
    draw_arrow(ax, 10, 2.8, 9, 2.5, GRAY)
    draw_arrow(ax, 3, 2.5, 2, 2.8, GRAY)
    draw_arrow(ax, 2, 2.8, 2, 3.8, GREEN)

    # 输出
    draw_box(ax, 0.5, 1, 2, 1, '融合输出\n状态+标签', GREEN, 9)
    draw_arrow(ax, 2, 3.8, 1.5, 2.0, GREEN)

    save_fig(fig, 'PF7-2_fig4.png')

# ===================== PF7-3 可视化监控与人机交互 =====================

def pf7_3_fig1():
    """水网拓扑语义图构建与实时数据映射流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-3 图1: 拓扑语义图构建与数据映射', fontsize=14, fontweight='bold', pad=15)

    # 拓扑图 G = (V, E, A)
    draw_box(ax, 1, 4.5, 3, 1.5, '节点集 V\n渠池/泵站/闸站/分水口', BLUE, 9)
    draw_box(ax, 4.5, 4.5, 3, 1.5, '连接边 E\n水力连接关系', GREEN, 9)
    draw_box(ax, 8, 4.5, 3.5, 1.5, '属性集 A\n流量/水位/水质/告警', PURPLE, 9)

    ax.text(6, 6.5, 'G = (V, E, A)', fontsize=13, ha='center', fontweight='bold', color=DARK)

    # 实时数据映射
    draw_box(ax, 1, 2, 10, 1.5, '实时数据流映射\nSCADA遥测 + IoT感知 + 视频分析 --> 拓扑属性实时刷新', ORANGE, 10)
    draw_arrow(ax, 6, 4.5, 6, 3.5, DARK)

    # 输出
    draw_box(ax, 3, 0.2, 6, 1, '拓扑语义图(实时)\n支持渲染/查询/交互', DARK, 10)
    draw_arrow(ax, 6, 2, 6, 1.2, DARK)

    save_fig(fig, 'PF7-3_fig1.png')

def pf7_3_fig2():
    """一张图动态渲染与安全边界叠加示意图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-3 图2: 一张图动态渲染与安全边界叠加', fontsize=14, fontweight='bold', pad=15)

    # 渲染图层
    layers_viz = [
        ('水位等值着色', BLUE, 0.5, 5),
        ('流量方向动画', GREEN, 3.2, 5),
        ('设备状态图标', PURPLE, 5.9, 5),
        ('安全边界叠加', ORANGE, 8.6, 5),
    ]
    for text, color, x, y in layers_viz:
        draw_box(ax, x, y, 2.5, 1, text, color, 9)

    # 渲染函数
    draw_box(ax, 2, 2.8, 8, 1.5, '渲染函数  It = R(G, Xt, Omega_t)\n实时状态Xt + ODD安全配置Omega_t', DARK, 11)
    for text, color, x, y in layers_viz:
        draw_arrow(ax, x+1.25, 5, x+1.25, 4.3, color)

    # 输出
    draw_box(ax, 3, 0.5, 6, 1.2, '运行态势一张图\n(1s核心刷新 / 3s全局刷新)', GREEN, 11)
    draw_arrow(ax, 6, 2.8, 6, 1.7, GREEN)

    save_fig(fig, 'PF7-3_fig2.png')

def pf7_3_fig3():
    """多尺度无缝缩放流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-3 图3: 多尺度无缝缩放流程', fontsize=14, fontweight='bold', pad=15)

    # 四级尺度
    scales = [
        ('S0: 全网\n风险区域着色', '#0D47A1', 0.5),
        ('S1: 分段\n边界流量+安全余量', '#1565C0', 3),
        ('S2: 渠池\n执行器+耦合影响', '#1976D2', 5.5),
        ('S3: 断面\n局部预测曲线', '#42A5F5', 8),
    ]
    for text, color, x in scales:
        draw_box(ax, x, 4.5, 2.3, 1.5, text, color, 8)
    for i in range(3):
        draw_arrow(ax, scales[i][2]+2.3, 5.2, scales[i+1][2], 5.2, DARK)

    # 语义保持映射
    draw_box(ax, 2, 2, 8, 1.5, '语义保持映射 Phi: G_Si --> G_Sj\n关键指标跨尺度跳变率 < 2.5%', PURPLE, 11)
    draw_arrow(ax, 6, 4.5, 6, 3.5, PURPLE)

    # 标注
    ax.text(6, 0.8, '缩放过程中关键指标连续, 上下文不丢失', fontsize=10, ha='center',
            color=DARK, style='italic')

    save_fig(fig, 'PF7-3_fig3.png')

def pf7_3_fig4():
    """自然语言交互、物理校核与反馈优化闭环"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF7-3 图4: 自然语言交互与物理校核闭环', fontsize=14, fontweight='bold', pad=15)

    # 流程
    draw_box(ax, 0.5, 5.5, 2.5, 1.5, '用户输入u\n(文本/语音/模板)', BLUE, 9)
    draw_box(ax, 3.5, 5.5, 2.5, 1.5, '意图解析\nT=(intent,scope,\nconstraints,action)', GREEN, 8)
    draw_box(ax, 6.5, 5.5, 2.5, 1.5, '任务编排\n查询/仿真/\n调度建议', PURPLE, 9)
    draw_box(ax, 9.5, 5.5, 2, 1.5, '候选方案\n生成', ORANGE, 9)

    draw_arrow(ax, 3, 6.2, 3.5, 6.2, DARK)
    draw_arrow(ax, 6, 6.2, 6.5, 6.2, DARK)
    draw_arrow(ax, 9, 6.2, 9.5, 6.2, DARK)

    # 物理校核
    draw_box(ax, 3, 3, 6, 1.5, '物理校核  V(a) = 1[g(a)<=0 AND h(a)=0 AND Csafe=1]\n水动力约束 + 等式约束 + 安全边界', ORANGE, 10)
    draw_arrow(ax, 10.5, 5.5, 10.5, 4.8, ORANGE)
    draw_arrow(ax, 10.5, 4.8, 9, 4.5, ORANGE)

    # 校核结果
    draw_box(ax, 0.5, 3, 2, 1.5, '通过:\n输出可执行\n建议', GREEN, 9)
    draw_box(ax, 9.5, 3, 2, 1.5, '未通过:\n冲突约束+\n修正建议', ORANGE, 9)
    draw_arrow(ax, 3, 3.7, 2.5, 3.7, GREEN)
    draw_arrow(ax, 9, 3.7, 9.5, 3.7, ORANGE)

    # 闭环
    draw_box(ax, 3, 0.5, 6, 1.5, '交互闭环优化\nQhmi = l1*Acc + l2/Tresp + l3*Sat\n更新: 图层策略 + 术语词典 + 模板', DARK, 9)
    draw_arrow(ax, 1.5, 3, 1.5, 2.3, GREEN)
    draw_arrow(ax, 1.5, 2.3, 3, 1.5, GRAY)

    save_fig(fig, 'PF7-3_fig4.png')

# ===================== PF7-4 知识积累与自进化 =====================

def pf7_4_fig1():
    """运行决策三元组自动记录与案例入库流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-4 图1: 三元组自动记录与案例入库', fontsize=14, fontweight='bold', pad=15)

    # 三元组
    draw_box(ax, 0.5, 4.5, 3, 1.5, '工况上下文 c\n来水/需水/设备/ODD', BLUE, 9)
    draw_box(ax, 4.2, 4.5, 3, 1.5, '决策动作 a\n闸泵指令/调度策略', GREEN, 9)
    draw_box(ax, 7.9, 4.5, 3.5, 1.5, '执行效果 e\n水位偏差/能耗/恢复', PURPLE, 9)

    ax.text(6, 6.5, 'kappa = (c, a, e)', fontsize=13, ha='center', fontweight='bold', color=DARK)

    # 质量评分
    draw_box(ax, 2, 2, 8, 1.5, '案例质量评分\nScore = a1*Qdata + a2*Qsafety + a3*Qeffect + a4*Qtrace', ORANGE, 10)
    draw_arrow(ax, 2, 4.5, 4, 3.5, DARK)
    draw_arrow(ax, 5.7, 4.5, 6, 3.5, DARK)
    draw_arrow(ax, 9.6, 4.5, 8, 3.5, DARK)

    # 案例库
    draw_box(ax, 3.5, 0.3, 5, 1, '案例库 K\n高价值案例筛选入库', DARK, 10)
    draw_arrow(ax, 6, 2, 6, 1.3, DARK)

    save_fig(fig, 'PF7-4_fig1.png')

def pf7_4_fig2():
    """案例聚类与模式挖掘流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-4 图2: 案例聚类与模式挖掘', fontsize=14, fontweight='bold', pad=15)

    # 输入
    draw_box(ax, 1, 5, 3, 1.2, '高价值案例库\nphi(kappa)特征向量', BLUE, 10)

    # 聚类
    draw_box(ax, 5, 5, 3, 1.2, '层次聚类\nC = Cluster({phi})', GREEN, 10)
    draw_arrow(ax, 4, 5.6, 5, 5.6, DARK)

    # 模式
    patterns = [
        ('稳定供水\n(9类)', BLUE, 0.5),
        ('季节切换\n(6类)', GREEN, 3),
        ('异常处置\n(5类)', ORANGE, 5.5),
        ('低效能耗\n(4类)', PURPLE, 8),
    ]
    for text, color, x in patterns:
        draw_box(ax, x, 2.5, 2.2, 1.2, text, color, 9)

    draw_arrow(ax, 6.5, 5, 6.5, 4.3, GREEN)
    for text, color, x in patterns:
        draw_arrow(ax, 6.5, 4.3, x+1.1, 3.7, GRAY)

    # 输出
    draw_box(ax, 2, 0.5, 8, 1, '可复用经验片段 + 模式标签', DARK, 10)
    for text, color, x in patterns:
        draw_arrow(ax, x+1.1, 2.5, 6, 1.5, GRAY)

    save_fig(fig, 'PF7-4_fig2.png')

def pf7_4_fig3():
    """知识图构建与规则生成流程图"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 7))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 7)
    ax.axis('off')
    ax.set_title('PF7-4 图3: 知识图构建与规则生成', fontsize=14, fontweight='bold', pad=15)

    # 输入
    draw_box(ax, 0.5, 5, 3, 1.2, '聚类结果\n(24类典型模式)', GREEN, 10)

    # 知识图三元素
    draw_box(ax, 4.5, 5, 2, 1.2, '实体集 E', BLUE, 10)
    draw_box(ax, 7, 5, 2, 1.2, '关系集 R', PURPLE, 10)
    draw_box(ax, 9.5, 5, 2, 1.2, '规则集 P', ORANGE, 10)
    draw_arrow(ax, 3.5, 5.6, 4.5, 5.6, DARK)
    draw_arrow(ax, 6.5, 5.6, 7, 5.6, DARK)
    draw_arrow(ax, 9, 5.6, 9.5, 5.6, DARK)

    # 规则生成
    draw_box(ax, 2, 2.5, 8, 1.5, '规则生成与筛选\npj: conditionj => actionj, conf(pj) >= theta\n(theta=0.82, 312条候选 --> 127条有效)', ORANGE, 10)
    draw_arrow(ax, 10.5, 5, 10.5, 4.3, ORANGE)
    draw_arrow(ax, 10.5, 4.3, 10, 4, ORANGE)

    # 示例规则
    ax.text(6, 1.2, '示例: 上游扰动+需求突增+闸站降级 => 分段缓升+调蓄补偿',
            fontsize=9, ha='center', color=DARK, style='italic',
            bbox=dict(facecolor=LIGHT_ORANGE, edgecolor=ORANGE, boxstyle='round'))

    save_fig(fig, 'PF7-4_fig3.png')

def pf7_4_fig4():
    """策略更新A/B验证与自进化闭环评估"""
    fig, ax = plt.subplots(1, 1, figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    ax.set_title('PF7-4 图4: 策略A/B验证与自进化闭环', fontsize=14, fontweight='bold', pad=15)

    # 参数更新
    draw_box(ax, 1, 6, 4, 1.2, '梯度方向参数更新\nw(t+1) = w(t) + eta*grad_J', BLUE, 10)

    # A/B验证
    draw_box(ax, 6, 6.3, 2.5, 1, '基线组 A\n(原参数w)', GRAY, 9)
    draw_box(ax, 9, 6.3, 2.5, 1, '优化组 B\n(候选w_new)', GREEN, 9)
    draw_arrow(ax, 5, 6.6, 6, 6.6, DARK)

    # 安全约束
    draw_box(ax, 6, 4.5, 5.5, 1.2, '安全零违规硬约束\nIF safety_B=0 AND perf_B>perf_A THEN 接受', ORANGE, 9)
    draw_arrow(ax, 7.25, 6.3, 7.25, 5.7, GRAY)
    draw_arrow(ax, 10.25, 6.3, 10.25, 5.7, GREEN)

    # 进化指标
    draw_box(ax, 1, 3.5, 10, 1.2, '自进化指标  Evo_t = b1*DeltaPerf + b2*DeltaSafety + b3*DeltaRecovery\n12轮迭代: 误差-13.8% / 能耗-8.7% / 恢复-19.4% / 安全违规=0', PURPLE, 9)
    draw_arrow(ax, 8.75, 4.5, 8.75, 4.7, PURPLE)

    # 闭环
    draw_box(ax, 2, 1, 8, 1.5, '闭环回写\n更新: 案例标注 + 规则权重 + 推荐策略\nEvo_t 均值: 0.11 --> 0.29 (90天)', DARK, 10)
    draw_arrow(ax, 6, 3.5, 6, 2.5, DARK)

    # 回到顶部的闭环
    draw_arrow(ax, 2, 2.5, 0.5, 2.5, GRAY)
    draw_arrow(ax, 0.5, 2.5, 0.5, 6.5, GRAY)
    draw_arrow(ax, 0.5, 6.5, 1, 6.5, GRAY)

    save_fig(fig, 'PF7-4_fig4.png')

# ===================== 主函数 =====================

if __name__ == '__main__':
    print("=== PF7系列专利图片生成 (4件x4图=16张) ===\n")

    print("PF7-1: HydroOS架构与资源管理")
    pf7_1_fig1()
    pf7_1_fig2()
    pf7_1_fig3()
    pf7_1_fig4()

    print("\nPF7-2: 数据采集质量评估与融合")
    pf7_2_fig1()
    pf7_2_fig2()
    pf7_2_fig3()
    pf7_2_fig4()

    print("\nPF7-3: 可视化监控与人机交互")
    pf7_3_fig1()
    pf7_3_fig2()
    pf7_3_fig3()
    pf7_3_fig4()

    print("\nPF7-4: 知识积累与自进化")
    pf7_4_fig1()
    pf7_4_fig2()
    pf7_4_fig3()
    pf7_4_fig4()

    print("\n=== 全部16张图片生成完毕 ===")
