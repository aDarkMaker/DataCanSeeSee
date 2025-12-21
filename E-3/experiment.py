# -*- coding: utf-8 -*-
"""
世界杯数据可视化实验
数据集：世界杯数据集（1930-2018）
"""

import pandas as pd
import numpy as np
from pyecharts.charts import Line, Bar, Pie, Scatter
from pyecharts import options as opts
from pyecharts.globals import ThemeType
from collections import Counter
import os

# 读取数据
print("正在读取数据...")
summary_df = pd.read_csv('世界杯数据集/WorldCupsSummary.csv')
matches_df = pd.read_csv('世界杯数据集/WorldCupMatches.csv')

print(f"汇总数据：{len(summary_df)}条记录")
print(f"比赛数据：{len(matches_df)}条记录")

# ==================== 数据预处理 ====================
print("\n开始数据预处理...")

# 处理缺失值
summary_df = summary_df.dropna()
matches_df = matches_df.dropna(subset=['Home Team Goals', 'Away Team Goals'])

# 计算场均进球数
summary_df['AvgGoalsPerMatch'] = summary_df['GoalsScored'] / summary_df['MatchesPlayed']

# 统计各队进入前四名的次数
teams_top4 = []
for col in ['Winner', 'Second', 'Third', 'Fourth']:
    teams_top4.extend(summary_df[col].tolist())
team_top4_count = Counter(teams_top4)

# 统计各队获得冠军次数
champions = summary_df['Winner'].tolist()
champion_count = Counter(champions)

# 统计各洲举办次数
host_continent_count = summary_df['HostContinent'].value_counts().to_dict()

# 统计各洲获得冠军次数
winner_continent_count = summary_df['WinnerContinent'].value_counts().to_dict()

print("数据预处理完成！\n")

# ==================== 通用样式配置 ====================
# 现代配色方案
COLORS = {
    'primary': '#667eea',
    'secondary': '#764ba2',
    'success': '#10b981',
    'warning': '#f59e0b',
    'danger': '#ef4444',
    'info': '#3b82f6',
    'purple': '#8b5cf6',
    'pink': '#ec4899',
    'teal': '#14b8a6',
    'orange': '#f97316'
}

# 渐变配色
GRADIENTS = {
    'blue_purple': {
        "type": "linear",
        "x": 0, "y": 0, "x2": 0, "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "#667eea"},
            {"offset": 1, "color": "#764ba2"}
        ]
    },
    'green_teal': {
        "type": "linear",
        "x": 0, "y": 0, "x2": 0, "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "#10b981"},
            {"offset": 1, "color": "#14b8a6"}
        ]
    },
    'orange_red': {
        "type": "linear",
        "x": 0, "y": 0, "x2": 0, "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "#f97316"},
            {"offset": 1, "color": "#ef4444"}
        ]
    },
    'purple_pink': {
        "type": "linear",
        "x": 0, "y": 0, "x2": 0, "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "#8b5cf6"},
            {"offset": 1, "color": "#ec4899"}
        ]
    },
    'yellow_orange': {
        "type": "linear",
        "x": 0, "y": 0, "x2": 0, "y2": 1,
        "colorStops": [
            {"offset": 0, "color": "#fbbf24"},
            {"offset": 1, "color": "#f97316"}
        ]
    }
}

# 通用标题样式
def get_title_opts(title, subtitle=""):
    return opts.TitleOpts(
        title=title,
        subtitle=subtitle,
        title_textstyle_opts=opts.TextStyleOpts(
            font_size=28,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        ),
        subtitle_textstyle_opts=opts.TextStyleOpts(
            font_size=14,
            color="#64748b",
            font_family="Arial, sans-serif"
        ),
        pos_left="center",
        pos_top="3%"
    )

# 通用坐标轴样式
def get_axis_opts(name, name_gap=30, rotate=0, type_="category", interval="auto"):
    return opts.AxisOpts(
        type_=type_,
        name=name,
        name_location="middle",
        name_gap=name_gap,
        name_textstyle_opts=opts.TextStyleOpts(
            font_size=15,
            font_weight="bold",
            color="#475569",
            font_family="Arial, sans-serif"
        ),
        axislabel_opts=opts.LabelOpts(
            font_size=12,
            color="#64748b",
            rotate=rotate,
            font_family="Arial, sans-serif",
            interval=interval  # 控制标签显示间隔，0表示显示所有，'auto'表示自动，数字表示每隔N个显示
        ),
        axisline_opts=opts.AxisLineOpts(
            linestyle_opts=opts.LineStyleOpts(color="#cbd5e1", width=2)
        ),
        splitline_opts=opts.SplitLineOpts(
            is_show=True,
            linestyle_opts=opts.LineStyleOpts(
                type_="dashed",
                opacity=0.2,
                color="#cbd5e1"
            )
        )
    )

# 通用提示框样式
def get_tooltip_opts(trigger="axis", formatter=None):
    return opts.TooltipOpts(
        trigger=trigger,
        axis_pointer_type="cross" if trigger == "axis" else "line",
        formatter=formatter,
        background_color="rgba(30, 41, 59, 0.95)",
        border_color="#475569",
        border_width=1,
        textstyle_opts=opts.TextStyleOpts(
            color="#f1f5f9",
            font_size=13,
            font_family="Arial, sans-serif"
        ),
        padding=[12, 16]
    )

# ==================== 视图1：历届世界杯总进球数趋势 ====================
print("生成视图1：历届世界杯总进球数趋势...")
# 将年份转换为字符串，确保category类型正常工作
x_data = [str(year) for year in summary_df['Year'].astype(int).tolist()]
y_data = summary_df['GoalsScored'].tolist()
line1 = (
    Line(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart1'
    ))
    .add_xaxis(x_data)
    .add_yaxis(
        "总进球数",
        y_data,
        is_smooth=True,
        symbol="circle",
        symbol_size=10,
        linestyle_opts=opts.LineStyleOpts(width=4, color=COLORS['primary']),
        itemstyle_opts=opts.ItemStyleOpts(
            color=COLORS['primary'],
            border_width=3,
            border_color="#ffffff"
        ),
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(
            opacity=0.2,
            color=COLORS['primary']
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值", symbol_size=70),
                opts.MarkPointItem(type_="min", name="最小值", symbol_size=70)
            ],
            label_opts=opts.LabelOpts(
                color="#ffffff",
                font_size=13,
                font_weight="bold"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS['danger'])
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")],
            label_opts=opts.LabelOpts(
                font_size=13,
                color="#64748b",
                font_weight="bold"
            ),
            linestyle_opts=opts.LineStyleOpts(
                type_="dashed",
                width=2,
                color=COLORS['warning']
            )
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("历届世界杯总进球数趋势", "1930-2018年共21届世界杯进球数据"),
        xaxis_opts=get_axis_opts("年份", 35, type_="category", interval=2),  # interval=2表示每隔2个年份显示一次
        yaxis_opts=get_axis_opts("进球数", 60),
        tooltip_opts=get_tooltip_opts(),
        legend_opts=opts.LegendOpts(
            pos_left="8%",
            pos_top="12%",
            textstyle_opts=opts.TextStyleOpts(
                font_size=14,
                color="#475569",
                font_family="Arial, sans-serif"
            ),
            item_width=25,
            item_height=14
        )
    )
)
line1.render("view1_goals_trend.html")
print("视图1已保存：view1_goals_trend.html")

# ==================== 视图2：各洲举办世界杯次数 ====================
print("生成视图2：各洲举办世界杯次数...")
pie_data = [list(z) for z in zip(host_continent_count.keys(), host_continent_count.values())]
pie_colors = [COLORS['primary'], COLORS['success'], COLORS['warning'], COLORS['info'], COLORS['purple']]

pie1 = (
    Pie(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart2'
    ))
    .add(
        "",
        pie_data,
        radius=["30%", "65%"],
        center=["50%", "55%"],
        rosetype="radius",
        itemstyle_opts=opts.ItemStyleOpts(
            border_width=3,
            border_color="#ffffff"
        )
    )
    .set_colors(pie_colors)
    .set_global_opts(
        title_opts=get_title_opts("各洲举办世界杯次数分布", "欧洲和美洲是主要举办地"),
        legend_opts=opts.LegendOpts(
            orient="vertical",
            pos_left="78%",
            pos_top="25%",
            textstyle_opts=opts.TextStyleOpts(
                font_size=14,
                color="#475569",
                font_family="Arial, sans-serif"
            ),
            item_width=25,
            item_height=16,
            item_gap=12
        ),
        tooltip_opts=get_tooltip_opts(trigger="item", formatter="{b}: {c}次 ({d}%)")
    )
    .set_series_opts(
        label_opts=opts.LabelOpts(
            formatter="{b}\n{c}次\n({d}%)",
            font_size=14,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        )
    )
)
pie1.render("view2_host_continent.html")
print("视图2已保存：view2_host_continent.html")

# ==================== 视图3：各洲获得冠军次数 ====================
print("生成视图3：各洲获得冠军次数...")
bar1 = (
    Bar(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart3'
    ))
    .add_xaxis(list(winner_continent_count.keys()))
    .add_yaxis(
        "冠军次数",
        list(winner_continent_count.values()),
        itemstyle_opts=opts.ItemStyleOpts(
            color=GRADIENTS['green_teal'],
            border_radius=[10, 10, 0, 0]
        ),
        bar_width="55%",
        label_opts=opts.LabelOpts(
            is_show=True,
            position="top",
            font_size=15,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("各洲获得世界杯冠军次数", "欧洲和南美洲占据绝对优势"),
        xaxis_opts=get_axis_opts("大洲", 35),
        yaxis_opts=get_axis_opts("冠军次数", 60),
        tooltip_opts=get_tooltip_opts(        )
    )
)
bar1.render("view3_winner_continent.html")
print("视图3已保存：view3_winner_continent.html")

# ==================== 视图4：历届世界杯观众人数变化 ====================
print("生成视图4：历届世界杯观众人数变化...")
# 将年份转换为字符串，确保category类型正常工作
x_data2 = [str(year) for year in summary_df['Year'].astype(int).tolist()]
y_data2 = (summary_df['Attendance'] / 10000).tolist()
line2 = (
    Line(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart4'
    ))
    .add_xaxis(x_data2)
    .add_yaxis(
        "观众人数（万人）",
        y_data2,
        is_smooth=True,
        symbol="circle",
        symbol_size=10,
        linestyle_opts=opts.LineStyleOpts(width=4, color=COLORS['success']),
        itemstyle_opts=opts.ItemStyleOpts(
            color=COLORS['success'],
            border_width=3,
            border_color="#ffffff"
        ),
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(
            opacity=0.2,
            color=COLORS['success']
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")],
            label_opts=opts.LabelOpts(
                font_size=13,
                color="#64748b",
                font_weight="bold"
            ),
            linestyle_opts=opts.LineStyleOpts(
                type_="dashed",
                width=2,
                color=COLORS['warning']
            )
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[opts.MarkPointItem(type_="max", name="最大值", symbol_size=70)],
            label_opts=opts.LabelOpts(
                color="#ffffff",
                font_size=13,
                font_weight="bold"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS['danger'])
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("历届世界杯观众人数变化", "观众人数持续增长，影响力不断扩大"),
        xaxis_opts=get_axis_opts("年份", 35, type_="category", interval=2),  # interval=2表示每隔2个年份显示一次
        yaxis_opts=get_axis_opts("观众人数（万人）", 70),
        tooltip_opts=get_tooltip_opts(formatter="{b}年<br/>{a}: {c}万人"),
        legend_opts=opts.LegendOpts(
            pos_left="8%",
            pos_top="12%",
            textstyle_opts=opts.TextStyleOpts(
                font_size=14,
                color="#475569",
                font_family="Arial, sans-serif"
            )
        )
    )
)
line2.render("view4_attendance_trend.html")
print("视图4已保存：view4_attendance_trend.html")

# ==================== 视图5：参赛队伍数量变化 ====================
print("生成视图5：参赛队伍数量变化...")
bar2 = (
    Bar(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart5'
    ))
    .add_xaxis(summary_df['Year'].astype(int).tolist())
    .add_yaxis(
        "参赛队伍数",
        summary_df['QualifiedTeams'].tolist(),
        itemstyle_opts=opts.ItemStyleOpts(
            color=GRADIENTS['yellow_orange'],
            border_radius=[10, 10, 0, 0]
        ),
        bar_width="35%",
        label_opts=opts.LabelOpts(
            is_show=True,
            position="top",
            font_size=12,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("历届世界杯参赛队伍数量变化", "从13支到32支，国际化程度不断提升"),
        xaxis_opts=get_axis_opts("年份", 35, rotate=45),
        yaxis_opts=get_axis_opts("队伍数", 50),
        tooltip_opts=get_tooltip_opts(),
        datazoom_opts=opts.DataZoomOpts(
            type_="slider",
            range_start=0,
            range_end=100
        )
    )
)
bar2.render("view5_teams_count.html")
print("视图5已保存：view5_teams_count.html")

# ==================== 视图6：各队进入前四名次数（Top 10） ====================
print("生成视图6：各队进入前四名次数（Top 10）...")
top10_teams = dict(sorted(team_top4_count.items(), key=lambda x: x[1], reverse=True)[:10])
bar3 = (
    Bar(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart6'
    ))
    .add_xaxis(list(top10_teams.keys()))
    .add_yaxis(
        "进入前四名次数",
        list(top10_teams.values()),
        itemstyle_opts=opts.ItemStyleOpts(
            color=GRADIENTS['purple_pink'],
            border_radius=[0, 10, 10, 0]
        ),
        bar_width="65%",
        label_opts=opts.LabelOpts(
            is_show=True,
            position="right",
            font_size=14,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        )
    )
    .reversal_axis()
    .set_global_opts(
        title_opts=get_title_opts("进入前四名次数最多的10支队伍", "传统强队的稳定表现"),
        xaxis_opts=get_axis_opts("次数", 35),
        yaxis_opts=get_axis_opts("队伍", 100),
        tooltip_opts=get_tooltip_opts(        )
    )
)
bar3.render("view6_top4_teams.html")
print("视图6已保存：view6_top4_teams.html")

# ==================== 视图7：历届世界杯场均进球数 ====================
print("生成视图7：历届世界杯场均进球数...")
# 将年份转换为字符串，确保category类型正常工作
x_data3 = [str(year) for year in summary_df['Year'].astype(int).tolist()]
y_data3 = summary_df['AvgGoalsPerMatch'].round(2).tolist()
line3 = (
    Line(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart7'
    ))
    .add_xaxis(x_data3)
    .add_yaxis(
        "场均进球数",
        y_data3,
        is_smooth=True,
        symbol="circle",
        symbol_size=10,
        linestyle_opts=opts.LineStyleOpts(width=4, color=COLORS['purple']),
        itemstyle_opts=opts.ItemStyleOpts(
            color=COLORS['purple'],
            border_width=3,
            border_color="#ffffff"
        ),
        label_opts=opts.LabelOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(
            opacity=0.2,
            color=COLORS['purple']
        ),
        markline_opts=opts.MarkLineOpts(
            data=[opts.MarkLineItem(type_="average", name="平均值")],
            label_opts=opts.LabelOpts(
                font_size=13,
                color="#64748b",
                font_weight="bold"
            ),
            linestyle_opts=opts.LineStyleOpts(
                type_="dashed",
                width=2,
                color=COLORS['warning']
            )
        ),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值", symbol_size=70),
                opts.MarkPointItem(type_="min", name="最小值", symbol_size=70)
            ],
            label_opts=opts.LabelOpts(
                color="#ffffff",
                font_size=13,
                font_weight="bold"
            ),
            itemstyle_opts=opts.ItemStyleOpts(color=COLORS['danger'])
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("历届世界杯场均进球数变化", "现代足球战术发展对进球数的影响"),
        xaxis_opts=get_axis_opts("年份", 35, type_="category", interval=2),  # interval=2表示每隔2个年份显示一次
        yaxis_opts=get_axis_opts("场均进球数", 60),
        tooltip_opts=get_tooltip_opts(),
        legend_opts=opts.LegendOpts(
            pos_left="8%",
            pos_top="12%",
            textstyle_opts=opts.TextStyleOpts(
                font_size=14,
                color="#475569",
                font_family="Arial, sans-serif"
            )
        )
    )
)
line3.render("view7_avg_goals.html")
print("视图7已保存：view7_avg_goals.html")

# ==================== 视图8：各队获得冠军次数 ====================
print("生成视图8：各队获得冠军次数...")
champion_sorted = dict(sorted(champion_count.items(), key=lambda x: x[1], reverse=True))
bar4 = (
    Bar(init_opts=opts.InitOpts(
        theme=ThemeType.MACARONS,
        width='1600px',
        height='800px',
        bg_color='#ffffff',
        chart_id='chart8'
    ))
    .add_xaxis(list(champion_sorted.keys()))
    .add_yaxis(
        "冠军次数",
        list(champion_sorted.values()),
        itemstyle_opts=opts.ItemStyleOpts(
            color=GRADIENTS['orange_red'],
            border_radius=[10, 10, 0, 0]
        ),
        bar_width="50%",
        label_opts=opts.LabelOpts(
            is_show=True,
            position="top",
            font_size=15,
            font_weight="bold",
            color="#1e293b",
            font_family="Arial, sans-serif"
        )
    )
    .set_global_opts(
        title_opts=get_title_opts("各队获得世界杯冠军次数", "巴西5次夺冠，是世界杯历史上最成功的球队"),
        xaxis_opts=get_axis_opts("队伍", 35, rotate=-45),
        yaxis_opts=get_axis_opts("冠军次数", 50),
        tooltip_opts=get_tooltip_opts(        )
    )
)
bar4.render("view8_champions.html")
print("视图8已保存：view8_champions.html")

print("\n所有可视化视图生成完成！")
