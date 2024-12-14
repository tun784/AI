import copy
from heapq import heappush, heappop

class priorityQueue:
    def __init__(self):
        self.elements = []

    def push(self, item):
        heappush(self.elements, item)

    def pop(self):
        return heappop(self.elements)

    def is_empty(self):
        return len(self.elements) == 0

# Cau 1: Thay doi ham calculateCosts thanh Manhattan
def calculateCosts(mats, final):
    """Tinh chi phi bang khoang cach Manhattan"""
    total_cost = 0
    for i in range(n):
        for j in range(n):
            if mats[i][j] != 0:
                for x in range(n):
                    for y in range(n):
                        if mats[i][j] == final[x][y]:
                            total_cost += abs(i - x) + abs(j - y)
    return total_cost

# Cau 2: Them tinh nang hien thi so luong trang thai da duyet
states_visited = 0
def increment_states():
    global states_visited
    states_visited += 1 

def display_states_visited():
    print(f"So trang thai da duyet: {states_visited}")

# Cau 3: Tim loi giai ngan nhat
class Node:
    def __init__(self, parent, mats, empty_tile_posi, costs, levels):
        self.parent = parent
        self.mats = mats
        self.empty_tile_posi = empty_tile_posi
        self.costs = costs
        self.levels = levels
        self.total_cost = costs + levels

    def __lt__(self, other):
        return self.total_cost < other.total_cost

# Cau 4: Ngan quay lai trang thai da duyet
visited_states = set()

def is_state_visited(state):
    return state in visited_states

def add_to_visited(state):
    visited_states.add(state)

def matrices_to_tuple(matrix):
    return tuple(tuple(row) for row in matrix)

# Kiem tra tinh kha thi cua bai toan
def count_inversions(arr):
    inversions = 0
    arr = [num for row in arr for num in row if num != 0]
    for i in range(len(arr)):
        for j in range(i + 1, len(arr)):
            if arr[i] > arr[j]:
                inversions += 1
    return inversions

def is_solvable(initial, final):
    initial_inversions = count_inversions(initial)
    final_inversions = count_inversions(final)
    return initial_inversions % 2 == final_inversions % 2

# Cau 5: Tao menu lua chon cau hoi
rows = [1, 0, -1, 0]
cols = [0, -1, 0, 1]
n = 3

def giai_quyet_bai_toan(initial, empty_tile_posi, final):
    global states_visited
    states_visited = 0
    pq = []
    costs = calculateCosts(initial, final)
    root = Node(None, initial, empty_tile_posi, costs, 0)
    heappush(pq, root)

    while pq:
        current = heappop(pq)
        state_tuple = matrices_to_tuple(current.mats)

        if is_state_visited(state_tuple):
            continue

        add_to_visited(state_tuple)
        increment_states()

        if current.costs == 0:
            print("Loi giai da tim thay:")
            printPath(current)
            display_states_visited()
            return

        for i in range(4):
            new_pos = [
                current.empty_tile_posi[0] + rows[i],
                current.empty_tile_posi[1] + cols[i],
            ]
            if 0 <= new_pos[0] < n and 0 <= new_pos[1] < n:
                child = newNodes(
                    current.mats,
                    current.empty_tile_posi,
                    new_pos,
                    current.levels + 1,
                    current,
                    final,
                )
                heappush(pq, child)

    print("Khong tim thay loi giai.")

def newNodes(mats, empty_tile_posi, new_empty_tile_posi, levels, parent, final):
    new_mats = copy.deepcopy(mats)
    x1, y1 = empty_tile_posi
    x2, y2 = new_empty_tile_posi
    new_mats[x1][y1], new_mats[x2][y2] = new_mats[x2][y2], new_mats[x1][y1]
    costs = calculateCosts(new_mats, final)
    return Node(parent, new_mats, new_empty_tile_posi, costs, levels)

def printMatsrix(matrix):
    for row in matrix:
        print(" ".join(map(str, row)))
    print()

def printPath(node):
    if node is None:
        return
    printPath(node.parent)
    printMatsrix(node.mats)

def cau5():
    print("Vui long chon cau can thuc hien:")
    print("1. Thay doi ham calculateCosts de su dung khoang cach Manhattan.")
    print("2. Dem va hien thi so luong trang thai da duyet.")
    print("3. Tim loi giai ngan nhat.")
    print("4. Ngan quay lai trang thai da duyet.")
    return int(input("Nhap so cau (1-4): "))

def cau_1(initial, empty_tile_posi, final):
    print("Cau 1: Su dung khoang cach Manhattan.")
    giai_quyet_bai_toan(initial, empty_tile_posi, final)

def cau_2():
    print("Cau 2: Hien thi so luong trang thai da duyet.")
    display_states_visited()

def cau_3(initial, empty_tile_posi, final):
    print("Cau 3: Tim loi giai ngan nhat.")
    giai_quyet_bai_toan(initial, empty_tile_posi, final)

def cau_4(initial, empty_tile_posi, final):
    print("Cau 4: Ngan quay lai trang thai da duyet.")
    giai_quyet_bai_toan(initial, empty_tile_posi, final)

def main():
    initial = [[1, 2, 3], [5, 6, 0], [7, 8, 4]]
    final = [[1, 2, 3], [5, 8, 6], [0, 7, 4]]
    empty_tile_posi = [1, 2]

    if not is_solvable(initial, final):
        print("Trang thai dau khong the dat den trang thai dich.")
        return

    while True:
        choice = cau5()
        if choice == 1:
            cau_1(initial, empty_tile_posi, final)
        elif choice == 2:
            cau_2()
        elif choice == 3:
            cau_3(initial, empty_tile_posi, final)
        elif choice == 4:
            cau_4(initial, empty_tile_posi, final)
        else:
            print("Lua chon khong hop le.")

if __name__ == "__main__":
    main()