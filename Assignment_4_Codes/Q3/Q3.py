import copy
from collections import deque

SIZE = 9


# ---------------------------
# PRINTING
# ---------------------------
def print_grid(grid, title=""):
    if title:
        print(title)
    for i in range(SIZE):
        if i % 3 == 0 and i != 0:
            print("-" * 21)
        for j in range(SIZE):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")
            val = grid[i][j]
            print(val if val != 0 else ".", end=" ")
        print()
    print()


# ---------------------------
# CSP HELPERS
# ---------------------------
def get_neighbors(row, col):
    neighbors = set()

    for i in range(SIZE):
        if i != col:
            neighbors.add((row, i))
        if i != row:
            neighbors.add((i, col))

    box_x = (col // 3) * 3
    box_y = (row // 3) * 3

    for i in range(box_y, box_y + 3):
        for j in range(box_x, box_x + 3):
            if (i, j) != (row, col):
                neighbors.add((i, j))

    return neighbors


def initialize_domains(grid):
    domains = {}
    for i in range(SIZE):
        for j in range(SIZE):
            if grid[i][j] == 0:
                domains[(i, j)] = set(range(1, 10))
            else:
                domains[(i, j)] = {grid[i][j]}
    return domains


# ---------------------------
# AC-3
# ---------------------------
def revise(domains, xi, xj):
    revised = False
    to_remove = set()

    for x in domains[xi]:
        if not any(x != y for y in domains[xj]):
            to_remove.add(x)

    if to_remove:
        domains[xi] -= to_remove
        revised = True

    return revised


def ac3(domains):
    queue = deque()

    for xi in domains:
        for xj in get_neighbors(*xi):
            queue.append((xi, xj))

    while queue:
        xi, xj = queue.popleft()

        if revise(domains, xi, xj):
            if not domains[xi]:
                return False

            for xk in get_neighbors(*xi):
                if xk != xj:
                    queue.append((xk, xi))

    return True


# ---------------------------
# HEURISTICS
# ---------------------------
def select_unassigned_variable(domains):
    # MRV
    return min(
        (v for v in domains if len(domains[v]) > 1),
        key=lambda var: len(domains[var]),
        default=None
    )


def order_domain_values(domains, var):
    # LCV
    def count_constraints(value):
        count = 0
        for neighbor in get_neighbors(*var):
            if value in domains[neighbor]:
                count += 1
        return count

    return sorted(domains[var], key=count_constraints)


# ---------------------------
# BACKTRACKING + AC3
# ---------------------------
def backtrack(domains):
    var = select_unassigned_variable(domains)
    if var is None:
        return domains  # solved

    for value in order_domain_values(domains, var):
        new_domains = copy.deepcopy(domains)
        new_domains[var] = {value}

        if ac3(new_domains):
            result = backtrack(new_domains)
            if result:
                return result

    return None


def domains_to_grid(domains):
    grid = [[0]*SIZE for _ in range(SIZE)]
    for (i, j), val in domains.items():
        grid[i][j] = next(iter(val))
    return grid


# ---------------------------
# TEST CASES
# ---------------------------
test_cases = [
    # Easy
    [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ],

    # Medium
    [
        [0, 2, 0, 6, 0, 8, 0, 0, 0],
        [5, 8, 0, 0, 0, 9, 7, 0, 0],
        [0, 0, 0, 0, 4, 0, 0, 0, 0],
        [3, 7, 0, 0, 0, 0, 5, 0, 0],
        [6, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 1, 3],
        [0, 0, 0, 0, 2, 0, 0, 0, 0],
        [0, 0, 9, 8, 0, 0, 0, 3, 6],
        [0, 0, 0, 3, 0, 6, 0, 9, 0]
    ],

    # Hard
    [
        [0, 0, 0, 0, 0, 0, 0, 1, 2],
        [0, 0, 0, 0, 3, 5, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 4, 0, 7],
        [0, 0, 4, 0, 0, 0, 1, 0, 0],
        [6, 0, 9, 0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 8, 0, 0],
        [0, 0, 0, 6, 1, 0, 0, 0, 0],
        [2, 5, 0, 0, 0, 0, 0, 0, 0]
    ]
]


# ---------------------------
# DRIVER
# ---------------------------
for idx, case in enumerate(test_cases, 1):
    print(f"\n===== Test Case {idx} =====\n")

    print_grid(case, "Problem:")

    input("Press Enter to see the solution...")

    domains = initialize_domains(case)

    if ac3(domains):
        result = backtrack(domains)
        if result:
            solved = domains_to_grid(result)
            print_grid(solved, "Solution:")
        else:
            print("No solution found.")
    else:
        print("No solution (AC3 failed early).")

    if idx != len(test_cases):
        input("Press Enter to go to the next test case...")
