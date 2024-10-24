import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from PIL import Image
import numpy as np

def resize_image(image_path, size=(100, 100)):
    with Image.open(image_path) as img:
        img = img.resize(size, Image.LANCZOS)
        return np.array(img)

# 创建一个有向图
G = nx.DiGraph()

# 添加节点（人物）
people = {
    "爸爸": {"photo": "Dad.jpg", "identity": "CEO"},
    "妈妈": {"photo": "Mom.jpg", "identity": "CFO"},
    "叔叔": {"photo": "Uncle.jpg", "identity": "CTO"},
    "阿姨": {"photo": "Aunt.jpg", "identity": "COO"},
    "哥哥": {"photo": "Brother.jpg", "identity": "经理"},
    "妹妹": {"photo": "Sister.jpg", "identity": "实习生"}
}

G.add_nodes_from(people.keys())

# 添加边（关系）
relationships = {
    ("爸爸", "妈妈"): "夫妻",
    ("爸爸", "叔叔"): "兄弟",
    ("妈妈", "阿姨"): "姐妹",
    ("爸爸", "哥哥"): "父子",
    ("妈妈", "哥哥"): "母子",
    ("爸爸", "妹妹"): "父女",
    ("妈妈", "妹妹"): "母女",
    ("哥哥", "妹妹"): "兄妹",
    ("叔叔", "哥哥"): "叔侄",
    ("阿姨", "妹妹"): "姨甥女",
}

G.add_edges_from(relationships.keys())

# 设置布局
pos = nx.spring_layout(G, k=0.9, iterations=50)

# 创建图形
plt.figure(figsize=(16, 12))

# 绘制边（关系）
nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, arrowsize=20)

# 绘制边标签（关系）
edge_labels = {(u, v): d for (u, v), d in relationships.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, font_family='SimHei')

# 绘制节点（人物头像）
for node in G.nodes():
    img = resize_image(people[node]['photo'])
    imagebox = OffsetImage(img, zoom=0.5)
    ab = AnnotationBbox(imagebox, pos[node], frameon=False)
    plt.gca().add_artist(ab)
    
    # 添加人名和身份
    plt.text(pos[node][0], pos[node][1]-0.05, node, ha='center', va='center', fontsize=12, fontweight='bold', fontfamily='SimHei')
    plt.text(pos[node][0], pos[node][1]-0.1, people[node]['identity'], ha='center', va='center', fontsize=10, fontfamily='SimHei')

plt.axis('off')  # 关闭坐标轴

# 保存图像
plt.savefig("family_business_network_matplotlib.png", dpi=300, bbox_inches='tight')
plt.close()