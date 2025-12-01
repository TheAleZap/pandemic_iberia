import random
from algorithms import greedy_select
from board import bfs_shortest_path


def choose_starting_city_for_cpu(game_state, player):   # Time Complexity: O(H)
    """
    Here, we pick a starting city for the CPU using a simple scoring heuristic.
    Our CPU prefers 3‑cube cities, while also avoiding clashing with Player 1's color.
    """
    board = game_state.board
    
    p1 = game_state.players[0]
    p1_color = None
    if p1.location:
        p1_color = board.get_city_color(p1.location)
    
    def score_city(city, avoid_color):   # Time Complexity: O(1)
        color = board.get_city_color(city)
        cubes = board.get_cube_count(city, color)
        
        is_port = board.is_port_city(city)
        score   = 0
        
        if cubes == 3:
            score += 100
        if is_port:
            score += 10
        if avoid_color and color == avoid_color:
            score -= 1000
        return score
    
    best_candidates = greedy_select(
        player.hand,
        score_func = lambda city: score_city(city, p1_color),
        maximize   = True,
        tie_breaker = random.choice,
    )
    
    return best_candidates


def calculate_movement_cost(board, current_city, target_city):   # Time Complexity: O(V + E)
    """
    Returns (cost, path) for the cheapest known way to move between two cities.
    Cost here is expressed in number of actions, not edge count.
    """
    if current_city == target_city:
        return (0, [current_city])
    if board.is_port_city(current_city) and board.is_port_city(target_city):
        return (1, [current_city, target_city])
    
    rr_graph = board.get_railroad_graph()
    if rr_graph:
        path = bfs_shortest_path(rr_graph, current_city, target_city)
        if path:
            return (1, path)
    
    full_graph = board.CITY_CONNECTIONS
    path = bfs_shortest_path(full_graph, current_city, target_city)
    if path:
        cost = len(path) - 1
        return (cost, path)
    return None

def can_reach_in_moves(board, current_city, target_city, max_moves):   # Time Complexity: O(V + E)
    """Convenience wrapper: can we get there in <= max_moves?"""
    result = calculate_movement_cost(board, current_city, target_city)
    if result is None:
        return (False, None, None)
    
    cost, path = result
    return (cost <= max_moves, cost, path)


def get_next_step_towards_target(board, current_city, target_city):   # Time Complexity: O(V + E)
    """
    Returns the very next hop along a shortest path toward target,
    or None if no valid movement exists.
    """
    result = calculate_movement_cost(board, current_city, target_city)
    if result is None:
        return None
    cost, path = result
    if len(path) < 2:
        return None 
    return path[1]

def is_city_connected_by_railroad(board, city): # Time Complexity: O(V + E) where V = number of cities, E = number of edges
    rr_graph = board.get_railroad_graph()
    neighbors = rr_graph.get(city, [])
    return len(neighbors) > 0

def find_research_target_with_check(board, player, game_state): # Time Complexity: O(H + D)
    counts = {}
    for color in board.DISEASE_COLORS:
        counts[color] = 0
    
    for card in player.hand:
        color = board.get_city_color(card)
        if color in counts:
            counts[color] += 1
    
    options = []
    for color, count in counts.items():
        if count >= 5:
            if color in board.hospitals:
                if color not in game_state.cured_diseases:
                    options.append((color, board.hospitals[color]))
    
    if len(options) > 0:
        return random.choice(options)
    return None, None

def find_hospital_build_target_prioritized(board, player, current_city): # Time Complexity: O(H × (V + E))
    port_cities_with_cost = []
    railroad_cities_with_cost = []
    
    for card in player.hand:
        city = card
        color = board.get_city_color(city)
        if not color:
            continue
        if color in board.hospitals:
            continue
        
        result = calculate_movement_cost(board, current_city, city)
        if result is None:
            continue
        
        cost, _ = result
        if cost > 3:
            continue
        
        if board.is_port_city(city):
            port_cities_with_cost.append((city, cost))
        elif is_city_connected_by_railroad(board, city):
            railroad_cities_with_cost.append((city, cost))
    
    if port_cities_with_cost:
        best_port = min(port_cities_with_cost, key=lambda x: x[1])
        return best_port[0]
    
    if railroad_cities_with_cost:
        best_rr = min(railroad_cities_with_cost, key=lambda x: x[1])
        return best_rr[0]
    
    return None

def find_three_cube_target_with_cost(board, current_city, max_moves=3): # Time Complexity: O(V + T × (V + E))
    targets = set()
    for city in board.cities:
        for color in board.DISEASE_COLORS:
            if board.get_cube_count(city, color) == 3:
                targets.add(city)
                break
    
    if current_city in targets:
        targets.remove(current_city)
    if not targets:
        return (None, None)
    
    reachable = []
    for city in targets:
        can_reach, cost, _ = can_reach_in_moves(board, current_city, city, max_moves)
        if can_reach:
            reachable.append((city, cost))
    if not reachable:
        return (None, None)
    best = min(reachable, key=lambda x: x[1])
    return best
def choose_cpu_action(game_state, player): # Time Complexity: O((H + V) × (V + E))
    board = game_state.board
    current = player.location

    if player.cpu_committed_plan is not None:
        plan = player.cpu_committed_plan
        target = plan["target"]
        
        plan_valid = True
        if plan["final_action"] == "treat":
            city_color = board.get_city_color(target)
            if city_color != plan["color"] or board.get_cube_count(target, plan["color"]) != 3:
                plan_valid = False
        elif plan["final_action"] == "research":
            research_color, research_city = find_research_target_with_check(board, player, game_state)
            if research_color != plan["color"] or research_city != target:
                plan_valid = False
        elif plan["final_action"] == "build_hospital":
            target_color = board.get_city_color(target)
            if target_color in board.hospitals or target not in player.hand:
                plan_valid = False
        
        if not plan_valid:
            player.cpu_committed_plan = None
        else:
            if current == target:
                if plan["final_action"] == "treat":
                    player.cpu_committed_plan = None
                    return ("treat", plan["color"])
                elif plan["final_action"] == "research":
                    player.cpu_committed_plan = None
                    return ("research", plan["color"])
                elif plan["final_action"] == "build_hospital":
                    player.cpu_committed_plan = None
                    return ("build_hospital", target)
            else:
                next_step = get_next_step_towards_target(board, current, target)
                if next_step:
                    return ("move", next_step)
                else:
                    player.cpu_committed_plan = None

    if not getattr(player, "cpu_first_action_done", False):
        player.cpu_first_action_done = True
        city_color = board.get_city_color(current)
        if city_color and city_color not in board.hospitals:
            if current in player.hand:
                return ("build_hospital", current)
        if city_color:
            cubes = board.get_cube_count(current, city_color)
            if cubes == 3:
                return ("treat", city_color)

    actions_remaining = player.actions_remaining
    
    research_color, research_city = find_research_target_with_check(board, player, game_state)
    if research_color and research_city:
        if current == research_city:
            return ("research", research_color)
        else:
            player.cpu_committed_plan = {
                "type": "move_to_research",
                "target": research_city,
                "final_action": "research",
                "color": research_color
            }
            next_step = get_next_step_towards_target(board, current, research_city)
            if next_step:
                return ("move", next_step)
    
    hospital_city = find_hospital_build_target_prioritized(board, player, current)
    if hospital_city:
        if current == hospital_city:
            return ("build_hospital", hospital_city)
        else:
            player.cpu_committed_plan = {
                "type": "move_to_build_hospital",
                "target": hospital_city,
                "final_action": "build_hospital"
            }
            next_step = get_next_step_towards_target(board, current, hospital_city)
            if next_step:
                return ("move", next_step)
    
    target, cost = find_three_cube_target_with_cost(board, current, actions_remaining - 1)
    if target:
        if current == target:
            city_color = board.get_city_color(target)
            if city_color and board.get_cube_count(target, city_color) == 3:
                return ("treat", city_color)
        else:
            city_color = board.get_city_color(target)
            player.cpu_committed_plan = {
                "type": "move_to_treat_3cube",
                "target": target,
                "final_action": "treat",
                "color": city_color
            }
            next_step = get_next_step_towards_target(board, current, target)
            if next_step:
                return ("move", next_step)
            else:
                player.cpu_committed_plan = None
    
    valid_hospital_cities = []
    for card in player.hand:
        city = card
        color = board.get_city_color(city)
        if color and color not in board.hospitals:
            result = calculate_movement_cost(board, current, city)
            if result:
                cost, _ = result
                valid_hospital_cities.append((city, cost))
    
    if valid_hospital_cities:
        port_railroad = [c for c in valid_hospital_cities if board.is_port_city(c[0]) or is_city_connected_by_railroad(board, c[0])]
        if port_railroad:
            best = min(port_railroad, key=lambda x: x[1])
        else:
            best = min(valid_hospital_cities, key=lambda x: x[1])
        
        target_city = best[0]
        if current == target_city:
            return ("build_hospital", target_city)
        else:
            player.cpu_committed_plan = {
                "type": "move_to_build_hospital",
                "target": target_city,
                "final_action": "build_hospital"
            }
            next_step = get_next_step_towards_target(board, current, target_city)
            if next_step:
                return ("move", next_step) 
    
    target, cost = find_three_cube_target_with_cost(board, current, 999)
    if target:
        city_color = board.get_city_color(target)
        player.cpu_committed_plan = {
            "type": "move_to_treat_3cube",
            "target": target,
            "final_action": "treat",
            "color": city_color
        }
        next_step = get_next_step_towards_target(board, current, target)
        if next_step:
            return ("move", next_step)
    
    neighbors = board.get_neighbors(current)
    if neighbors:
        return ("move", random.choice(neighbors))
    
    if board.is_port_city(current):
        port_cities = [city for city in board.PORT_CITIES if city != current]
        if port_cities:
            return ("move", random.choice(port_cities))
    
    return ("skip", None)