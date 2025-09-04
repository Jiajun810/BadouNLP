#!/usr/bin/env python3
"""
矩阵字典序最大化问题的完整解决方案

问题描述：
给定一个大小为n*m的矩阵A，每次操作可以选择两个不相邻的元素交换，
即选定两个坐标(i1,j1),(i2,j2)满足|i1-i2| + |j1-j2| ≠ 1，
然后交换A_i1,j1和A_i2,j2的元素值。
求在所有操作结果中，矩阵字典序最大的元素分布。

核心思路：
1. 建模为图论问题：每个矩阵位置是一个节点，可交换的位置对之间有边
2. 找出所有连通分量：同一连通分量内的元素可以任意重排
3. 贪心策略：对每个连通分量，将最大的元素放在字典序最小的位置

时间复杂度：O(n²m²) - 主要是构建连通图的开销
空间复杂度：O(nm) - 存储矩阵和连通分量信息
"""


def can_swap(i1, j1, i2, j2):
    """
    检查两个位置是否可以交换
    
    Args:
        i1, j1: 第一个位置的行列坐标
        i2, j2: 第二个位置的行列坐标
    
    Returns:
        bool: 如果曼哈顿距离 > 1，返回True（可以交换）
    """
    manhattan_distance = abs(i1 - i2) + abs(j1 - j2)
    return manhattan_distance > 1


def find_connected_component(n, m, start_i, start_j, visited):
    """
    使用深度优先搜索找到从给定位置开始的连通分量
    
    Args:
        n, m: 矩阵的行数和列数
        start_i, start_j: 起始位置
        visited: 已访问位置的集合
    
    Returns:
        set: 包含所有连通位置的集合
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
    构建矩阵的连通性图
    
    Args:
        n, m: 矩阵的行数和列数
    
    Returns:
        list: 连通分量列表，每个分量是位置坐标的集合
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
    
    Args:
        matrix: 输入的n×m矩阵
    
    Returns:
        list: 字典序最大的矩阵
    
    算法步骤：
    1. 分析矩阵的连通性，找出所有连通分量
    2. 对每个连通分量：
       - 提取所有元素值，按降序排列
       - 提取所有位置，按字典序排列
       - 将最大值分配给字典序最小的位置
    3. 这样保证了全局字典序最大
    """
    if not matrix or not matrix[0]:
        return matrix
    
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
        
        # 按值降序排序（最大值优先）
        values.sort(reverse=True)
        
        # 按位置的字典序排序（行优先，列次之）
        positions.sort(key=lambda pos: (pos[0], pos[1]))
        
        # 贪心分配：将最大的值分配给字典序最小的位置
        for k, (i, j) in enumerate(positions):
            result[i][j] = values[k]
    
    return result


def main():
    """
    主函数：处理标准输入输出
    """
    try:
        # 读取输入
        line = input().strip()
        n, m = map(int, line.split())
        
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
        print("矩阵字典序最大化求解器")
        print("=" * 40)
        print("输入格式：")
        print("第一行：n m（矩阵行数和列数）")
        print("接下来n行：每行m个整数")
        print()
        print("输出格式：")
        print("n行m列：字典序最大的矩阵")
        print()
        print("示例：")
        print("输入：")
        print("2 2")
        print("1 2")
        print("3 4")
        print()
        print("输出：")
        print("4 3")
        print("2 1")


if __name__ == "__main__":
    main()