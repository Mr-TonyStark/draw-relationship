from PIL import Image, ImageDraw, ImageFont
import networkx as nx
import os

# 创建一个图
G = nx.DiGraph()

# 添加节点（人物）和边（关系）
G.add_node("Alice", photo="Alice.jpg", identity="Engineer")
G.add_node("Bob", photo="Bob.jpg", identity="Designer")
G.add_node("Charlie", photo="Charlie.jpg", identity="Manager")
G.add_node("David", photo="David.jpg", identity="Analyst")

# 使用字典手动设置人物关系
relationships = {
    "Alice": ["Bob", "Charlie"],
    "Bob": ["Charlie"],
    "Charlie": ["David"],
}

# 添加边（关系）
for person, friends in relationships.items():
    for friend in friends:
        G.add_edge(person, friend)

# 手动设置主要人物节点的位置
pos = {
    "Alice": (400, 100),
    "Bob": (100, 400),
    "Charlie": (400, 400),
    "David": (700, 400),
}

# 创建一个大的白色背景图像
img = Image.new('RGB', (800, 600), color='white')
draw = ImageDraw.Draw(img)

# 尝试加载系统默认字体
try:
    font = ImageFont.load_default()
    small_font = ImageFont.load_default()
except:
    # 如果默认字体加载失败，可以尝试使用特定的字体文件
    # 请确保这个字体文件存在于您的系统中
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    font = ImageFont.truetype(font_path, 20)
    small_font = ImageFont.truetype(font_path, 16)

# 首先绘制所有的边（关系）
for start, end in G.edges:
    start_pos = pos[start]
    end_pos = pos[end]
    draw.line([start_pos, end_pos], fill='red', width=2)
    mid_x = (start_pos[0] + end_pos[0]) // 2
    mid_y = (start_pos[1] + end_pos[1]) // 2
    draw.text((mid_x, mid_y), f"{start} -> {end}", font=small_font, fill='black')

# 然后绘制节点
for node in G.nodes:
    x, y = pos[node]
    # 加载并调整头像大小
    avatar = Image.open(G.nodes[node]['photo']).resize((100, 100))
    img.paste(avatar, (x-50, y-50))
    # 绘制人名和身份
    draw.text((x, y+60), node, font=font, fill='black', anchor='ms')
    draw.text((x, y+85), G.nodes[node]['identity'], font=small_font, fill='black', anchor='ms')

# 保存图像
img.save("relationship_network.png")