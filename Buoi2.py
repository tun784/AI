import copy
from heapq import heappush, heappop
import math

# Bai 1
n = 4  # Kich thuoc cua bang (4x4 cho 15-puzzle)
rows = [1, 0, -1, 0]  # Huong di: xuong, trai, len, phai
cols = [0, -1, 0, 1]

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def push(self, node):
        heappush(self.heap, node)

    def pop(self):
        return heappop(self.heap)

    def empty(self):
        return len(self.heap) == 0

class Node:
    def __init__(self, parent, matrix, empty_tile_pos, cost, level):
        self.parent = parent
        self.matrix = matrix
        self.empty_tile_pos = empty_tile_pos
        self.cost = cost
        self.level = level

    def __lt__(self, other):
        return self.cost < other.cost

def calculate_cost(matrix, final):
    count = 0
    for i in range(n):
        for j in range(n):
            if matrix[i][j] and matrix[i][j] != final[i][j]:
                count += 1
    return count

def create_new_node(matrix, empty_tile_pos, new_empty_tile_pos, level, parent, final):
    new_matrix = copy.deepcopy(matrix)
    x1, y1 = empty_tile_pos
    x2, y2 = new_empty_tile_pos
    new_matrix[x1][y1], new_matrix[x2][y2] = new_matrix[x2][y2], new_matrix[x1][y1]
    cost = calculate_cost(new_matrix, final)
    return Node(parent, new_matrix, new_empty_tile_pos, cost, level)

def is_safe(x, y):
    return 0 <= x < n and 0 <= y < n

def print_path(node):
    if node is None:
        return
    print_path(node.parent)
    for row in node.matrix:
        print(row)
    print()

def solve_15_puzzle(initial, empty_tile_pos, final):
    pq = PriorityQueue()
    root_cost = calculate_cost(initial, final)
    root = Node(None, initial, empty_tile_pos, root_cost, 0)
    pq.push(root)

    while not pq.empty():
        current = pq.pop()

        if current.cost == 0:
            print("Giai phap da duoc tim thay:")
            print_path(current)
            return

        x, y = current.empty_tile_pos
        for i in range(4):
            new_x, new_y = x + rows[i], y + cols[i]

            if is_safe(new_x, new_y):
                child = create_new_node(current.matrix, (x, y), (new_x, new_y), current.level + 1, current, final)
                pq.push(child)

# Cau hinh dau vao cho bai toan 15-puzzle
initial = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 0],
    [13, 14, 15, 12]
]

final = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
    [13, 14, 15, 0]
]

empty_tile_pos = (2, 3)  # Vi tri o trong trong cau hinh ban dau
solve_15_puzzle(initial, empty_tile_pos, final)

# Bai 2
class Graph:
    def __init__(self, adj_list):
        self.adj_list = adj_list

    def get_neighbors(self, node):
        return self.adj_list[node]

    def heuristic(self, node, goal):
        # Ham heuristic, su dung khoang cach Euclidean giua cac diem
        h_dist = {
            'A': 4,
            'B': 6,
            'C': 7,
            'D': 2,
            'E': 3,
            'F': 1
        }
        return h_dist.get(node, 0)

    def a_star(self, start, goal):
        open_list = []
        heappush(open_list, (0, start))
        costs = {start: 0}
        parents = {start: None}

        while open_list:
            _, current = heappop(open_list)

            if current == goal:
                path = []
                while current:
                    path.append(current)
                    current = parents[current]
                path.reverse()
                return path

            for (neighbor, weight) in self.get_neighbors(current):
                new_cost = costs[current] + weight

                if neighbor not in costs or new_cost < costs[neighbor]:
                    costs[neighbor] = new_cost
                    priority = new_cost + self.heuristic(neighbor, goal)
                    heappush(open_list, (priority, neighbor))
                    parents[neighbor] = current

        return None

# Do thi voi cac diem va trong so cua cac canh
adjacency_list = {
    'A': [('B', 1), ('C', 3), ('D', 7)],
    'B': [('A', 1), ('D', 5)],
    'C': [('A', 3), ('D', 12)],
    'D': [('A', 7), ('B', 5), ('C', 12), ('E', 2)],
    'E': [('D', 2), ('F', 3)],
    'F': [('E', 3)]
}

graph = Graph(adjacency_list)
start = 'A'
goal = 'F'
path = graph.a_star(start, goal)

if path:
    print(f"Duong di ngan nhat tu {start} den {goal}: {path}")
else:
    print("Khong tim thay duong di.")