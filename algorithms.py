from data_structures import Queue


def bfs_traverse(graph, start, target):  # Time Complexity: O(V + E), classic BFS

    if start == target:
        return [start]

    if (start not in graph) or (target not in graph):
        return None

    visited   = set()
    queue  = Queue()
    queue.enqueue(start)
    visited.add(start)
    parent   = {start: None}

    while not queue.is_empty():
        current = queue.dequeue()

        for neighbor in graph.get(current, []):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.enqueue(neighbor)

                if neighbor == target:
                    path = []
                    node = target
                    while node is not None:
                        path.append(node)
                        node = parent[node]
                    return path[::-1]

    return None


def greedy_select(items, score_func, maximize=True, tie_breaker=None):   # Time Complexity: O(n)
    if not items:
        return [] if tie_breaker is None else None

    best_score = None
    best_items = []

    for item in items:
        score = score_func(item)

        if best_score is None:
            is_better = True
        elif maximize:
            is_better = score > best_score
        else:
            is_better = score <  best_score

        if is_better:
            best_score = score
            best_items = [item]
        elif score == best_score:
            best_items.append(item)

    if tie_breaker and best_items:
        return tie_breaker(best_items)

    return best_items