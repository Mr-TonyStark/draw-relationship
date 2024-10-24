from graphviz import Digraph
import os

def create_family_tree():
    dot = Digraph(comment='平凡的世界人物关系图')
    dot.attr(rankdir='TB', size='12,8', dpi='300')
    dot.attr('node', shape='box', style='filled', color='lightblue', fontname='SimHei')
    dot.attr('edge', color='gray')

    # 主标题
    with dot.subgraph(name='cluster_0') as c:
        c.attr(label='《平凡的世界》', fontsize='20', fontname='SimHei')
        c.node('title', style='invis')

    # 孙家
    with dot.subgraph(name='cluster_1') as c:
        c.attr(label='孙家', style='filled', color='lightsalmon')
        c.node('孙玉厚')
        c.node('孙玉亭')
        with c.subgraph() as s:
            s.attr(rank='same')
            s.node('孙少安')
            s.node('孙少平')
            s.node('孙兰香')
        c.edge('孙玉厚', '孙少安')
        c.edge('孙玉厚', '孙少平')
        c.edge('孙玉厚', '孙兰香')

    # 金家
    with dot.subgraph(name='cluster_2') as c:
        c.attr(label='金家', style='filled', color='tan')
        c.node('金俊武')
        c.node('金俊文')
        with c.subgraph() as s:
            s.attr(rank='same')
            s.node('金富')
            s.node('金强')
        c.edge('金俊文', '金富')
        c.edge('金俊文', '金强')

    # 领导干部
    with dot.subgraph(name='cluster_3') as c:
        c.attr(label='领导干部', style='filled', color='lightgreen')
        c.node('冯世宽')
        c.node('田福军')
        c.node('高步杰')

    # 其他人物关系
    dot.edge('孙少安', '田润叶', '单恋', dir='both')
    dot.edge('孙少平', '田晓霞', '恋人')
    dot.edge('金富', '孙兰香', '夫妻')

    return dot

# 生成图片
family_tree = create_family_tree()
output_file = '平凡的世界人物关系图'

try:
    # 渲染并保存图片
    family_tree.render(output_file, format='png', cleanup=True)
    
    # 检查文件是否成功创建
    if os.path.exists(f"{output_file}.png"):
        print(f"图片已成功保存为 {output_file}.png")
    else:
        print("图片保存失败")
except Exception as e:
    print(f"生成图片时发生错误: {e}")