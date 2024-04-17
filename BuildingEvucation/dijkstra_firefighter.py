from heapq import heappop, heappush


def dijkstra_firefighter(graph, source, fire_rooms):
    distances = {node: float('inf') for node in graph.nodes}
    distances[source] = 0
    previous = {node: None for node in graph.nodes}
    visited = set()
    
    queue = [(0, source)]

    while queue:
        current_distance, current_node = heappop(queue)

        if current_node in visited:
            continue

        visited.add(current_node)

        if current_node in fire_rooms:
            return construct_path(previous, current_node), distances[current_node]

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor]['weight']
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heappush(queue, (distance, neighbor))

    return None, None

def construct_path(previous, target):
    path = []  # Initialize the path list
    current_node = target  # Start from the target node
    while current_node is not None:  # While we haven't reached the source node
        path.insert(0, current_node)  # Insert the current node at the beginning of the path list
        current_node = previous[current_node]  # Move to the previous node in the path
    return path  # Return the path list