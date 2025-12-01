# 实验一：matplotlib库应用 - 问题回答

## 一、折线图和散点图在表达数据上各有什么特点？

### 折线图的特点：
1. **趋势展示**：折线图能够清晰地展示数据随时间的变化趋势，特别适合展示时间序列数据。
2. **连续性**：通过连接数据点，折线图强调数据的连续性和变化过程。
3. **对比分析**：多条折线可以方便地对比不同指标（如确诊、死亡、治愈）的变化趋势。
4. **易于识别**：能够快速识别数据的峰值、谷值以及整体走势。
5. **适用场景**：最适合展示时间序列数据、趋势分析和周期性变化。

### 散点图的特点：
1. **离散性**：散点图强调数据的离散性，每个数据点都是独立的。
2. **分布展示**：能够清晰地展示数据的分布情况和数据点的密度。
3. **异常值识别**：更容易识别异常值和离群点。
4. **相关性分析**：适合用于分析两个变量之间的相关关系。
5. **适用场景**：最适合展示数据分布、相关性分析和异常值检测。

### 思考：哪一个图更为有效？
对于按日期的新冠疫情数据，**折线图更为有效**，因为：
- 时间序列数据需要展示趋势变化，折线图能更好地体现数据的连续性和变化趋势
- 可以清晰地看到疫情的发展过程，包括上升期、高峰期和下降期
- 多条折线可以直观地对比确诊、死亡、治愈三个指标的变化关系

---

## 二、饼图有什么特点，在绘制饼图时应注意什么？

### 饼图的特点：
1. **比例展示**：饼图能够直观地展示各部分占整体的比例关系。
2. **视觉冲击**：通过扇形面积的大小，能够快速传达各部分的重要性。
3. **易于理解**：对于普通观众来说，饼图是最容易理解的可视化方式之一。
4. **局限性**：
   - 不适合展示过多类别（建议不超过5-7个）
   - 难以精确比较相似大小的扇形
   - 不适合展示时间序列数据

### 绘制饼图时应注意：
1. **类别数量**：饼图的类别数量不宜过多，建议控制在5-7个以内，过多会导致难以区分。
2. **数据排序**：通常按照数值大小从大到小排列，或者将最重要的部分放在12点钟方向。
3. **标签和百分比**：应该清晰标注每个扇形的名称和百分比，便于读者理解。
4. **颜色选择**：使用对比鲜明的颜色，避免使用过于相似的颜色。
5. **避免3D效果**：3D饼图会扭曲数据比例，应避免使用。
6. **零值处理**：对于值为0或接近0的数据，应该过滤掉或明确标注。
7. **起始角度**：合理设置起始角度（startangle），使重要数据位于显眼位置。
8. **图例位置**：如果标签过长，可以使用图例，但要确保图例清晰易读。

---

## 三、使用matplotlib库绘制的统计图如何实现交互？

matplotlib库本身主要是一个静态绘图库，但可以通过以下方式实现交互：

### 1. **使用matplotlib的交互模式**
```python
import matplotlib.pyplot as plt
plt.ion()  # 开启交互模式
# 绘制图形后，图形会实时更新
plt.ioff()  # 关闭交互模式
```

### 2. **使用matplotlib的交互式后端**
```python
import matplotlib
matplotlib.use('TkAgg')  # 或 'Qt5Agg', 'Qt4Agg' 等
import matplotlib.pyplot as plt
# 使用交互式后端可以缩放、平移图形
```

### 3. **使用mplcursors库**
```python
import mplcursors
cursor = mplcursors.cursor(hover=True)
# 鼠标悬停时显示数据点信息
```

### 4. **使用plotly库（推荐）**
plotly是专门用于交互式可视化的库：
```python
import plotly.graph_objects as go
fig = go.Figure()
fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))
fig.show()  # 生成交互式图表，支持缩放、平移、悬停等
```

### 5. **使用Bokeh库**
Bokeh专门用于创建交互式Web可视化：
```python
from bokeh.plotting import figure, show
p = figure()
p.line(x, y)
show(p)  # 在浏览器中显示交互式图表
```

### 6. **使用Jupyter Notebook的交互功能**
在Jupyter Notebook中，使用`%matplotlib widget`或`%matplotlib notebook`可以启用交互功能：
```python
%matplotlib widget
import matplotlib.pyplot as plt
# 图形可以交互式操作
```

### 7. **自定义交互功能**
使用matplotlib的事件处理机制：
```python
def on_click(event):
    print(f'点击位置: ({event.xdata}, {event.ydata})')

fig, ax = plt.subplots()
fig.canvas.mpl_connect('button_press_event', on_click)
```

