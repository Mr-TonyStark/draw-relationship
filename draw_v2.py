from graphviz import Digraph
from PIL import Image
import os

def resize_image(image_path, size=(100, 100)):
    """调整图片大小并保存为PNG"""
    with Image.open(image_path) as img:
        img = img.convert('RGBA')  # 确保图片有 alpha 通道
        img = img.resize(size, Image.LANCZOS)
        new_path = f"resized_{os.path.splitext(os.path.basename(image_path))[0]}.png"
        img.save(new_path, 'PNG')
        return new_path

# 创建一个有向图
dot = Digraph(comment='Family Business Network')
dot.attr(rankdir='TB', size='10,10')  # 增加图片大小

# 定义节点样式
dot.attr('node', shape='none', margin='0')

# 添加节点（人物）
people = {
    "爸爸": {"photo": "Dad.jpg", "identity": "CEO"},
    "妈妈": {"photo": "Mom.jpg", "identity": "CFO"},
    "叔叔": {"photo": "Uncle.jpg", "identity": "CTO"},
    "阿姨": {"photo": "Aunt.jpg", "identity": "COO"},
    "哥哥": {"photo": "Brother.jpg", "identity": "经理"},
    "妹妹": {"photo": "Sister.jpg", "identity": "实习生"}
}

# 调整所有图片大小
for name, info in people.items():
    info['photo'] = resize_image(info['photo'])

# 创建一个子图来放置"爸爸"节点
with dot.subgraph(name='center') as c:
    c.attr(rank='min')  # 将这个子图放在最上层
    c.node("爸爸", f'''<
    <table border="0" cellborder="0" cellspacing="0">
    <tr><td><img src="{people['爸爸']['photo']}" width="100" height="100"/></td></tr>
    <tr><td>爸爸</td></tr>
    <tr><td>{people['爸爸']['identity']}</td></tr>
    </table>
    >''')

# 添加其他节点
for name, info in people.items():
    if name != "爸爸":  # 跳过"爸爸"节点，因为已经添加过了
        dot.node(name, f'''<
        <table border="0" cellborder="0" cellspacing="0">
        <tr><td><img src="{info['photo']}" width="100" height="100"/></td></tr>
        <tr><td>{name}</td></tr>
        <tr><td>{info['identity']}</td></tr>
        </table>
        >''')

# 添加边（关系）
relationships = {
    ("爸爸", "妈妈"): "夫妻",
    ("爸爸", "叔叔"): "兄弟",
    ("妈妈", "阿姨"): "姐妹",
    ("爸爸", "哥哥"): "父子",
    ("妈妈", "哥哥"): "母子",
    ("爸爸", "妹妹"): "父女",
    # ("妈妈", "妹妹"): "母女",
    # ("哥哥", "妹妹"): "兄妹",
    ("叔叔", "哥哥"): "叔侄",
    # ("阿姨", "妹妹"): "姨甥女",
}

for (person1, person2), relation in relationships.items():
    dot.edge(person1, person2, label=relation)

# 保存图像
dot.render('family_business_network', format='png', cleanup=True)

# 清理调整大小后的图片
for info in people.values():
    os.remove(info['photo'])