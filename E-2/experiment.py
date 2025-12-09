import json
import pandas as pd  # pyright: ignore[reportMissingImports]
from pyecharts.charts import Graph, WordCloud, Bar, Pie, Line  # pyright: ignore[reportMissingImports]
from pyecharts import options as opts  # pyright: ignore[reportMissingImports]
from pyecharts.globals import ThemeType  # pyright: ignore[reportMissingImports]
import requests  # pyright: ignore[reportMissingModuleSource]
from bs4 import BeautifulSoup  # pyright: ignore[reportMissingModuleSource]
import re

print("=" * 60)
print("实验二：pyecharts库应用")
print("=" * 60)

print("\n【任务1】正在绘制关系图...")

with open('weibo.json', 'r', encoding='utf-8') as f:
    weibo_data = json.load(f)

if isinstance(weibo_data, list) and len(weibo_data) >= 2:
    nodes_data = weibo_data[0]
    links_data = weibo_data[1] if isinstance(weibo_data[1], list) else []
else:
    nodes_data = weibo_data.get('nodes', []) if isinstance(weibo_data, dict) else weibo_data
    links_data = weibo_data.get('links', []) if isinstance(weibo_data, dict) else []

nodes = []
categories = set()
for node in nodes_data:
    if isinstance(node, dict) and 'name' in node:
        name = node.get("name", "")
        if name and name.strip():
            symbol_size = node.get("symbolSize", 5)
            if isinstance(symbol_size, str):
                try:
                    symbol_size = int(symbol_size)
                except:
                    symbol_size = 10
            symbol_size = max(5, min(symbol_size, 50))
            
            node_info = {
                "name": name,
                "symbolSize": symbol_size,
                "value": node.get("value", 1),
                "category": node.get("category", ""),
            }
            nodes.append(node_info)
            if node.get("category"):
                categories.add(node.get("category"))

links = []
if isinstance(links_data, list):
    for link in links_data:
        if isinstance(link, dict) and 'source' in link and 'target' in link:
            links.append({
                "source": link.get("source"),
                "target": link.get("target"),
                "value": link.get("value", 1)
            })

if not links and len(nodes) > 0:
    category_map = {}
    for node in nodes:
        if node.get("category"):
            cat = node["category"]
            if cat not in category_map:
                category_map[cat] = []
            category_map[cat].append(node["name"])
    
    for cat, names in category_map.items():
        if len(names) > 1 and len(names) <= 50:
            if len(names) > 1:
                center = names[0]
                for name in names[1:min(20, len(names))]:
                    links.append({
                        "source": center,
                        "target": name,
                        "value": 1
                    })

print(f"节点数量: {len(nodes)}")
print(f"连接数量: {len(links)}")

if len(nodes) > 500:
    print(f"节点数量较多({len(nodes)})，将限制显示以提高性能...")
    nodes = sorted(nodes, key=lambda x: x.get("value", 1), reverse=True)[:500]
    node_names = {n["name"] for n in nodes}
    links = [l for l in links if l["source"] in node_names and l["target"] in node_names]
    print(f"已限制为 {len(nodes)} 个节点，{len(links)} 个连接")

graph = (
    Graph(init_opts=opts.InitOpts(width="1600px", height="900px", theme=ThemeType.MACARONS))
    .add(
        "",
        nodes,
        links,
        repulsion=8000,
        gravity=0.2,
        layout="force",
        linestyle_opts=opts.LineStyleOpts(curve=0.3, width=0.5, opacity=0.6),
        label_opts=opts.LabelOpts(
            is_show=True,
            position="right",
            font_size=8,
            formatter="{b}"
        ),
        itemstyle_opts=opts.ItemStyleOpts(
            border_width=1,
            border_color="#fff"
        ),
        is_roam=True,
        is_focusnode=True,
        is_draggable=True,
        categories=[{"name": cat} for cat in categories] if categories else None,
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="微博关系图",
            subtitle="节点可拖拽、缩放、平移（鼠标滚轮缩放，拖拽移动）",
            title_textstyle_opts=opts.TextStyleOpts(font_size=18),
            subtitle_textstyle_opts=opts.TextStyleOpts(font_size=12)
        ),
        legend_opts=opts.LegendOpts(is_show=False),
        tooltip_opts=opts.TooltipOpts(is_show=True),
    )
)

graph.render("task1_graph.html")
print("任务1完成，关系图已保存为 task1_graph.html")

print("\n【任务2】正在获取百度热搜并绘制词云图...")

try:
    url = "https://top.baidu.com/board?platform=wise"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    response = requests.get(url, headers=headers, timeout=10)
    response.encoding = 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')
    
    hot_words = []
    selectors = [
        '.c-single-text-ellipsis',
        '.title-text',
        '.content_1YWBm',
        'a[class*="title"]',
        '.item-title',
        '[class*="title"]',
        'div[class*="content"] a',
        '.hot-item-title'
    ]
    
    found = False
    seen_texts = set()
    
    for selector in selectors:
        elements = soup.select(selector)
        if elements:
            for i, elem in enumerate(elements[:30], 1):
                text = elem.get_text(strip=True)
                if text and 2 <= len(text) <= 50 and text not in seen_texts:
                    seen_texts.add(text)
                    weight = 21 - len(hot_words)
                    hot_words.append((text, weight))
                    if len(hot_words) >= 20:
                        break
            if len(hot_words) >= 20:
                found = True
                break
    
    if not found or len(hot_words) < 20:
        scripts = soup.find_all('script')
        for script in scripts:
            if script.string:
                text = script.string
                patterns = [
                    r'"title":"([^"]+)"',
                    r'"keyword":"([^"]+)"',
                    r'"word":"([^"]+)"',
                ]
                for pattern in patterns:
                    matches = re.findall(pattern, text)
                    for match in matches[:20]:
                        if match and 2 <= len(match) <= 50 and match not in seen_texts:
                            seen_texts.add(match)
                            weight = 21 - len(hot_words)
                            hot_words.append((match, weight))
                            if len(hot_words) >= 20:
                                break
                    if len(hot_words) >= 20:
                        found = True
                        break
                if found:
                    break
    
    if not found or len(hot_words) == 0:
        print("警告：无法从网页获取数据，使用示例数据")
        hot_words = [
            ("人工智能", 20), ("科技创新", 19), ("教育改革", 18), ("环境保护", 17),
            ("健康生活", 16), ("数字化转型", 15), ("新能源", 14), ("5G技术", 13),
            ("远程办公", 12), ("在线教育", 11), ("电商发展", 10), ("智慧城市", 9),
            ("医疗健康", 8), ("文化传承", 7), ("乡村振兴", 6), ("绿色发展", 5),
            ("创新创业", 4), ("人才培养", 3), ("国际合作", 2), ("社会公益", 1)
        ]
    
    print(f"获取到 {len(hot_words)} 个热搜词条")
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.MACARONS))
        .add(
            series_name="百度热搜",
            data_pair=hot_words,
            word_size_range=[20, 100],
            textstyle_opts=opts.TextStyleOpts(font_family="Microsoft YaHei"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="百度热搜榜前20词云图",
                title_textstyle_opts=opts.TextStyleOpts(font_size=20)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    
    wordcloud.render("task2_wordcloud.html")
    print("任务2完成，词云图已保存为 task2_wordcloud.html")
    
except Exception as e:
    print(f"获取百度热搜时出错: {e}")
    print("使用示例数据生成词云图")
    hot_words = [
        ("人工智能", 20), ("科技创新", 19), ("教育改革", 18), ("环境保护", 17),
        ("健康生活", 16), ("数字化转型", 15), ("新能源", 14), ("5G技术", 13),
        ("远程办公", 12), ("在线教育", 11), ("电商发展", 10), ("智慧城市", 9),
        ("医疗健康", 8), ("文化传承", 7), ("乡村振兴", 6), ("绿色发展", 5),
        ("创新创业", 4), ("人才培养", 3), ("国际合作", 2), ("社会公益", 1)
    ]
    
    wordcloud = (
        WordCloud(init_opts=opts.InitOpts(width="1200px", height="800px", theme=ThemeType.MACARONS))
        .add(
            series_name="百度热搜",
            data_pair=hot_words,
            word_size_range=[20, 100],
            textstyle_opts=opts.TextStyleOpts(font_family="Microsoft YaHei"),
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title="百度热搜榜前20词云图（示例数据）",
                title_textstyle_opts=opts.TextStyleOpts(font_size=20)
            ),
            tooltip_opts=opts.TooltipOpts(is_show=True),
        )
    )
    
    wordcloud.render("task2_wordcloud.html")
    print("任务2完成，词云图已保存为 task2_wordcloud.html")

print("\n【任务3】正在处理学生数据并绘制可视化图表...")

try:
    df = pd.read_excel('student.xls')
    print(f"成功读取学生数据，共 {len(df)} 条记录")
    print(f"数据列: {list(df.columns)}")
except Exception as e:
    print(f"读取Excel文件出错: {e}")
    try:
        df = pd.read_excel('student.xls', header=0)
    except:
        print("无法读取文件，请检查文件路径和格式")
        exit(1)

name_col = None
gender_col = None
english_col = None
math_analysis_col = None
linear_algebra_col = None
analytic_geometry_col = None
total_col = None
for col in df.columns:
    col_lower = str(col).lower()
    if '姓名' in str(col) or 'name' in col_lower:
        name_col = col
    elif '性别' in str(col) or 'gender' in col_lower or 'sex' in col_lower:
        gender_col = col
    elif '英语' in str(col) or 'english' in col_lower or 'eng' in col_lower:
        english_col = col
    elif '数分' in str(col) or '数学分析' in str(col) or 'math' in col_lower:
        math_analysis_col = col
    elif '高代' in str(col) or '线性代数' in str(col) or 'linear' in col_lower:
        linear_algebra_col = col
    elif '解几' in str(col) or '解析几何' in str(col) or 'analytic' in col_lower:
        analytic_geometry_col = col
    elif '总分' in str(col) or 'total' in col_lower or 'sum' in col_lower:
        total_col = col

if total_col is None:
    score_cols = [english_col, math_analysis_col, linear_algebra_col, analytic_geometry_col]
    score_cols = [col for col in score_cols if col is not None]
    if score_cols:
        df['总分'] = df[score_cols].sum(axis=1)
        total_col = '总分'
        print("已自动计算总分")

print("\n任务3.1：绘制总分条形图...")
students = df[name_col].tolist() if name_col else [f"学生{i+1}" for i in range(len(df))]
totals = df[total_col].tolist()

bar1 = (
    Bar(init_opts=opts.InitOpts(width="1600px", height="600px", theme=ThemeType.MACARONS))
    .add_xaxis(students)
    .add_yaxis("总分", totals, color="#5470C6")
    .set_global_opts(
        title_opts=opts.TitleOpts(title="所有学生总分条形图", subtitle="按学生姓名排序"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-45)),
        yaxis_opts=opts.AxisOpts(name="分数"),
        datazoom_opts=[opts.DataZoomOpts(type_="slider", range_start=0, range_end=100)],
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(is_show=True, position="top"),
    )
)

bar1.render("task3_1_total_bar.html")
print("任务3.1完成，条形图已保存为 task3_1_total_bar.html")

print("\n任务3.2：绘制前3名分数构成饼图...")
top3 = df.nlargest(3, total_col)

pie_charts = []
for idx, row in top3.iterrows():
    student_name = row[name_col] if name_col else f"学生{idx+1}"
    total_score = row[total_col]
    
    pie_data = []
    if english_col and pd.notna(row[english_col]):
        pie_data.append(("英语", row[english_col]))
    if math_analysis_col and pd.notna(row[math_analysis_col]):
        pie_data.append(("数分", row[math_analysis_col]))
    if linear_algebra_col and pd.notna(row[linear_algebra_col]):
        pie_data.append(("高代", row[linear_algebra_col]))
    if analytic_geometry_col and pd.notna(row[analytic_geometry_col]):
        pie_data.append(("解几", row[analytic_geometry_col]))
    
    title_text = f"{student_name}\n总分: {total_score}"
    if len(title_text) > 20:
        title_text = f"{student_name[:15]}...\n总分: {total_score}"
    
    pie = (
        Pie(init_opts=opts.InitOpts(width="450px", height="500px", theme=ThemeType.MACARONS))
        .add(
            series_name="",
            data_pair=pie_data,
            radius=["30%", "70%"],
            center=["50%", "55%"],
        )
        .set_global_opts(
            title_opts=opts.TitleOpts(
                title=title_text,
                pos_left="center",
                pos_top="5%",
                title_textstyle_opts=opts.TextStyleOpts(font_size=12, font_weight="bold"),
            ),
            legend_opts=opts.LegendOpts(
                orient="vertical",
                pos_left="5%",
                pos_top="15%",
                item_width=15,
                item_height=12,
                textstyle_opts=opts.TextStyleOpts(font_size=10)
            ),
        )
        .set_series_opts(
            label_opts=opts.LabelOpts(
                formatter="{b}: {c}分\n({d}%)",
                font_size=9
            ),
        )
    )
    pie_charts.append(pie)

from pyecharts.charts import Grid  # pyright: ignore[reportMissingImports]

grid = Grid(init_opts=opts.InitOpts(width="1600px", height="600px", theme=ThemeType.MACARONS))
for i, pie in enumerate(pie_charts):
    grid.add(
        pie,
        grid_opts=opts.GridOpts(
            pos_left=f"{5 + i*30}%",
            pos_top="5%",
            width="28%",
            height="90%"
        )
    )

grid.render("task3_2_top3_pie.html")
print("任务3.2完成，饼图已保存为 task3_2_top3_pie.html")

print("\n任务3.3：绘制成绩分布折线图...")

def get_score_distribution(scores, bin_size=10):
    max_score = int(scores.max())
    min_score = int(scores.min())
    bins = list(range(min_score - (min_score % bin_size), max_score + bin_size, bin_size))
    if bins[-1] < max_score:
        bins.append(bins[-1] + bin_size)
    
    counts = []
    labels = []
    for i in range(len(bins) - 1):
        count = len(scores[(scores >= bins[i]) & (scores < bins[i+1])])
        counts.append(count)
        labels.append(f"{bins[i]}-{bins[i+1]}")
    
    return labels, counts

courses = []
if english_col:
    labels, counts = get_score_distribution(df[english_col].dropna())
    courses.append(("英语", labels, counts))
if math_analysis_col:
    labels, counts = get_score_distribution(df[math_analysis_col].dropna())
    courses.append(("数分", labels, counts))
if linear_algebra_col:
    labels, counts = get_score_distribution(df[linear_algebra_col].dropna())
    courses.append(("高代", labels, counts))
if analytic_geometry_col:
    labels, counts = get_score_distribution(df[analytic_geometry_col].dropna())
    courses.append(("解几", labels, counts))

line = (
    Line(init_opts=opts.InitOpts(width="1200px", height="600px", theme=ThemeType.MACARONS))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="四门课程成绩分布图", subtitle="按每10分统计人数"),
        xaxis_opts=opts.AxisOpts(name="分数段"),
        yaxis_opts=opts.AxisOpts(name="人数"),
        legend_opts=opts.LegendOpts(pos_top="10%"),
    )
    )

if courses:
    x_labels = courses[0][1]
    line.add_xaxis(x_labels)
    
    for course_name, labels, counts in courses:
        if len(counts) == len(x_labels):
            line.add_yaxis(
                course_name,
                counts,
                is_smooth=True,
                symbol="circle",
                symbol_size=8,
                label_opts=opts.LabelOpts(is_show=True),
            )

line.render("task3_3_score_distribution.html")
print("任务3.3完成，折线图已保存为 task3_3_score_distribution.html")

print("\n任务3.4：绘制男女各科平均成绩对比图...")

if gender_col:
    score_cols = [col for col in [english_col, math_analysis_col, linear_algebra_col, analytic_geometry_col] if col is not None]
    
    if score_cols:
        gender_avg = df.groupby(gender_col)[score_cols].mean().round(2)
        
        categories = []
        male_scores = []
        female_scores = []
        
        gender_labels = list(gender_avg.index)
        male_label = None
        female_label = None
        
        for label in gender_labels:
            label_str = str(label).strip()
            if '男' in label_str or label_str.upper() in ['M', 'MALE', '男']:
                male_label = label
            elif '女' in label_str or label_str.upper() in ['F', 'FEMALE', '女']:
                female_label = label
        
        if not male_label and len(gender_labels) > 0:
            male_label = gender_labels[0]
        if not female_label and len(gender_labels) > 1:
            female_label = gender_labels[1]
        
        course_names = {
            english_col: "英语",
            math_analysis_col: "数分",
            linear_algebra_col: "高代",
            analytic_geometry_col: "解几"
        }
        
        for col in score_cols:
            if col in course_names:
                categories.append(course_names[col])
                if male_label:
                    male_scores.append(float(gender_avg.loc[male_label, col]) if male_label in gender_avg.index else 0)
                else:
                    male_scores.append(0)
                
                if female_label:
                    female_scores.append(float(gender_avg.loc[female_label, col]) if female_label in gender_avg.index else 0)
                else:
                    female_scores.append(0)
        
        if categories:
            bar2 = (
                Bar(init_opts=opts.InitOpts(width="1000px", height="600px", theme=ThemeType.MACARONS))
                .add_xaxis(categories)
                .add_yaxis("男生平均分" if male_label else "第一组", male_scores, color="#5470C6")
                .add_yaxis("女生平均分" if female_label else "第二组", female_scores, color="#EE6666")
                .set_global_opts(
                    title_opts=opts.TitleOpts(title="男生和女生各科平均成绩对比"),
                    yaxis_opts=opts.AxisOpts(name="平均分"),
                    legend_opts=opts.LegendOpts(pos_top="10%"),
                )
                .set_series_opts(
                    label_opts=opts.LabelOpts(is_show=True, position="top"),
                )
            )
            
            bar2.render("task3_4_gender_comparison.html")
            print("任务3.4完成，对比图已保存为 task3_4_gender_comparison.html")
        else:
            print("警告：无法准备对比数据，跳过任务3.4")
    else:
        print("警告：未找到成绩列，跳过任务3.4")
else:
    print("警告：未找到性别列，跳过任务3.4")

print("\n" + "=" * 60)
print("所有任务完成！")
print("=" * 60)
print("\n生成的HTML文件：")
print("  - task1_graph.html (关系图)")
print("  - task2_wordcloud.html (词云图)")
print("  - task3_1_total_bar.html (总分条形图)")
print("  - task3_2_top3_pie.html (前3名饼图)")
print("  - task3_3_score_distribution.html (成绩分布折线图)")
print("  - task3_4_gender_comparison.html (男女成绩对比图)")

