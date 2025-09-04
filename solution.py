#!/usr/bin/env python3
"""
矩阵字典序最大化问题的解决方案

给定一个大小为n*m的矩阵A，可以交换不相邻的元素（曼哈顿距离>1）。
求所有操作结果中字典序最大的矩阵。

算法思路：
1. 构建连通图：找出所有可以通过交换操作相互到达的位置集合
2. 对每个连通分量，将最大的元素放在字典序最小的位置上
3. 这样可以保证整体字典序最大
"""


def can_swap(i1, j1, i2, j2):
    """
    检查两个位置是否可以交换
    条件：曼哈顿距离 > 1
    """
    return abs(i1 - i2) + abs(j1 - j2) > 1


def find_connected_component(n, m, start_i, start_j, visited):
    """
    使用DFS找到从给定位置开始的连通分量
    连通分量内的所有位置可以通过一系列交换操作相互到达
    """
    if (start_i, start_j) in visited:
        return set()
    
    component = set()
    stack = [(start_i, start_j)]
    
    while stack:
        i, j = stack.pop()
        if (i, j) in visited:
            continue
        
        visited.add((i, j))
        component.add((i, j))
        
        # 查找所有可以直接交换的位置
        for i2 in range(n):
            for j2 in range(m):
                if (i2, j2) not in visited and can_swap(i, j, i2, j2):
                    stack.append((i2, j2))
    
    return component


def build_connectivity_graph(n, m):
    """
    构建连通性图，找出所有连通分量
    每个连通分量内的元素可以任意重排列
    """
    visited = set()
    components = []
    
    for i in range(n):
        for j in range(m):
            if (i, j) not in visited:
                component = find_connected_component(n, m, i, j, visited)
                if component:
                    components.append(component)
    
    return components


def solve_matrix_optimization(matrix):
    """
    解决矩阵字典序最大化问题
    
    算法步骤：
    1. 分析矩阵的连通性
    2. 对每个连通分量进行优化：
       - 提取分量中的所有值，按降序排列
       - 提取分量中的所有位置，按字典序排列
       - 将最大值分配给字典序最小的位置
    """
    n, m = len(matrix), len(matrix[0])
    
    # 构建连通性图
    components = build_connectivity_graph(n, m)
    
    # 创建结果矩阵
    result = [[0] * m for _ in range(n)]
    
    # 对每个连通分量进行优化
    for component in components:
        # 获取该分量中所有元素的值
        values = []
        positions = []
        
        for i, j in component:
            values.append(matrix[i][j])
            positions.append((i, j))
        
        # 按值降序排序
        values.sort(reverse=True)
        
        # 按位置的字典序排序（行优先，列次之）
        positions.sort(key=lambda pos: (pos[0], pos[1]))
        
        # 将最大的值分配给字典序最小的位置
        for k, (i, j) in enumerate(positions):
            result[i][j] = values[k]
    
    return result


def main():
    """
    主函数：处理标准输入输出
    """
    try:
        # 读取输入
        n, m = map(int, input().split())
        matrix = []
        for _ in range(n):
            row = list(map(int, input().split()))
            matrix.append(row)
        
        # 求解
        result = solve_matrix_optimization(matrix)
        
        # 输出结果
        for row in result:
            print(' '.join(map(str, row)))
            
    except EOFError:
        # 如果没有输入，显示使用说明
        print("使用说明：")
        print("第一行输入 n m（矩阵大小）")
        print("接下来n行，每行m个整数")
        print()
        print("示例输入：")
        print("2 2")
        print("1 2")
        print("3 4")
        print()
        print("示例输出：")
        print("4 3")
        print("2 1")


if __name__ == "__main__":
    main()