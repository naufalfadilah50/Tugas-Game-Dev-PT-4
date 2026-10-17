import heapq

# Peta Grid 15 x 15 dengan Bobot Medan & Rintangan
# S = Start, G = Goal, # = Wall, . = Jalan (Cost 1), ~ = Lumpur (Cost 3), ^ = Gunung (Cost 5)
MAZE_MAP = [
    ["S", ".", ".", "#", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    [".", "#", ".", "#", ".", "#", "#", "#", "#", ".", "#", "#", "#", "#", "."],
    [".", "#", ".", ".", ".", ".", "~", "~", ".", ".", ".", ".", ".", "#", "."],
    [".", "#", "#", "#", "#", ".", "#", "#", "#", "#", "#", "#", ".", "#", "."],
    [".", ".", ".", ".", "#", ".", ".", ".", ".", ".", ".", "#", ".", ".", "."],
    ["#", "#", "#", ".", "#", "#", "#", "#", "#", "#", ".", "#", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", "^", "^", "^", ".", ".", ".", ".", ".", "."],
    [".", "#", "#", "#", "#", "#", "^", "^", "^", "#", "#", "#", "#", "#", "."],
    [".", ".", ".", ".", "~", "~", "~", "~", "~", "~", "~", ".", ".", ".", "."],
    ["#", "#", "#", ".", "#", "#", "#", "#", "#", "#", ".", "#", "#", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", "#", ".", ".", ".", ".", "."],
    [".", "#", "#", "#", "#", "#", "#", "#", ".", "#", "#", "#", "#", "#", "."],
    [".", ".", ".", "~", "~", "~", ".", ".", ".", ".", ".", ".", ".", "#", "."],
    ["#", "#", ".", "#", "#", "#", "#", "#", "#", "#", "#", "#", ".", "#", "."],
    [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "G"]
]

ROWS = len(MAZE_MAP)
COLS = len(MAZE_MAP[0])

COST_MAP = {".": 1, "~": 3, "^": 5, "S": 1, "G": 1}

def get_neighbors(r, c):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < ROWS and 0 <= nc < COLS and MAZE_MAP[nr][nc] != "#":
            neighbors.append((nr, nc))
    return neighbors

def manhattan_distance(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def reconstruct_path(previous, start, goal):
    path, curr = [], goal
    while curr in previous:
        path.append(curr)
        curr = previous[curr]
    path.append(start)
    path.reverse()
    return path

# Algoritma Dijkstra
def dijkstra(start, goal):
    pq = [(0, start)]
    distances = {start: 0}
    previous = {}
    visited = set()
    nodes_explored = 0

    while pq:
        current_cost, current_node = heapq.heappop(pq)
        if current_node in visited: continue
        visited.add(current_node)
        nodes_explored += 1

        if current_node == goal: break

        for neighbor in get_neighbors(*current_node):
            step_cost = COST_MAP.get(MAZE_MAP[neighbor[0]][neighbor[1]], 1)
            new_cost = current_cost + step_cost
            if neighbor not in distances or new_cost < distances[neighbor]:
                distances[neighbor] = new_cost
                previous[neighbor] = current_node
                heapq.heappush(pq, (new_cost, neighbor))

    path = reconstruct_path(previous, start, goal) if goal in distances else []
    return path, distances.get(goal, float('inf')), nodes_explored

# Algoritma A* Search
def a_star(start, goal):
    pq = [(0 + manhattan_distance(start, goal), 0, start)]
    g_score = {start: 0}
    previous = {}
    visited = set()
    nodes_explored = 0

    while pq:
        _, current_g, current_node = heapq.heappop(pq)
        if current_node in visited: continue
        visited.add(current_node)
        nodes_explored += 1

        if current_node == goal: break

        for neighbor in get_neighbors(*current_node):
            step_cost = COST_MAP.get(MAZE_MAP[neighbor[0]][neighbor[1]], 1)
            tentative_g = current_g + step_cost
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                g_score[neighbor] = tentative_g
                previous[neighbor] = current_node
                f_score = tentative_g + manhattan_distance(neighbor, goal)
                heapq.heappush(pq, (f_score, tentative_g, neighbor))

    path = reconstruct_path(previous, start, goal) if goal in g_score else []
    return path, g_score.get(goal, float('inf')), nodes_explored

if __name__ == "__main__":
    start, goal = (0, 0), (14, 14)
    p_dij, cost_dij, exp_dij = dijkstra(start, goal)
    p_a, cost_a, exp_a = a_star(start, goal)
    
    print("=== HASIL PROGRAM PATHFINDING ===")
    print(f"Dijkstra  -> Path Cost: {cost_dij} | Nodes Explored: {exp_dij}")
    print(f"A* Search -> Path Cost: {cost_a} | Nodes Explored: {exp_a}")