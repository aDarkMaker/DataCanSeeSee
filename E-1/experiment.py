import pandas as pd  # pyright: ignore[reportMissingImports]
import matplotlib.pyplot as plt  # pyright: ignore[reportMissingImports]
import numpy as np  # pyright: ignore[reportMissingImports]
from matplotlib import font_manager  # pyright: ignore[reportMissingImports]

plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

excel_file = './E-1/covid19_data.xls'

data_history = pd.read_excel(excel_file, sheet_name='data_history')
data_world = pd.read_excel(excel_file, sheet_name='data_world')
current_prov = pd.read_excel(excel_file, sheet_name='current_prov')

print("数据读取成功！")
print(f"data_history 形状: {data_history.shape}")
print(f"data_world 形状: {data_world.shape}")
print(f"current_prov 形状: {current_prov.shape}")

# ==================== 任务1：折线图和散点图 ====================
print("\n正在绘制任务1：折线图和散点图...")

# 准备数据
dates = data_history['date'] if 'date' in data_history.columns else data_history.iloc[:, 0]
confirm = data_history['confirm'] if 'confirm' in data_history.columns else data_history.iloc[:, 1]
dead = data_history['dead'] if 'dead' in data_history.columns else data_history.iloc[:, 2]
heal = data_history['heal'] if 'heal' in data_history.columns else data_history.iloc[:, 3]

# 如果日期是字符串，转换为索引
if dates.dtype == 'object':
    x_values = range(len(dates))
    x_labels = dates
else:
    x_values = dates
    x_labels = dates

# 创建折线图和散点图的子图
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))

# 折线图
ax1.plot(x_values, confirm, marker='o', linestyle='-', linewidth=2, 
         color='#FF6B6B', label='确诊(confirm)', markersize=4)
ax1.plot(x_values, dead, marker='s', linestyle='-', linewidth=2, 
         color='#4ECDC4', label='死亡(dead)', markersize=4)
ax1.plot(x_values, heal, marker='^', linestyle='-', linewidth=2, 
         color='#95E1D3', label='治愈(heal)', markersize=4)
ax1.set_xlabel('日期', fontsize=12)
ax1.set_ylabel('人数', fontsize=12)
ax1.set_title('新冠疫情数据 - 折线图', fontsize=14, fontweight='bold')
ax1.legend(loc='best', fontsize=10)
ax1.grid(True, alpha=0.3, linestyle='--')
# 设置x轴刻度
if len(x_labels) > 20:
    step = len(x_labels) // 10
    ax1.set_xticks(x_values[::step])
    ax1.set_xticklabels(x_labels[::step], rotation=45, ha='right')
else:
    ax1.set_xticks(x_values)
    ax1.set_xticklabels(x_labels, rotation=45, ha='right')
ax1.tick_params(axis='y', labelsize=9)

# 散点图
ax2.scatter(x_values, confirm, s=50, alpha=0.6, color='#FF6B6B', 
           marker='o', label='确诊(confirm)', edgecolors='darkred', linewidths=0.5)
ax2.scatter(x_values, dead, s=50, alpha=0.6, color='#4ECDC4', 
           marker='s', label='死亡(dead)', edgecolors='darkcyan', linewidths=0.5)
ax2.scatter(x_values, heal, s=50, alpha=0.6, color='#95E1D3', 
           marker='^', label='治愈(heal)', edgecolors='darkgreen', linewidths=0.5)
ax2.set_xlabel('日期', fontsize=12)
ax2.set_ylabel('人数', fontsize=12)
ax2.set_title('新冠疫情数据 - 散点图', fontsize=14, fontweight='bold')
ax2.legend(loc='best', fontsize=10)
ax2.grid(True, alpha=0.3, linestyle='--')
# 设置x轴刻度
if len(x_labels) > 20:
    step = len(x_labels) // 10
    ax2.set_xticks(x_values[::step])
    ax2.set_xticklabels(x_labels[::step], rotation=45, ha='right')
else:
    ax2.set_xticks(x_values)
    ax2.set_xticklabels(x_labels, rotation=45, ha='right')
ax2.tick_params(axis='y', labelsize=9)

plt.tight_layout()
plt.savefig('task1_line_scatter.png', dpi=300, bbox_inches='tight')
print("任务1完成，图片已保存为 task1_line_scatter.png")
plt.close()

# ==================== 任务2：饼图 ====================
print("\n正在绘制任务2：饼图...")

# 获取确诊人数最多的前4个国家
top4_world = data_world.nlargest(4, 'confirm' if 'confirm' in data_world.columns else data_world.columns[1])

# 准备饼图数据
countries = top4_world.iloc[:, 0] if top4_world.columns[0] != 'confirm' else top4_world.index
confirm_data = top4_world['confirm'] if 'confirm' in top4_world.columns else top4_world.iloc[:, 1]
dead_data = top4_world['dead'] if 'dead' in top4_world.columns else top4_world.iloc[:, 2]
heal_data = top4_world['heal'] if 'heal' in top4_world.columns else top4_world.iloc[:, 3]
suspect_data = top4_world['suspect'] if 'suspect' in top4_world.columns else top4_world.iloc[:, 4]

# 创建4个子图，每个国家一个饼图
fig2, axes = plt.subplots(2, 2, figsize=(14, 12))
axes = axes.flatten()

colors = ['#FF6B6B', '#4ECDC4', '#95E1D3', '#FFE66D']
labels = ['确诊(confirm)', '死亡(dead)', '治愈(heal)', '疑似(suspect)']

for i, country in enumerate(countries):
    values = [confirm_data.iloc[i], dead_data.iloc[i], heal_data.iloc[i], suspect_data.iloc[i]]
    # 过滤掉0值
    non_zero_values = [v for v in values if v > 0]
    non_zero_labels = [labels[j] for j, v in enumerate(values) if v > 0]
    non_zero_colors = [colors[j] for j, v in enumerate(values) if v > 0]
    
    axes[i].pie(non_zero_values, labels=non_zero_labels, colors=non_zero_colors, 
                autopct='%1.1f%%', startangle=90, textprops={'fontsize': 9})
    axes[i].set_title(f'{country}\n(确诊: {confirm_data.iloc[i]:,})', 
                     fontsize=12, fontweight='bold')

plt.suptitle('前4个国家新冠疫情数据分布饼图', fontsize=16, fontweight='bold', y=0.98)
plt.tight_layout()
plt.savefig('task2_pie_chart.png', dpi=300, bbox_inches='tight')
print("任务2完成，图片已保存为 task2_pie_chart.png")
plt.close()

# ==================== 任务3：直方图和条形图 ====================
print("\n正在绘制任务3：直方图和条形图...")

# 准备数据
provinces = current_prov.iloc[:, 0] if current_prov.columns[0] != 'confirm' else current_prov.index
confirm_prov = current_prov['confirm'] if 'confirm' in current_prov.columns else current_prov.iloc[:, 1]
dead_prov = current_prov['dead'] if 'dead' in current_prov.columns else current_prov.iloc[:, 2]
heal_prov = current_prov['heal'] if 'heal' in current_prov.columns else current_prov.iloc[:, 3]

# 创建直方图和条形图的子图
fig3, axes = plt.subplots(2, 2, figsize=(16, 12))

# 直方图 - 确诊人数分布
axes[0, 0].hist(confirm_prov, bins=15, color='#FF6B6B', alpha=0.7, edgecolor='black', linewidth=1)
axes[0, 0].set_xlabel('确诊人数', fontsize=11)
axes[0, 0].set_ylabel('省份数量', fontsize=11)
axes[0, 0].set_title('各省确诊人数分布 - 直方图', fontsize=12, fontweight='bold')
axes[0, 0].grid(True, alpha=0.3, axis='y', linestyle='--')

# 直方图 - 死亡人数分布
axes[0, 1].hist(dead_prov, bins=15, color='#4ECDC4', alpha=0.7, edgecolor='black', linewidth=1)
axes[0, 1].set_xlabel('死亡人数', fontsize=11)
axes[0, 1].set_ylabel('省份数量', fontsize=11)
axes[0, 1].set_title('各省死亡人数分布 - 直方图', fontsize=12, fontweight='bold')
axes[0, 1].grid(True, alpha=0.3, axis='y', linestyle='--')

# 条形图 - 堆叠条形图（显示前15个省份）
top_n = min(15, len(provinces))
x_pos = np.arange(top_n)
width = 0.6

axes[1, 0].bar(x_pos, confirm_prov[:top_n], width, label='确诊(confirm)', 
               color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 0].bar(x_pos, dead_prov[:top_n], width, bottom=confirm_prov[:top_n], 
               label='死亡(dead)', color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 0].bar(x_pos, heal_prov[:top_n], width, 
               bottom=confirm_prov[:top_n] + dead_prov[:top_n], 
               label='治愈(heal)', color='#95E1D3', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 0].set_xlabel('省份', fontsize=11)
axes[1, 0].set_ylabel('人数', fontsize=11)
axes[1, 0].set_title(f'前{top_n}个省份新冠疫情数据 - 堆叠条形图', fontsize=12, fontweight='bold')
axes[1, 0].set_xticks(x_pos)
axes[1, 0].set_xticklabels(provinces[:top_n], rotation=45, ha='right', fontsize=8)
axes[1, 0].legend(loc='best', fontsize=9)
axes[1, 0].grid(True, alpha=0.3, axis='y', linestyle='--')

# 条形图 - 分组条形图（显示前15个省份）
x_pos = np.arange(top_n)
width = 0.25

axes[1, 1].bar(x_pos - width, confirm_prov[:top_n], width, label='确诊(confirm)', 
               color='#FF6B6B', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 1].bar(x_pos, dead_prov[:top_n], width, label='死亡(dead)', 
               color='#4ECDC4', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 1].bar(x_pos + width, heal_prov[:top_n], width, label='治愈(heal)', 
               color='#95E1D3', alpha=0.8, edgecolor='black', linewidth=0.5)
axes[1, 1].set_xlabel('省份', fontsize=11)
axes[1, 1].set_ylabel('人数', fontsize=11)
axes[1, 1].set_title(f'前{top_n}个省份新冠疫情数据 - 分组条形图', fontsize=12, fontweight='bold')
axes[1, 1].set_xticks(x_pos)
axes[1, 1].set_xticklabels(provinces[:top_n], rotation=45, ha='right', fontsize=8)
axes[1, 1].legend(loc='best', fontsize=9)
axes[1, 1].grid(True, alpha=0.3, axis='y', linestyle='--')

plt.tight_layout()
plt.savefig('task3_histogram_bar.png', dpi=300, bbox_inches='tight')
print("任务3完成，图片已保存为 task3_histogram_bar.png")
plt.close()

print("\n所有任务完成！")
print("生成的图片文件：")
print("  - task1_line_scatter.png (折线图和散点图)")
print("  - task2_pie_chart.png (饼图)")
print("  - task3_histogram_bar.png (直方图和条形图)")

