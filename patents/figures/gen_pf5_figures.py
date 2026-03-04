"""
PF5系列专利配图生成脚本
PF5：认知智能与大模型（5件）
每件生成4张图，共20张
"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
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
DARK_BLUE = '#0D47A1'
TEAL = '#00796B'

outdir = os.path.dirname(os.path.abspath(__file__))

def save(fig, name):
    fig.savefig(os.path.join(outdir, name), dpi=200, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    plt.close(fig)
    print(f"  Saved {name}")

def draw_box(ax, x, y, w, h, text, color, fontsize=9, textcolor='white'):
    box = FancyBboxPatch((x-w/2, y-h/2), w, h,
                         boxstyle="round,pad=0.05", facecolor=color, edgecolor='none', alpha=0.9)
    ax.add_patch(box)
    ax.text(x, y, text, ha='center', va='center', fontsize=fontsize,
            color=textcolor, fontweight='bold', wrap=True)

def draw_arrow(ax, x1, y1, x2, y2, color='#555555', style='->', lw=1.5):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle=style, color=color, lw=lw))

# ============================================================
# PF5-1: 领域大语言模型构建方法
# ============================================================

def pf5_1_fig1():
    """图1 领域大语言模型构建总体流程图（S1-S6六步）"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off')

    steps = [
        ('S1\n语料治理', 1.2, GRAY),
        ('S2\n术语本体\n+指令集', 3.2, TEAL),
        ('S3\n领域微调\nDAPT+SFT\n+DPO', 5.4, BLUE),
        ('S4\n图谱增强\nRAG', 7.6, PURPLE),
        ('S5\n三重校核\nIDZ+安全\n+规程', 9.8, ORANGE),
        ('S6\n持续学习\n+回归测试', 12.0, GREEN),
    ]

    for text, x, color in steps:
        draw_box(ax, x, 2.8, 1.8, 2.0, text, color, fontsize=10)

    for i in range(len(steps)-1):
        draw_arrow(ax, steps[i][1]+0.95, 2.8, steps[i+1][1]-0.95, 2.8, DARK_BLUE, '->')

    # 回环箭头 S5→S4
    ax.annotate('', xy=(7.6+0.9, 1.5), xytext=(9.8-0.9, 1.5),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(8.7, 0.9, '校核不通过\n检索补强→重生成', ha='center', va='center',
            fontsize=8, color=RED, fontstyle='italic')

    # 回环箭头 S6→S3
    ax.annotate('', xy=(5.4, 4.3), xytext=(12.0, 4.3),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.5, ls='--',
                                connectionstyle='arc3,rad=0.3'))
    ax.text(8.7, 4.7, '增量学习触发再训练', ha='center', va='center',
            fontsize=8, color=GREEN)

    ax.set_title('图1  领域大语言模型构建总体流程', fontsize=14, fontweight='bold', pad=15)
    save(fig, 'PF5-1_fig1.png')

def pf5_1_fig2():
    """图2 水利语料治理与术语本体构建"""
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

    # 数据源
    sources = ['规范标准\n420份', '调度日志\n180万条', '报警记录\n46万条', '学术文献\n1.2万页', 'HydroOS\n知识条目']
    for i, s in enumerate(sources):
        draw_box(ax, 1.5, 5.0 - i*1.0, 2.2, 0.7, s, GRAY, fontsize=8)
        draw_arrow(ax, 2.65, 5.0 - i*1.0, 4.2, 3.0)

    # 治理漏斗
    draw_box(ax, 5.2, 3.0, 2.2, 2.5, '语料治理\n\n脱敏\n去重\n质量评价\nQ=[Qc,Qa,Qt,Qs]', BLUE, fontsize=9)

    draw_arrow(ax, 6.35, 3.0, 7.8, 3.0)

    # 术语本体
    draw_box(ax, 8.8, 4.2, 2.0, 1.0, '术语本体 E×R', TEAL, fontsize=9)
    draw_box(ax, 8.8, 2.8, 2.0, 1.0, '指令数据集\nN=185,000', PURPLE, fontsize=9)
    draw_box(ax, 8.8, 1.4, 2.0, 1.0, '训练语料\n3.8B tokens', DARK_BLUE, fontsize=9)

    # 本体示例
    draw_box(ax, 11.8, 4.2, 2.0, 1.2, '渠池─约束于→\n  最低水位\n泵站─作用于→\n  流量', '#546E7A', fontsize=7, textcolor='white')
    draw_arrow(ax, 9.85, 4.2, 10.75, 4.2)

    ax.set_title('图2  水利语料治理与术语本体构建', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-1_fig2.png')

def pf5_1_fig3():
    """图3 知识图谱增强RAG与约束校核闭环"""
    fig, ax = plt.subplots(figsize=(13, 8))
    ax.set_xlim(0, 13); ax.set_ylim(0, 8); ax.axis('off')

    # 查询输入
    draw_box(ax, 1.5, 6.5, 2.2, 0.8, '用户查询 q', GRAY, fontsize=10)
    draw_arrow(ax, 2.65, 6.5, 3.8, 6.5)

    # 三路检索
    draw_box(ax, 5.0, 7.2, 2.0, 0.7, '向量检索\nTop-k=12', BLUE, fontsize=8)
    draw_box(ax, 5.0, 6.5, 2.0, 0.7, '图谱路径检索\nTop-p=6', PURPLE, fontsize=8)
    draw_box(ax, 5.0, 5.8, 2.0, 0.7, '规则检索\nTop-r=4', GREEN, fontsize=8)
    for y in [7.2, 6.5, 5.8]:
        draw_arrow(ax, 3.8, 6.5, 3.95, y, GRAY)
        draw_arrow(ax, 6.05, y, 7.2, 6.5, GRAY)

    # 融合→生成
    draw_box(ax, 8.0, 6.5, 1.8, 0.8, '证据融合\nEq', TEAL, fontsize=9)
    draw_arrow(ax, 8.95, 6.5, 10.0, 6.5)
    draw_box(ax, 11.0, 6.5, 2.0, 0.8, 'LLM生成\n结论+依据+约束', PURPLE, fontsize=8)

    # 校核层
    draw_arrow(ax, 11.0, 6.05, 11.0, 4.5)
    draw_box(ax, 5.0, 3.5, 2.2, 0.8, 'V_hyd\nIDZ水力校核', BLUE, fontsize=8)
    draw_box(ax, 8.0, 3.5, 2.2, 0.8, 'V_safe\n安全边界校核', ORANGE, fontsize=8)
    draw_box(ax, 11.0, 3.5, 2.2, 0.8, 'V_rule\n规程一致性', GREEN, fontsize=8)
    draw_arrow(ax, 11.0, 4.0, 11.0, 4.5)
    draw_arrow(ax, 9.85, 3.5, 9.15, 3.5)
    draw_arrow(ax, 6.85, 3.5, 6.15, 3.5)

    # 判定
    draw_box(ax, 3.5, 3.5, 1.5, 0.8, '三重校核\n通过?', DARK_BLUE, fontsize=9)
    draw_arrow(ax, 4.85, 3.5, 5.0-1.15, 3.5)

    # 通过路径
    draw_box(ax, 3.5, 1.8, 2.0, 0.8, '[通过] 输出方案\n+ 引用来源', GREEN, fontsize=9)
    draw_arrow(ax, 3.5, 3.05, 3.5, 2.25)
    ax.text(2.7, 2.7, '通过', fontsize=8, color=GREEN)

    # 不通过路径 → 回环
    draw_box(ax, 8.0, 1.8, 2.2, 0.8, '[不通过] 检索补强\n→重生成→再校核', RED, fontsize=8)
    draw_arrow(ax, 3.5+0.75, 3.1, 8.0-1.1, 2.2, RED)
    ax.text(5.5, 2.3, '不通过 (k<N_max=3)', fontsize=8, color=RED)

    ax.annotate('', xy=(8.0, 6.05), xytext=(8.0, 2.25),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2, ls='--',
                                connectionstyle='arc3,rad=-0.5'))

    ax.set_title('图3  知识图谱增强RAG与约束校核闭环', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-1_fig3.png')

def pf5_1_fig4():
    """图4 在线评估与持续学习迭代架构"""
    fig, ax = plt.subplots(figsize=(11, 7))
    ax.set_xlim(0, 11); ax.set_ylim(0, 7); ax.axis('off')

    # 环形闭环
    nodes = [
        ('运行服务\n(问答/调度)', 5.5, 6.0, BLUE),
        ('在线评估\nM=[Acc,Fact,\nExec,Viol,Trace]', 9.5, 4.5, ORANGE),
        ('达标判定\nViol<5%?', 9.5, 2.0, DARK_BLUE),
        ('增量学习\nLoRA+回放缓冲', 5.5, 1.0, PURPLE),
        ('回归测试\nvs 历史基线', 1.5, 2.0, GREEN),
        ('模型更新\n部署', 1.5, 4.5, TEAL),
    ]

    for text, x, y, color in nodes:
        draw_box(ax, x, y, 2.2, 1.2, text, color, fontsize=9)

    # 连接
    draw_arrow(ax, 6.65, 5.7, 8.35, 4.8)
    draw_arrow(ax, 9.5, 3.85, 9.5, 2.65)
    ax.text(10.0, 3.3, '否', fontsize=9, color=RED, fontweight='bold')
    draw_arrow(ax, 8.35, 1.7, 6.65, 1.15, RED)
    draw_arrow(ax, 4.35, 1.15, 2.65, 1.7)
    draw_arrow(ax, 1.5, 2.65, 1.5, 3.85)
    draw_arrow(ax, 2.65, 4.8, 4.35, 5.7)

    # 达标→继续
    ax.text(10.2, 2.0, '是→继续运行', fontsize=9, color=GREEN, fontweight='bold')

    # 触发条件标注
    ax.text(5.5, 3.5, '触发条件:\n- Viol_rate > 5%\n- 新规程发布\n- 评估窗口W=500条',
            ha='center', va='center', fontsize=9, color='#333333',
            bbox=dict(boxstyle='round', facecolor=LIGHT_ORANGE, alpha=0.5))

    ax.set_title('图4  在线评估与持续学习迭代架构', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-1_fig4.png')

# ============================================================
# PF5-2: 调度方案自动生成与评审
# ============================================================

def pf5_2_fig1():
    """图1 大模型驱动调度方案自动生成总体架构"""
    fig, ax = plt.subplots(figsize=(14, 5))
    ax.set_xlim(0, 14); ax.set_ylim(0, 5); ax.axis('off')

    steps = [
        ('自然语言\n调度指令', 1.2, GRAY),
        ('LLM\n需求解析\nψ=[ψd,ψt,\nψs,ψr]', 3.4, PURPLE),
        ('知识图谱\n+规则库\n参数映射', 5.6, TEAL),
        ('物理引擎\nIDZ仿真\n候选方案Π', 7.8, BLUE),
        ('五维评审\nS(π)=ΣwjJj', 10.0, ORANGE),
        ('可解释\n报告输出', 12.2, GREEN),
    ]

    for text, x, color in steps:
        draw_box(ax, x, 3.0, 1.8, 2.0, text, color, fontsize=9)

    for i in range(len(steps)-1):
        draw_arrow(ax, steps[i][1]+0.95, 3.0, steps[i+1][1]-0.95, 3.0, DARK_BLUE)

    # 回环
    ax.annotate('', xy=(5.6, 1.5), xytext=(10.0, 1.5),
                arrowprops=dict(arrowstyle='->', color=RED, lw=2,
                                connectionstyle='arc3,rad=-0.3'))
    ax.text(7.8, 0.8, '未达标→修正权重/边界→重新生成 (≤N_max=5)', ha='center',
            fontsize=9, color=RED, fontstyle='italic')

    ax.set_title('图1  大模型驱动调度方案自动生成总体架构', fontsize=14, fontweight='bold', pad=15)
    save(fig, 'PF5-2_fig1.png')

def pf5_2_fig2():
    """图2 需求结构化与参数映射"""
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

    # NL输入
    draw_box(ax, 1.5, 4.5, 2.5, 1.2, '自然语言指令T\n"未来24h保障A、B\n受水区供水..."', GRAY, 8)

    draw_arrow(ax, 2.8, 4.5, 3.8, 4.5)

    # LLM解析
    draw_box(ax, 5.0, 4.5, 2.0, 1.2, 'LLM\n需求解析', PURPLE, 10)

    draw_arrow(ax, 6.05, 4.5, 7.0, 4.5)

    # 结构化向量
    fields = ['ψd: 受水区=[A,B]', 'ψt: 24h, 15min步长', 'ψs: 裕度=0.1m', 'ψr: 供水>能耗']
    for i, f in enumerate(fields):
        draw_box(ax, 8.5, 5.2 - i*0.7, 2.5, 0.55, f, LIGHT_PURPLE, 7, 'black')

    # 映射
    draw_arrow(ax, 9.8, 3.5, 10.5, 2.5)
    draw_box(ax, 6.5, 2.0, 2.5, 1.0, '知识图谱\n+规则库', TEAL, 9)
    draw_arrow(ax, 7.8, 2.0, 10.0, 2.0)

    # 参数集P
    draw_box(ax, 11.5, 2.0, 2.2, 1.8, 'P = JSON\nQ_ref(t)\nH_lim\nU_lim\nΩ, Λ', BLUE, 8)

    draw_arrow(ax, 11.5, 0.9, 11.5, 0.3)
    ax.text(11.5, 0.1, '→ REST API → 物理引擎', ha='center', fontsize=9, color=DARK_BLUE)

    ax.set_title('图2  自然语言需求结构化与参数映射', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-2_fig2.png')

def pf5_2_fig3():
    """图3 物理引擎仿真与多维评审（含雷达图）"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5),
                                     gridspec_kw={'width_ratios': [1.5, 1]})
    # 左侧流程
    ax1.set_xlim(0, 8); ax1.set_ylim(0, 6); ax1.axis('off')
    draw_box(ax1, 2.0, 5.0, 3.0, 0.8, '参数集 P → IDZ/水动力模型', BLUE, 9)
    draw_arrow(ax1, 2.0, 4.55, 2.0, 4.0)
    draw_box(ax1, 2.0, 3.5, 3.0, 0.8, '候选方案 Pi={pi_1,...,pi_12}', TEAL, 9)
    draw_arrow(ax1, 2.0, 3.05, 2.0, 2.5)
    draw_box(ax1, 2.0, 2.0, 3.0, 0.8, '五维评审 S(pi_i)=Sum(w_j*J_j)', ORANGE, 9)
    draw_arrow(ax1, 2.0, 1.55, 2.0, 1.0)
    draw_box(ax1, 2.0, 0.5, 3.0, 0.8, '最优 π* (S=0.91)', GREEN, 9)

    # 指标列表
    metrics = ['J_supply = 99.1%', 'J_energy = 6.8%↓', 'J_safety = 100%', 'J_stability = 0.94', 'J_robust = 0.88']
    for i, m in enumerate(metrics):
        ax1.text(5.5, 4.5 - i*0.7, m, fontsize=9, color=DARK_BLUE,
                bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.4))

    ax1.set_title('仿真与评审流程', fontsize=12, fontweight='bold')

    # 右侧雷达图
    categories = ['供水\n达标率', '能耗\n节省率', '安全\n合规率', '水位\n稳定性', '扰动\n鲁棒性']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    ax2 = fig.add_subplot(122, polar=True)
    values_ours = [0.99, 0.85, 1.0, 0.94, 0.88]
    values_base = [0.73, 0.50, 0.78, 0.71, 0.62]
    values_ours += values_ours[:1]
    values_base += values_base[:1]

    ax2.plot(angles, values_ours, 'o-', linewidth=2, color=BLUE, label='本发明')
    ax2.fill(angles, values_ours, alpha=0.15, color=BLUE)
    ax2.plot(angles, values_base, 's--', linewidth=1.5, color=GRAY, label='人工方案')
    ax2.fill(angles, values_base, alpha=0.1, color=GRAY)
    ax2.set_xticks(angles[:-1])
    ax2.set_xticklabels(categories, fontsize=8)
    ax2.set_ylim(0, 1.1)
    ax2.legend(fontsize=8, loc='lower right')
    ax2.set_title('五维评审雷达图', fontsize=12, fontweight='bold', pad=15)

    fig.suptitle('图3  物理引擎仿真与多维评审', fontsize=14, fontweight='bold', y=1.02)
    fig.tight_layout()
    save(fig, 'PF5-2_fig3.png')

def pf5_2_fig4():
    """图4 生成—仿真—评审—修正闭环状态图"""
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis('off')

    draw_box(ax, 2.0, 5.0, 1.8, 0.8, 'START', GRAY, 10)
    draw_arrow(ax, 2.0, 4.55, 2.0, 4.0)
    draw_box(ax, 2.0, 3.5, 1.8, 0.8, '生成', PURPLE, 10)
    draw_arrow(ax, 2.95, 3.5, 3.8, 3.5)
    draw_box(ax, 4.8, 3.5, 1.8, 0.8, '仿真', BLUE, 10)
    draw_arrow(ax, 5.75, 3.5, 6.6, 3.5)
    draw_box(ax, 7.5, 3.5, 1.8, 0.8, '评审', ORANGE, 10)
    draw_arrow(ax, 7.5, 3.05, 7.5, 2.2)

    # 判定
    draw_box(ax, 7.5, 1.5, 2.0, 1.0, '达标?\nS≥S_th', DARK_BLUE, 9)

    # 达标→发布
    draw_arrow(ax, 8.55, 1.5, 9.8, 1.5)
    draw_box(ax, 10.2, 1.5, 1.2, 0.8, 'END\n发布报告', GREEN, 8)

    # 不达标→修正→回环
    draw_arrow(ax, 7.5, 0.95, 7.5, 0.3)
    ax.text(8.0, 0.6, 'k<N_max', fontsize=8, color=RED)
    draw_box(ax, 4.8, 0.5, 2.2, 0.7, '修正策略\n权重/边界/模板', RED, 8)
    draw_arrow(ax, 7.5-1.0, 0.3, 4.8+1.1, 0.5, RED)
    draw_arrow(ax, 4.8-1.1, 0.8, 2.0, 3.05, RED)

    # 超次数→不可行
    draw_box(ax, 4.8, 1.5, 2.0, 0.7, 'k=N_max\n不可行原因清单', '#795548', 7)
    draw_arrow(ax, 6.45, 1.5, 5.85, 1.5, '#795548')

    ax.set_title('图4  生成—仿真—评审—修正闭环状态图', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-2_fig4.png')

# ============================================================
# PF5-3: 多模态异常识别
# ============================================================

def pf5_3_fig1():
    """图1 多模态数据采集与统一时间轴对齐"""
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis('off')

    sources = [
        ('SCADA时序\n采样1s', 1.5, 4.2, BLUE),
        ('GIS拓扑\n空间数据', 1.5, 3.2, GREEN),
        ('视频监控\n30fps', 1.5, 2.2, PURPLE),
        ('运行日志\n文本', 1.5, 1.2, ORANGE),
    ]

    for text, x, y, color in sources:
        draw_box(ax, x, y, 2.0, 0.7, text, color, 8)

    # 时间对齐
    draw_box(ax, 5.5, 2.7, 2.5, 2.8, '时间同步\nA(·)\n\n重采样\n延迟校正\n关键帧提取\nΔt=10s', DARK_BLUE, 9)

    for _, _, y, _ in sources:
        draw_arrow(ax, 2.55, y, 4.2, 2.7)

    draw_arrow(ax, 6.8, 2.7, 7.8, 2.7)

    # 对齐输出
    draw_box(ax, 9.0, 4.0, 2.0, 0.6, "X't (128-d)", LIGHT_BLUE, 8, 'black')
    draw_box(ax, 9.0, 3.2, 2.0, 0.6, "X'g (96-d)", LIGHT_GREEN, 8, 'black')
    draw_box(ax, 9.0, 2.4, 2.0, 0.6, "X'v (128-d)", LIGHT_PURPLE, 8, 'black')
    draw_box(ax, 9.0, 1.6, 2.0, 0.6, "X'l (96-d)", LIGHT_ORANGE, 8, 'black')

    draw_box(ax, 11.8, 2.8, 2.0, 1.0, '统一时间窗\n[k-τ, k]', TEAL, 9)
    draw_arrow(ax, 10.05, 2.8, 10.75, 2.8)

    ax.set_title('图1  多模态数据采集与统一时间轴对齐', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-3_fig1.png')

def pf5_3_fig2():
    """图2 四通道特征提取与注意力融合"""
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

    channels = [
        ('时序编码器\nLSTM/Trans.', 'ft in R^128', BLUE, 5.0),
        ('图神经网络\nGCN/GAT', 'fg in R^96', GREEN, 3.8),
        ('视觉编码器\nResNet/ViT', 'fv in R^128', PURPLE, 2.6),
        ('语言编码器\nBERT微调', 'fl in R^96', ORANGE, 1.4),
    ]

    for text, feat, color, y in channels:
        draw_box(ax, 2.5, y, 2.2, 0.8, text, color, 8)
        draw_box(ax, 5.8, y, 1.8, 0.6, feat, color, 8)
        draw_arrow(ax, 3.65, y, 4.85, y)
        draw_arrow(ax, 6.75, y, 7.8, 3.2)

    # 融合
    draw_box(ax, 9.0, 3.2, 2.5, 1.5, '注意力融合\nz = Σ αm·fm\n\nα = Softmax\n(qm × rm)\n缺失→掩码', DARK_BLUE, 8)

    draw_arrow(ax, 10.3, 3.2, 11.3, 3.2)
    draw_box(ax, 12.0, 3.2, 1.3, 0.8, '融合\n表示 z', TEAL, 9)

    ax.set_title('图2  四通道特征提取与注意力融合', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-3_fig2.png')

def pf5_3_fig3():
    """图3 异常分类、置信度计算与分级告警"""
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

    draw_box(ax, 1.5, 3.0, 1.5, 0.8, '融合 z', TEAL, 10)
    draw_arrow(ax, 2.3, 3.0, 3.0, 3.0)

    # 分类器
    draw_box(ax, 4.0, 3.0, 2.0, 0.8, '异常分类器\nP(y|z)', PURPLE, 9)

    # 事件类别
    events = ['泄漏', '溢流', '设备故障', '水质异常', '外部入侵']
    for i, e in enumerate(events):
        draw_box(ax, 4.0, 5.5 - i*0.5, 1.2, 0.35, e, LIGHT_PURPLE, 7, 'black')

    # 置信度计算
    draw_arrow(ax, 5.05, 3.0, 6.0, 3.0)
    inputs_conf = [
        ('p_cls\n分类概率', 7.5, 4.5, PURPLE),
        ('q_data\n数据质量', 7.5, 3.0, BLUE),
        ('s_topo\n拓扑一致性', 7.5, 1.5, GREEN),
    ]
    for text, x, y, color in inputs_conf:
        draw_box(ax, x, y, 1.8, 0.8, text, color, 8)
        draw_arrow(ax, 8.45, y, 9.2, 3.0)

    # 融合
    draw_box(ax, 10.0, 3.0, 2.0, 1.0, 'Conf =\nlambda_1*p + lambda_2*q + lambda_3*s', DARK_BLUE, 8)

    # 分级告警
    draw_arrow(ax, 11.05, 3.0, 11.8, 3.0)
    draw_box(ax, 12.3, 4.0, 1.0, 0.5, '一级\n红', RED, 8)
    draw_box(ax, 12.3, 3.0, 1.0, 0.5, '二级\n橙', ORANGE, 8)
    draw_box(ax, 12.3, 2.0, 1.0, 0.5, '三级\n黄', YELLOW, 8, 'black')

    ax.set_title('图3  异常分类、置信度计算与分级告警', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-3_fig3.png')

def pf5_3_fig4():
    """图4 在线反馈与增量学习闭环"""
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5); ax.axis('off')

    nodes = [
        ('分级告警\n输出', 1.5, 3.5, ORANGE),
        ('人工确认\n+处置', 3.8, 3.5, GRAY),
        ('回写\n样本池', 6.0, 3.5, TEAL),
        ('触发判断\nFPR>5%?\n新类型?', 8.2, 3.5, DARK_BLUE),
        ('增量训练\ntheta←theta-mu*grad(L)', 8.2, 1.5, PURPLE),
        ('模型更新\n部署', 4.8, 1.5, GREEN),
    ]

    for text, x, y, color in nodes:
        draw_box(ax, x, y, 1.8, 1.0, text, color, 8)

    draw_arrow(ax, 2.45, 3.5, 2.85, 3.5)
    draw_arrow(ax, 4.75, 3.5, 5.05, 3.5)
    draw_arrow(ax, 6.95, 3.5, 7.25, 3.5)
    draw_arrow(ax, 8.2, 2.95, 8.2, 2.05, RED)
    ax.text(8.8, 2.5, '是', fontsize=9, color=RED)
    draw_arrow(ax, 7.25, 1.5, 5.75, 1.5)
    draw_arrow(ax, 3.85, 1.5, 1.5, 2.95)

    ax.text(9.5, 3.5, '否→\n继续监控', fontsize=8, color=GREEN)

    ax.set_title('图4  在线反馈与增量学习闭环', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-3_fig4.png')

# ============================================================
# PF5-4: 双引擎协同决策
# ============================================================

def pf5_4_fig1():
    """图1 大模型与物理引擎双层协同架构"""
    fig, ax = plt.subplots(figsize=(13, 7))
    ax.set_xlim(0, 13); ax.set_ylim(0, 7); ax.axis('off')

    # 认知层
    ax.add_patch(FancyBboxPatch((0.5, 4.0), 12, 2.2, boxstyle="round,pad=0.1",
                                 facecolor=LIGHT_PURPLE, edgecolor=PURPLE, lw=2, alpha=0.3))
    ax.text(6.5, 6.0, '认知层（大模型）', ha='center', fontsize=12, color=PURPLE, fontweight='bold')

    draw_box(ax, 2.5, 4.8, 2.2, 0.8, 'NL需求\n场景理解', PURPLE, 9)
    draw_box(ax, 5.5, 4.8, 2.2, 0.8, '候选方案\n构思 Pi_0', PURPLE, 9)
    draw_box(ax, 8.5, 4.8, 2.2, 0.8, '定向修正\n→ Πk+1', '#9C27B0', 9)
    draw_arrow(ax, 3.65, 4.8, 4.35, 4.8)
    draw_arrow(ax, 6.65, 4.8, 7.35, 4.8)

    # 验证层
    ax.add_patch(FancyBboxPatch((0.5, 0.8), 12, 2.2, boxstyle="round,pad=0.1",
                                 facecolor=LIGHT_BLUE, edgecolor=BLUE, lw=2, alpha=0.3))
    ax.text(6.5, 2.8, '验证层（物理引擎）', ha='center', fontsize=12, color=BLUE, fontweight='bold')

    draw_box(ax, 2.5, 1.6, 2.0, 0.8, 'IDZ仿真\nV_hyd', BLUE, 9)
    draw_box(ax, 5.5, 1.6, 2.0, 0.8, '安全校核\nV_safe', ORANGE, 9)
    draw_box(ax, 8.5, 1.6, 2.0, 0.8, '规程校核\nV_rule', GREEN, 9)
    draw_arrow(ax, 3.55, 1.6, 4.45, 1.6)
    draw_arrow(ax, 6.55, 1.6, 7.45, 1.6)

    # 方案下发
    draw_arrow(ax, 5.5, 4.35, 5.5, 2.05, DARK_BLUE, '->')
    ax.text(5.9, 3.3, '方案下发\n(JSON)', fontsize=8, color=DARK_BLUE)

    # 失败解释反馈
    draw_arrow(ax, 8.5, 2.05, 8.5, 4.35, RED, '->')
    ax.text(9.0, 3.3, '失败解释E\n(违规项+\n时段+幅度)', fontsize=8, color=RED)

    # 评估输出
    draw_box(ax, 11.5, 1.6, 1.5, 0.8, '评估\nRi=[J...]', TEAL, 8)
    draw_arrow(ax, 9.55, 1.6, 10.7, 1.6)

    # 接口
    draw_box(ax, 11.5, 4.8, 1.5, 0.8, '接口 I\n[G,C,B,\nΩ,T]', '#546E7A', 7)

    ax.set_title('图1  大模型与物理引擎双层协同架构', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-4_fig1.png')

def pf5_4_fig2():
    """图2 认知→物理数据接口流程"""
    fig, ax = plt.subplots(figsize=(13, 4.5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 4.5); ax.axis('off')

    steps = [
        ('NL输入', 1.0, GRAY),
        ('LLM解析', 2.8, PURPLE),
        ('结构化JSON\nQ_ref, u(t)\n风险说明', 5.0, '#546E7A'),
        ('标准化接口\nREST API', 7.2, TEAL),
        ('物理引擎\nIDZ仿真', 9.2, BLUE),
        ('状态轨迹\n+违规记录\n→R_i', 11.5, ORANGE),
    ]

    for text, x, color in steps:
        draw_box(ax, x, 2.5, 1.8, 1.5, text, color, 8)

    for i in range(len(steps)-1):
        draw_arrow(ax, steps[i][1]+0.95, 2.5, steps[i+1][1]-0.95, 2.5, DARK_BLUE)

    ax.set_title('图2  认知生成到物理验证的数据接口流程', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-4_fig2.png')

def pf5_4_fig3():
    """图3 构思—验证—反馈—修正迭代闭环"""
    fig, ax = plt.subplots(figsize=(9, 9))
    ax.set_xlim(0, 9); ax.set_ylim(0, 9); ax.axis('off')

    # 四节点环形
    cx, cy = 4.5, 4.5
    r = 2.5
    nodes = [
        ('构思\n认知层生成\nΠk', cx, cy+r, PURPLE),
        ('验证\n物理层校核\nV(πi)', cx+r, cy, BLUE),
        ('反馈\n失败解释 Ei\n违规项+时段', cx, cy-r, ORANGE),
        ('修正\n调权重/边界\n切换模板', cx-r, cy, GREEN),
    ]

    for text, x, y, color in nodes:
        draw_box(ax, x, y, 2.2, 1.3, text, color, 9)

    # 环形箭头
    draw_arrow(ax, cx+1.0, cy+r-0.3, cx+r-0.5, cy+0.7, DARK_BLUE)
    draw_arrow(ax, cx+r-0.3, cy-0.7, cx+1.0, cy-r+0.3, DARK_BLUE)
    draw_arrow(ax, cx-1.0, cy-r+0.3, cx-r+0.5, cy-0.7, DARK_BLUE)
    draw_arrow(ax, cx-r+0.3, cy+0.7, cx-1.0, cy+r-0.3, DARK_BLUE)

    # 中心标注
    draw_box(ax, cx, cy, 2.0, 1.0, '迭代 k/K_max\nK_max=4', DARK_BLUE, 9)

    ax.set_title('图3  构思—验证—反馈—修正迭代闭环', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-4_fig3.png')

def pf5_4_fig4():
    """图4 发布条件判定与降级托底"""
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.set_xlim(0, 11); ax.set_ylim(0, 6); ax.axis('off')

    draw_box(ax, 2.0, 5.0, 2.0, 0.8, '迭代完成\n第k轮', GRAY, 9)
    draw_arrow(ax, 2.0, 4.55, 2.0, 4.0)

    # 判定1
    draw_box(ax, 2.0, 3.3, 2.5, 1.0, 'V(π*)=1 且\nS(π*)≥0.82?', DARK_BLUE, 9)

    # 通过
    draw_arrow(ax, 3.3, 3.3, 5.0, 3.3)
    ax.text(4.0, 3.7, '是', fontsize=10, color=GREEN, fontweight='bold')
    draw_box(ax, 6.2, 3.3, 2.5, 0.8, '发布最终方案\n+ 可解释报告', GREEN, 9)
    draw_arrow(ax, 7.5, 3.3, 8.8, 3.3)
    draw_box(ax, 9.5, 3.3, 1.2, 0.8, '审计\n日志', TEAL, 9)

    # 不通过
    draw_arrow(ax, 2.0, 2.75, 2.0, 2.2)
    ax.text(2.5, 2.5, '否', fontsize=10, color=RED, fontweight='bold')

    # 判定2
    draw_box(ax, 2.0, 1.5, 2.0, 0.8, 'k < K_max?', ORANGE, 9)

    # k<Kmax → 回到修正
    draw_arrow(ax, 0.95, 1.5, 0.3, 1.5)
    ax.text(0.3, 1.0, '是→返回\n修正', fontsize=8, color=ORANGE)

    # k=Kmax → 降级
    draw_arrow(ax, 3.05, 1.5, 4.5, 1.5)
    ax.text(3.5, 1.9, '否', fontsize=10, color=RED, fontweight='bold')
    draw_box(ax, 6.2, 1.5, 3.0, 0.8, '切换托底方案 π_safe\n+ 提示人工复核', RED, 9)

    ax.set_title('图4  发布条件判定与降级托底', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-4_fig4.png')

# ============================================================
# PF5-5: 知识图谱自动构建与推理
# ============================================================

def pf5_5_fig1():
    """图1 多源语料到知识图谱自动构建"""
    fig, ax = plt.subplots(figsize=(13, 6))
    ax.set_xlim(0, 13); ax.set_ylim(0, 6); ax.axis('off')

    # 语料源
    sources = ['规范标准\n312份', '运维手册\n128份', 'SCADA日志\n220万条', '事故复盘\n640份', '专家案例库']
    for i, s in enumerate(sources):
        draw_box(ax, 1.5, 5.0 - i*0.9, 2.0, 0.6, s, GRAY, 8)
        draw_arrow(ax, 2.55, 5.0 - i*0.9, 3.8, 3.0)

    # NER + 关系抽取
    draw_box(ax, 5.0, 4.0, 2.5, 1.0, 'NER\nBERT+CRF\n命名实体识别', PURPLE, 8)
    draw_box(ax, 5.0, 2.2, 2.5, 1.0, '关系抽取\n依存句法+规则\n模板', ORANGE, 8)
    draw_arrow(ax, 5.0, 3.45, 5.0, 2.75)

    # 三元组
    draw_arrow(ax, 6.3, 3.0, 7.2, 3.0)
    draw_box(ax, 8.5, 3.0, 2.5, 1.5, '三元组\n(h, r, t, τ, c)\n\n58万实体\n214万关系\nP=94%, R=89%', TEAL, 8)

    # 图数据库 + 本体约束
    draw_arrow(ax, 9.8, 3.0, 10.5, 3.0)
    draw_box(ax, 11.5, 3.8, 2.0, 0.8, '知识图谱\nKG=(V,E,A)', BLUE, 9)
    draw_box(ax, 11.5, 2.2, 2.0, 0.8, '本体约束\n校核', GREEN, 9)
    draw_arrow(ax, 11.5, 3.35, 11.5, 2.65)

    ax.text(12.8, 1.5, '不一致→\n人工队列', fontsize=7, color=RED)

    ax.set_title('图1  多源语料到知识图谱自动构建', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-5_fig1.png')

def pf5_5_fig2():
    """图2 实体关系抽取与本体校核详细流程"""
    fig, ax = plt.subplots(figsize=(13, 5))
    ax.set_xlim(0, 13); ax.set_ylim(0, 5); ax.axis('off')

    pipeline = [
        ('原始文本', 0.8, GRAY),
        ('分词', 2.2, '#546E7A'),
        ('BERT\n编码', 3.6, PURPLE),
        ('CRF\n实体标注', 5.2, PURPLE),
        ('依存\n分析', 6.8, ORANGE),
        ('关系\n分类', 8.4, ORANGE),
        ('三元组\n生成', 10.0, TEAL),
    ]

    for text, x, color in pipeline:
        draw_box(ax, x, 3.5, 1.2, 1.0, text, color, 8)

    for i in range(len(pipeline)-1):
        draw_arrow(ax, pipeline[i][1]+0.65, 3.5, pipeline[i+1][1]-0.65, 3.5, DARK_BLUE)

    # 本体约束
    draw_arrow(ax, 10.0, 2.95, 10.0, 2.2)
    constraints = ['类型约束', '基数约束', '互斥约束']
    for i, c in enumerate(constraints):
        draw_box(ax, 10.0 + i*1.3 - 1.3, 1.5, 1.1, 0.6, c, GREEN, 7)

    draw_box(ax, 11.8, 3.5, 1.6, 1.0, '写入KG\n或转人工', BLUE, 8)
    draw_arrow(ax, 10.65, 3.5, 10.95, 3.5)

    # 示例
    ax.text(5.5, 0.5, '示例: "渠池A最低水位为0.5m" → (渠池A, 约束于, 最低水位0.5m, 2025-12-01, 0.96)',
            fontsize=8, ha='center', color='#333333',
            bbox=dict(boxstyle='round', facecolor=LIGHT_BLUE, alpha=0.3))

    ax.set_title('图2  实体关系抽取与本体一致性校核', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-5_fig2.png')

def pf5_5_fig3():
    """图3 规则推理与GNN混合推理架构"""
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.set_xlim(0, 12); ax.set_ylim(0, 7); ax.axis('off')

    # 查询
    draw_box(ax, 1.5, 3.5, 2.0, 0.8, '查询 q', GRAY, 10)

    # 通道1 规则
    ax.add_patch(FancyBboxPatch((3.5, 4.5), 4.5, 2.0, boxstyle="round,pad=0.1",
                                 facecolor=LIGHT_GREEN, edgecolor=GREEN, lw=1.5, alpha=0.3))
    ax.text(5.75, 6.2, '通道1: 规则推理', ha='center', fontsize=10, color=GREEN, fontweight='bold')
    draw_box(ax, 4.5, 5.2, 1.8, 0.8, '规则引擎\n匹配', GREEN, 9)
    draw_box(ax, 7.0, 5.2, 1.5, 0.8, 'Score_rule', GREEN, 9)
    draw_arrow(ax, 5.45, 5.2, 6.2, 5.2)

    # 通道2 GNN
    ax.add_patch(FancyBboxPatch((3.5, 0.5), 4.5, 2.0, boxstyle="round,pad=0.1",
                                 facecolor=LIGHT_PURPLE, edgecolor=PURPLE, lw=1.5, alpha=0.3))
    ax.text(5.75, 2.2, '通道2: R-GCN推理', ha='center', fontsize=10, color=PURPLE, fontweight='bold')
    draw_box(ax, 4.5, 1.2, 1.8, 0.8, 'R-GCN\n4层 d=128', PURPLE, 9)
    draw_box(ax, 7.0, 1.2, 1.5, 0.8, 'Score_gnn', PURPLE, 9)
    draw_arrow(ax, 5.45, 1.2, 6.2, 1.2)

    draw_arrow(ax, 2.55, 3.8, 3.6, 5.2)
    draw_arrow(ax, 2.55, 3.2, 3.6, 1.2)

    # 融合
    draw_arrow(ax, 7.8, 5.2, 9.0, 3.5)
    draw_arrow(ax, 7.8, 1.2, 9.0, 3.5)
    draw_box(ax, 9.8, 3.5, 2.5, 1.5, '自适应融合\nScore =\nbeta_1*rule+beta_2*gnn\n\n规程查询: beta_1=0.7\n关联预测: beta_2=0.7', DARK_BLUE, 8)

    # 输出
    draw_arrow(ax, 11.1, 3.5, 11.5, 3.5)
    ax.text(11.7, 3.5, '→输出', fontsize=10, color=DARK_BLUE, fontweight='bold')

    ax.set_title('图3  规则推理与图神经网络混合推理架构', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-5_fig3.png')

def pf5_5_fig4():
    """图4 图谱动态更新与质量评估闭环"""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.set_xlim(0, 12); ax.set_ylim(0, 5); ax.axis('off')

    nodes = [
        ('新增数据\n规程/日志/处置', 1.5, 3.5, GRAY),
        ('增量抽取\n定时+事件驱动', 4.0, 3.5, PURPLE),
        ('图谱更新\nKG←KG∪ΔT', 6.5, 3.5, TEAL),
        ('质量评估\nM=[P,R,Cons,\nHit@k,Trace]', 9.0, 3.5, ORANGE),
    ]

    for text, x, y, color in nodes:
        draw_box(ax, x, y, 2.2, 1.2, text, color, 8)

    for i in range(len(nodes)-1):
        draw_arrow(ax, nodes[i][1]+1.15, 3.5, nodes[i+1][1]-1.15, 3.5, DARK_BLUE)

    # 达标
    draw_box(ax, 11.0, 3.5, 1.5, 0.8, '达标\n继续运行', GREEN, 8)
    draw_arrow(ax, 10.15, 3.8, 10.2, 3.8)
    ax.text(10.3, 4.2, '是', fontsize=9, color=GREEN)

    # 未达标→再训练→回环
    draw_box(ax, 9.0, 1.5, 2.5, 0.8, '模型再训练\n+规则重整', RED, 8)
    draw_arrow(ax, 9.0, 2.85, 9.0, 1.95, RED)
    ax.text(9.5, 2.4, '否\nCons<0.95\nHit@5<0.85', fontsize=7, color=RED)

    draw_arrow(ax, 7.7, 1.5, 4.0, 2.85, RED)

    ax.set_title('图4  图谱动态更新与质量评估闭环', fontsize=14, fontweight='bold', pad=10)
    save(fig, 'PF5-5_fig4.png')


# ============================================================
# Main
# ============================================================

if __name__ == '__main__':
    print("Generating PF5 patent figures...")

    print("\n[PF5-1] 领域大语言模型构建方法")
    pf5_1_fig1()
    pf5_1_fig2()
    pf5_1_fig3()
    pf5_1_fig4()

    print("\n[PF5-2] 调度方案自动生成与评审")
    pf5_2_fig1()
    pf5_2_fig2()
    pf5_2_fig3()
    pf5_2_fig4()

    print("\n[PF5-3] 多模态异常识别")
    pf5_3_fig1()
    pf5_3_fig2()
    pf5_3_fig3()
    pf5_3_fig4()

    print("\n[PF5-4] 双引擎协同决策")
    pf5_4_fig1()
    pf5_4_fig2()
    pf5_4_fig3()
    pf5_4_fig4()

    print("\n[PF5-5] 知识图谱构建与推理")
    pf5_5_fig1()
    pf5_5_fig2()
    pf5_5_fig3()
    pf5_5_fig4()

    print(f"\nDone! 20 figures saved to {outdir}")
