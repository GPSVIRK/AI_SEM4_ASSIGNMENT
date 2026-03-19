"""
UGV D* Lite Pathfinding — Dynamic Battlefield
==============================================
D* Lite replans efficiently when the environment changes.
Obstacles can move, appear, or disappear each step.

Controls:
  SPACE       – Step the UGV one move forward
  A           – Auto-run (hold to animate continuously)
  R           – Reset with new random map
  Click cell  – Toggle obstacle manually
  ESC / Q     – Quit

Legend (on screen):
  Dark blue   = Free cell
  Steel blue  = Static obstacle
  Orange      = Moving obstacle
  Cyan line   = Current planned path
  Green       = UGV (robot)
  Red         = Goal
  Teal tint   = Cells expanded during last replan
"""

import heapq
import math
import random
import time
import sys

try:
    import pygame
except ImportError:
    print("pygame not found. Install it with:  pip install pygame")
    sys.exit(1)


GRID         = 40          # 40x40 cells
CELL         = 24          # pixels per cell
PANEL_W      = 280         # right info panel width
FPS          = 30

NUM_MOVING   = 8           # number of drifting obstacles
STATIC_DENS  = 0.18        # fraction of grid that is static obstacles
MOVE_PROB    = 0.6         # chance a moving obstacle moves each step
APPEAR_PROB  = 0.03        # chance a random free cell becomes obstacle
DISAPPEAR_P  = 0.04        # chance a static obstacle disappears

C_BG         = (5,  10,  18)
C_FREE       = (13, 31,  45)
C_GRID_LINE  = (18, 45,  65)
C_STATIC     = (30, 65, 100)
C_MOVING     = (200,120,  20)
C_PATH       = (0, 220, 255)
C_VISITED    = (10,  60,  75)
C_UGV        = (0,  255, 130)
C_GOAL       = (220,  40,  60)
C_PANEL      = (8,  18,  28)
C_ACCENT     = (0,  200, 230)
C_TEXT       = (130,180,210)
C_BRIGHT     = (200,235,255)
C_WARNING    = (255,160,  40)
C_REPLAN     = (0,  80,  80)

INF = float("inf")

class DStarLite:
    """
    D* Lite (Koenig & Likhachev 2002).
    Searches backward from goal to start so incremental repairs are cheap
    when the UGV moves forward and discovers changes.
    """

    def __init__(self, grid, start, goal):
        self.rows  = len(grid)
        self.cols  = len(grid[0])
        self.grid  = [row[:] for row in grid]
        self.start = start   # current UGV position (updated each step)
        self.goal  = goal
        self.km    = 0.0     # accumulated heuristic offset

        self.g   = {}        # g[v]   = cost-to-go from v to goal
        self.rhs = {}        # rhs[v] = one-step lookahead of g
        self.open_heap = []  # priority queue
        self.open_set  = {}  # (r,c) -> key, for O(1) membership test

        self.expanded_last = set()   # cells touched in last replan (for viz)

        for r in range(self.rows):
            for c in range(self.cols):
                self.g[(r,c)]   = INF
                self.rhs[(r,c)] = INF

        self.rhs[self.goal] = 0.0
        k = self._calc_key(self.goal)
        heapq.heappush(self.open_heap, (*k, self.goal))
        self.open_set[self.goal] = k

    # --- Heuristic: octile distance from s to goal (which is start of UGV) ---
    def _h(self, r, c):
        dr = abs(r - self.start[0])
        dc = abs(c - self.start[1])
        return max(dr, dc) + (math.sqrt(2)-1)*min(dr,dc)

    def _calc_key(self, node):
        r, c = node
        g_rhs = min(self.g[node], self.rhs[node])
        return (g_rhs + self._h(r,c) + self.km, g_rhs)

    def _neighbors(self, r, c):
        for dr, dc in [(-1,0),(1,0),(0,-1),(0,1),
                       (-1,-1),(-1,1),(1,-1),(1,1)]:
            nr, nc = r+dr, c+dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols:
                yield nr, nc

    def _cost(self, r1,c1, r2,c2):
        if self.grid[r2][c2] != 0:
            return INF
        return math.sqrt((r1-r2)**2 + (c1-c2)**2)

    def _update_vertex(self, node):
        r, c = node
        if node != self.goal:
            best = INF
            for nr,nc in self._neighbors(r,c):
                v = self._cost(r,c,nr,nc) + self.g[(nr,nc)]
                if v < best:
                    best = v
            self.rhs[node] = best

        # Remove from open if present
        if node in self.open_set:
            del self.open_set[node]

        if self.g[node] != self.rhs[node]:
            k = self._calc_key(node)
            heapq.heappush(self.open_heap, (*k, node))
            self.open_set[node] = k

    def compute_shortest_path(self):
        self.expanded_last = set()
        s = self.start

        while self.open_heap:
            # Peek at top key
            top = self.open_heap[0]
            k_old = (top[0], top[1])
            u     = top[2]

            if u not in self.open_set or self.open_set[u] != k_old:
                heapq.heappop(self.open_heap)
                continue

            k_new = self._calc_key(u)
            s_key = self._calc_key(s)

            if k_old >= s_key and self.rhs[s] == self.g[s]:
                break

            heapq.heappop(self.open_heap)
            self.expanded_last.add(u)

            if k_old < k_new:
                self.open_set[u] = k_new
                heapq.heappush(self.open_heap, (*k_new, u))
            elif self.g[u] > self.rhs[u]:
                self.g[u] = self.rhs[u]
                del self.open_set[u]
                for nr, nc in self._neighbors(*u):
                    self._update_vertex((nr,nc))
            else:
                self.g[u] = INF
                self._update_vertex(u)
                for nr, nc in self._neighbors(*u):
                    self._update_vertex((nr,nc))

    def extract_path(self):
        """Greedy gradient descent from start to goal using g values."""
        path = [self.start]
        cur  = self.start
        seen = {cur}
        for _ in range(self.rows * self.cols):
            if cur == self.goal:
                break
            r, c = cur
            best_cost = INF
            best_next = None
            for nr,nc in self._neighbors(r,c):
                if (nr,nc) in seen:
                    continue
                g_val = self.g[(nr,nc)]
                move  = self._cost(r,c,nr,nc)
                total = move + g_val
                if total < best_cost:
                    best_cost = total
                    best_next = (nr,nc)
            if best_next is None:
                return None   # no path
            cur = best_next
            seen.add(cur)
            path.append(cur)
        return path if cur == self.goal else None

    def update_obstacle(self, r, c, is_obstacle):
        """Notify D* Lite that cell (r,c) changed."""
        old = self.grid[r][c]
        new = 1 if is_obstacle else 0
        if old == new:
            return
        self.grid[r][c] = new
        # Re-evaluate all neighbours + the cell itself
        affected = [(r,c)] + list(self._neighbors(r,c))
        for node in affected:
            self._update_vertex(node)

    def move_start(self, new_start):
        """UGV stepped to new_start — update km and start."""
        self.km    += self._h(*self.start)
        self.start  = new_start

    def replan(self):
        self.compute_shortest_path()


# ---------------------------------------------------------------------------
# Dynamic Obstacle Manager
# ---------------------------------------------------------------------------

class ObstacleManager:
    def __init__(self, grid, start, goal, n_moving, seed=None):
        self.rows   = len(grid)
        self.cols   = len(grid[0])
        self.start  = start
        self.goal   = goal
        self.rng    = random.Random(seed)

        # Static obstacles: set of (r,c)
        self.static  = set()
        for r in range(self.rows):
            for c in range(self.cols):
                if grid[r][c] == 1:
                    self.static.add((r,c))

        # Moving obstacles: list of [r, c, dr, dc]
        free = self._free_cells(exclude={start,goal} | self.static)
        sample = self.rng.sample(free, min(n_moving, len(free)))
        dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        self.moving = []
        for (r,c) in sample:
            d = self.rng.choice(dirs)
            self.moving.append([r, c, d[0], d[1]])

    def _free_cells(self, exclude=None):
        ex = exclude or set()
        return [(r,c) for r in range(self.rows) for c in range(self.cols)
                if (r,c) not in ex and (r,c) not in self.static]

    def all_obstacles(self):
        obs = dict()
        for (r,c) in self.static:
            obs[(r,c)] = "static"
        for m in self.moving:
            obs[(m[0],m[1])] = "moving"
        return obs

    def step(self, ugv_pos):
        """Evolve obstacles; return list of (r,c,old_state,new_state) changes."""
        changes = []
        occupied = self.static | {(m[0],m[1]) for m in self.moving} | {ugv_pos, self.goal}

        # --- Move drifting obstacles ---
        for m in self.moving:
            if self.rng.random() > MOVE_PROB:
                continue
            r,c,dr,dc = m
            nr,nc = r+dr, c+dc
            # Bounce off walls or collisions
            if not (0<=nr<self.rows and 0<=nc<self.cols) or (nr,nc) in occupied:
                # try random new direction
                dirs = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
                self.rng.shuffle(dirs)
                moved = False
                for ndr,ndc in dirs:
                    nr2,nc2 = r+ndr, c+ndc
                    if (0<=nr2<self.rows and 0<=nc2<self.cols
                            and (nr2,nc2) not in occupied
                            and (nr2,nc2) != self.goal):
                        m[2],m[3] = ndr,ndc
                        nr,nc = nr2,nc2
                        moved = True
                        break
                if not moved:
                    continue
            else:
                pass  # proceed in same direction

            if (nr,nc) == ugv_pos or (nr,nc) == self.goal:
                continue

            changes.append((r, c, "moving", "free"))
            changes.append((nr, nc, "free", "moving"))
            occupied.discard((r,c))
            occupied.add((nr,nc))
            m[0],m[1] = nr,nc

        # --- Random appearances ---
        free = [cell for cell in self._free_cells()
                if cell not in occupied]
        for cell in free:
            if self.rng.random() < APPEAR_PROB and cell not in {ugv_pos, self.goal}:
                self.static.add(cell)
                changes.append((cell[0], cell[1], "free", "static"))

        # --- Random disappearances ---
        to_remove = [s for s in list(self.static) if self.rng.random() < DISAPPEAR_P]
        for cell in to_remove:
            self.static.discard(cell)
            changes.append((cell[0], cell[1], "static", "free"))

        return changes


# ---------------------------------------------------------------------------
# Pygame Visualizer
# ---------------------------------------------------------------------------

WIDTH  = GRID * CELL + PANEL_W
HEIGHT = GRID * CELL

def cell_rect(r, c):
    return pygame.Rect(c*CELL, r*CELL, CELL, CELL)

def draw_grid(surface, dstar, obs_map, path, ugv, goal, expanded):
    for r in range(GRID):
        for c in range(GRID):
            rect = cell_rect(r, c)
            obs  = obs_map.get((r,c))
            if obs == "static":
                color = C_STATIC
            elif obs == "moving":
                color = C_MOVING
            elif (r,c) in expanded:
                color = C_REPLAN
            else:
                color = C_FREE
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, C_GRID_LINE, rect, 1)

    # Path
    if path:
        for i in range(len(path)-1):
            r1,c1 = path[i]
            r2,c2 = path[i+1]
            x1,y1 = c1*CELL+CELL//2, r1*CELL+CELL//2
            x2,y2 = c2*CELL+CELL//2, r2*CELL+CELL//2
            pygame.draw.line(surface, C_PATH, (x1,y1), (x2,y2), 2)

    # Goal
    gr, gc = goal
    grect = cell_rect(gr, gc)
    pygame.draw.rect(surface, C_GOAL, grect.inflate(-4,-4), border_radius=3)
    pygame.draw.rect(surface, (255,80,100), grect.inflate(-4,-4), 2, border_radius=3)

    # UGV
    ur, uc = ugv
    cx, cy = uc*CELL+CELL//2, ur*CELL+CELL//2
    pygame.draw.circle(surface, C_UGV, (cx,cy), CELL//2-2)
    pygame.draw.circle(surface, (0,180,90), (cx,cy), CELL//2-2, 2)


def draw_panel(surface, font_big, font_med, font_sm, moe, status, step_n):
    px = GRID * CELL
    panel = pygame.Rect(px, 0, PANEL_W, HEIGHT)
    pygame.draw.rect(surface, C_PANEL, panel)
    pygame.draw.line(surface, C_ACCENT, (px,0), (px,HEIGHT), 2)

    y = 14
    def text(txt, f, color, indent=0):
        nonlocal y
        s = f.render(txt, True, color)
        surface.blit(s, (px+10+indent, y))
        y += s.get_height() + 4

    text("UGV D* LITE", font_big, C_ACCENT)
    text("BATTLEFIELD NAV", font_med, C_TEXT)
    y += 8
    pygame.draw.line(surface, C_BORDER := C_ACCENT, (px+8,y), (px+PANEL_W-8,y), 1)
    y += 10

    text(f"Step: {step_n}", font_med, C_BRIGHT)
    text(f"Status: {status}", font_med,
         C_UGV if "MOVING" in status else
         C_WARNING if "REPLAN" in status else
         C_GOAL if "REACHED" in status else
         C_TEXT)
    y += 6
    pygame.draw.line(surface, (30,60,80), (px+8,y), (px+PANEL_W-8,y), 1)
    y += 10

    text("— MEASURES OF EFFECTIVENESS —", font_sm, C_ACCENT)
    y += 2
    for k,v in moe.items():
        text(f"{k}", font_sm, C_TEXT)
        text(f"  {v}", font_sm, C_BRIGHT, indent=6)
        y += 1

    y += 10
    pygame.draw.line(surface, (30,60,80), (px+8,y), (px+PANEL_W-8,y), 1)
    y += 10
    text("CONTROLS", font_sm, C_ACCENT)
    for line in ["SPACE  — step once",
                 "A      — auto-run",
                 "R      — reset map",
                 "Click  — toggle obstacle",
                 "ESC/Q  — quit"]:
        text(line, font_sm, C_TEXT)

    # Legend
    y += 6
    pygame.draw.line(surface, (30,60,80), (px+8,y), (px+PANEL_W-8,y), 1)
    y += 8
    text("LEGEND", font_sm, C_ACCENT)
    legends = [
        (C_FREE,    "Free cell"),
        (C_STATIC,  "Static obstacle"),
        (C_MOVING,  "Moving obstacle"),
        (C_REPLAN,  "Replanned cells"),
        (C_PATH,    "Planned path"),
        (C_UGV,     "UGV (robot)"),
        (C_GOAL,    "Goal"),
    ]
    for color, label in legends:
        pygame.draw.rect(surface, color,
                         pygame.Rect(px+10, y, 12, 12), border_radius=2)
        s = font_sm.render(label, True, C_TEXT)
        surface.blit(s, (px+28, y))
        y += 16


# ---------------------------------------------------------------------------
# Main Simulation
# ---------------------------------------------------------------------------

def build_base_grid(seed=None):
    rng = random.Random(seed)
    return [[1 if rng.random() < STATIC_DENS else 0
             for _ in range(GRID)] for _ in range(GRID)]

def make_moe(total_steps, total_replans, total_expanded,
             path_len, straight, elapsed_ms, obs_count):
    sl = straight
    ratio = f"{path_len/sl:.4f}" if sl>0 else "N/A"
    return {
        "Steps taken":        total_steps,
        "Replans triggered":  total_replans,
        "Total cells expanded": total_expanded,
        "Travel dist (km)":   f"{path_len:.2f}",
        "Straight-line (km)": f"{sl:.2f}",
        "Optimality ratio":   ratio,
        "Replan time (ms)":   f"{elapsed_ms:.2f}",
        "Active obstacles":   obs_count,
    }

def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("UGV D* Lite — Dynamic Battlefield")
    clock  = pygame.time.Clock()

    try:
        font_big = pygame.font.SysFont("couriernew", 15, bold=True)
        font_med = pygame.font.SysFont("couriernew", 12, bold=True)
        font_sm  = pygame.font.SysFont("couriernew", 10)
    except Exception:
        font_big = font_med = font_sm = pygame.font.SysFont(None, 14)

    def reset(seed=None):
        grid  = build_base_grid(seed)
        start = (0, 0)
        goal  = (GRID-1, GRID-1)
        grid[start[0]][start[1]] = 0
        grid[goal[0]][goal[1]]   = 0

        obs_mgr = ObstacleManager(grid, start, goal, NUM_MOVING, seed)
        dstar   = DStarLite([row[:] for row in grid], start, goal)

        # Apply moving obstacles into dstar grid
        for (r,c), kind in obs_mgr.all_obstacles().items():
            dstar.update_obstacle(r, c, True)

        dstar.replan()
        path = dstar.extract_path()

        return {
            "dstar":          dstar,
            "obs_mgr":        obs_mgr,
            "ugv":            start,
            "goal":           goal,
            "path":           path or [],
            "step_n":         0,
            "replans":        1,
            "total_expanded": len(dstar.expanded_last),
            "travel_dist":    0.0,
            "last_replan_ms": 0.0,
            "status":         "READY",
            "reached":        False,
            "seed":           seed,
        }

    state = reset(seed=42)
    auto_run = False

    def do_step(state):
        if state["reached"]:
            return state

        path = state["path"]
        dstar = state["dstar"]
        obs_mgr = state["obs_mgr"]
        ugv = state["ugv"]
        goal = state["goal"]

        # 1. Move UGV one step along path (if path exists)
        moved = False
        if path and len(path) > 1:
            next_cell = path[1]
            # Check it's still free
            obs = obs_mgr.all_obstacles()
            if obs.get(next_cell) is None:
                dist = math.sqrt((ugv[0]-next_cell[0])**2 + (ugv[1]-next_cell[1])**2)
                state["travel_dist"] += dist
                dstar.move_start(next_cell)
                ugv = next_cell
                state["ugv"] = ugv
                state["step_n"] += 1
                moved = True

        if ugv == goal:
            state["reached"] = True
            state["status"]  = "REACHED GOAL!"
            state["path"]    = [ugv]
            return state

        # 2. Evolve obstacles
        changes = obs_mgr.step(ugv)
        changed = False
        for (r, c, old, new) in changes:
            is_obs = (new in ("static","moving"))
            dstar.update_obstacle(r, c, is_obs)
            changed = True

        # 3. Replan if anything changed or path was blocked
        need_replan = changed or not moved or not path
        if need_replan:
            t0 = time.perf_counter()
            dstar.replan()
            state["last_replan_ms"] = (time.perf_counter()-t0)*1000
            state["replans"]        += 1
            state["total_expanded"] += len(dstar.expanded_last)
            state["status"] = "REPLANNING..."
        else:
            state["status"] = "MOVING"

        # 4. Extract new path
        new_path = dstar.extract_path()
        state["path"] = new_path or []

        if not new_path:
            state["status"] = "NO PATH — BLOCKED"

        return state

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    running = False
                elif event.key == pygame.K_SPACE:
                    state = do_step(state)
                elif event.key == pygame.K_a:
                    auto_run = not auto_run
                elif event.key == pygame.K_r:
                    state = reset(seed=random.randint(0,9999))
                    auto_run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if mx < GRID * CELL:
                    cc = mx // CELL
                    rc = my // CELL
                    if (rc,cc) not in {state["ugv"], state["goal"]}:
                        obs = state["obs_mgr"].all_obstacles()
                        is_obs = (rc,cc) in obs
                        if is_obs:
                            state["obs_mgr"].static.discard((rc,cc))
                        else:
                            state["obs_mgr"].static.add((rc,cc))
                        state["dstar"].update_obstacle(rc, cc, not is_obs)
                        t0 = time.perf_counter()
                        state["dstar"].replan()
                        state["last_replan_ms"] = (time.perf_counter()-t0)*1000
                        state["replans"] += 1
                        state["total_expanded"] += len(state["dstar"].expanded_last)
                        state["path"] = state["dstar"].extract_path() or []

        if auto_run and not state["reached"]:
            state = do_step(state)

        # Draw
        screen.fill(C_BG)
        obs_map = state["obs_mgr"].all_obstacles()
        draw_grid(screen, state["dstar"], obs_map,
                  state["path"], state["ugv"], state["goal"],
                  state["dstar"].expanded_last)

        # Straight-line distance (from original start to goal)
        sl = math.sqrt((GRID-1)**2 + (GRID-1)**2)

        moe = make_moe(
            state["step_n"],
            state["replans"],
            state["total_expanded"],
            state["travel_dist"],
            sl,
            state["last_replan_ms"],
            len(obs_map),
        )

        draw_panel(screen, font_big, font_med, font_sm,
                   moe, state["status"], state["step_n"])

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    run()
