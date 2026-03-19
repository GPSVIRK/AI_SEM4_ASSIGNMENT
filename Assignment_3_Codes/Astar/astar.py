import heapq
import math
import random
import time


GRID_SIZE   = 40          # 30x30 grid (represents 30x30 km)
DENSITY_MAP = {"low": 0.10, "medium": 0.25, "high": 0.40}

MOVES = [#change in value and cost
    (-1,  0, 1.0),          # N
    ( 1,  0, 1.0),          # S
    ( 0, -1, 1.0),          # W
    ( 0,  1, 1.0),          # E
    (-1, -1, math.sqrt(2)), # NW
    (-1,  1, math.sqrt(2)), # NE
    ( 1, -1, math.sqrt(2)), # SW
    ( 1,  1, math.sqrt(2)), # SE
]


def generate_grid(rows, cols, density, start, goal, seed=None):
    rng = random.Random(seed)
    grid = [
        [1 if rng.random() < density else 0 for _ in range(cols)]
        for _ in range(rows)
    ]
    # Always keep start and goal free
    grid[start[0]][start[1]] = 0
    grid[goal[0]][goal[1]]   = 0
    return grid




def heuristic(r1, c1, r2, c2):#octile distance
    dx, dy = abs(r1 - r2), abs(c1 - c2)
    return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)


def astar(grid, start, goal):
    rows, cols = len(grid), len(grid[0])
    gr, gc = goal

    open_heap = []
    open_map  = {}   # (r,c) -> best g_cost seen
    closed    = set()
    came_from = {}   # (r,c) -> (parent_r, parent_c)

    t0 = time.perf_counter()

    start_h = heuristic(start[0], start[1], gr, gc)
    heapq.heappush(open_heap, (start_h, start_h, start[0], start[1], 0.0))
    open_map[(start[0], start[1])] = 0.0

    nodes_expanded  = 0
    nodes_generated = 1
    peak_memory     = 1

    while open_heap:
        f, h, r, c, g = heapq.heappop(open_heap)

        if (r, c) in closed:
            continue

        closed.add((r, c))
        nodes_expanded += 1
        peak_memory = max(peak_memory, len(open_map) + len(closed))

        if (r, c) == (gr, gc):
            # Reconstruct path
            path = []
            cur = (r, c)
            while cur != start:
                path.append(cur)
                cur = came_from[cur]
            path.append(start)
            path.reverse()

            elapsed_ms = (time.perf_counter() - t0) * 1000
            path_len = sum(
                heuristic(path[i][0], path[i][1], path[i+1][0], path[i+1][1])
                for i in range(len(path) - 1)
            )
            return {
                "found":           True,
                "path":            path,
                "path_length":     path_len,
                "nodes_expanded":  nodes_expanded,
                "nodes_generated": nodes_generated,
                "elapsed_ms":      elapsed_ms,
                "peak_memory":     peak_memory,
            }

        for dr, dc, cost in MOVES:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols):
                continue
            if grid[nr][nc] == 1:
                continue
            if (nr, nc) in closed:
                continue

            new_g = g + cost
            if open_map.get((nr, nc), float("inf")) <= new_g:
                continue

            open_map[(nr, nc)] = new_g
            came_from[(nr, nc)] = (r, c)
            nh = heuristic(nr, nc, gr, gc)
            heapq.heappush(open_heap, (new_g + nh, nh, nr, nc, new_g))
            nodes_generated += 1

    elapsed_ms = (time.perf_counter() - t0) * 1000
    return {
        "found":           False,
        "path":            [],
        "path_length":     float("inf"),
        "nodes_expanded":  nodes_expanded,
        "nodes_generated": nodes_generated,
        "elapsed_ms":      elapsed_ms,
        "peak_memory":     peak_memory,
    }


def render(grid, path, start, goal):
    path_set = set(path)
    rows, cols = len(grid), len(grid[0])

    lines = []
    # last digit only to keep narrow for coloumns
    lines.append("    " + " ".join(str(c % 10) for c in range(cols)))
    lines.append("    " + "- " * cols)

    for r in range(rows):
        row_str = f"{r:3d}|"
        for c in range(cols):
            if (r, c) == tuple(start):
                row_str += "S "
            elif (r, c) == tuple(goal):
                row_str += "G "
            elif (r, c) in path_set:
                row_str += "@ "
            elif grid[r][c] == 1:
                row_str += "# "
            else:
                row_str += ". "
        lines.append(row_str)

    return "\n".join(lines)


def print_moe(result, grid, start, goal, density_label):
    rows, cols = len(grid), len(grid[0])
    obstacle_count = sum(grid[r][c] for r in range(rows) for c in range(cols))
    obstacle_pct   = obstacle_count / (rows * cols) * 100

    sl  = heuristic(start[0], start[1], goal[0], goal[1])
    pl  = result["path_length"]
    exp = result["nodes_expanded"]

    print("=" * 50)
    print("       MEASURES OF EFFECTIVENESS (MoE)")
    print("=" * 50)
    print(f"  Grid Size              : {rows} x {cols} km")
    print(f"  Start Node             : {start}")
    print(f"  Goal Node              : {goal}")
    print(f"  Obstacle Density       : {density_label.upper()} ({obstacle_pct:.1f}%)")
    print(f"  Path Found             : {'YES' if result['found'] else 'NO'}")
    if result["found"]:
        print(f"  Path Length            : {pl:.3f} km  ({len(result['path'])} cells)")
        print(f"  Straight-Line Distance : {sl:.3f} km")
        print(f"  Path Optimality Ratio  : {pl / sl:.4f}  (1.000 = ideal)")
        print(f"  Nodes Expanded         : {exp}")
        print(f"  Nodes Generated        : {result['nodes_generated']}")
        print(f"  Search Efficiency      : {pl / max(exp, 1):.5f} km / node")
        print(f"  Time Elapsed           : {result['elapsed_ms']:.3f} ms")
        print(f"  Peak Memory (nodes)    : {result['peak_memory']}")
    else:
        print("  [!] No valid path — all routes are blocked.")
    print("=" * 50)


def get_coord(prompt, rows, cols):
    while True:
        try:
            raw = input(prompt).strip()
            r, c = map(int, raw.split(","))
            if 0 <= r < rows and 0 <= c < cols:
                return (r, c)
            print(f"    Out of bounds. Row: 0-{rows-1}, Col: 0-{cols-1}")
        except ValueError:
            print("    Format must be: row,col  (e.g. 0,0)")


def main():
    print("=" * 50)
    print("    UGV A* BATTLEFIELD PATHFINDER")
    print("=" * 50)
    print(f"  Grid  : {GRID_SIZE} x {GRID_SIZE} km")
    print(f"  Move  : 8-directional")
    print(f"  Legend: S=Start  G=Goal  @=Path  #=Obstacle  .=Free")
    print()

    print("  Obstacle density: low (10%) / medium (25%) / high (40%)")
    while True:
        density_label = input("  Choose density [medium]: ").strip().lower() or "medium"
        if density_label in DENSITY_MAP:
            break
        print("  Please enter: low, medium, or high")

    density = DENSITY_MAP[density_label]

    seed_raw = input("  Random seed (leave blank for random): ").strip()
    seed = int(seed_raw) if seed_raw.lstrip("-").isdigit() else None

    rows = cols = GRID_SIZE

    print(f"\n  Grid indices  row: 0-{rows-1}   col: 0-{cols-1}")
    start = get_coord("  Enter START (row,col) e.g. 0,0        : ", rows, cols)
    goal  = get_coord(f"  Enter GOAL  (row,col) e.g. {rows-1},{cols-1}: ", rows, cols)

    if start == goal:
        print("\n  Start and Goal are the same — trivial path.")
        return

    print("\n  Generating battlefield grid...")
    grid = generate_grid(rows, cols, density, start, goal, seed)

    print("  Running A* search...\n")
    result = astar(grid, start, goal)

    print(render(grid, result["path"], start, goal))
    print()
    print_moe(result, grid, start, goal, density_label)


if __name__ == "__main__":
    main()
