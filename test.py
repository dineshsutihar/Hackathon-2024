from queue import PriorityQueue

# Symbolic representation of elements in the room
wall_symbol = '#'
door_symbol = '.'
open_space_symbol = 'os'
occupant_symbol = '0'
fire_symbol = 'f'

infinity = float('inf')

def calculate_temperature(symbol):
    if symbol == fire_symbol:
        return 1000  # High temperature for fire
    elif symbol == occupant_symbol:
        return 37  # Normal body temperature for occupant
    else:
        return 20  # Normal room temperature

def calculate_fuel_load(symbol):
    if symbol == fire_symbol:
        return 1  # High fuel load for fire
    else:
        return 0  # No fuel load for other elements

def calculate_tentative_distance(temperature, fuel_load, max_temperature_threshold, fuel_combustion_rate):
    # Calculate tentative distance based on temperature and fuel load
    if temperature > max_temperature_threshold:
        return infinity  # High temperature makes the cell unsafe
    else:
        return temperature + fuel_load * fuel_combustion_rate

def get_neighbors(row, col, rows, cols):
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < rows - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < cols - 1:
        neighbors.append((row, col + 1))
    return neighbors

def evacuate_with_properties(room_grid, start_row, start_col, exit_row, exit_col, fire_row, fire_col, max_temperature_threshold, fuel_combustion_rate):
    rows, cols = len(room_grid), len(room_grid[0])
    
    # Initialize distances and visited flags
    distances = [[infinity] * cols for _ in range(rows)]
    distances[start_row][start_col] = 0
    visited = [[False] * cols for _ in range(rows)]
    
    # Initialize priority queue
    priority_queue = PriorityQueue()
    priority_queue.put((0, (start_row, start_col)))
    
    # Dijkstra's Algorithm
    while not priority_queue.empty():
        _, current_cell = priority_queue.get()
        current_row, current_col = current_cell
        
        if current_row == exit_row and current_col == exit_col:
            break
        
        visited[current_row][current_col] = True
        
        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col, rows, cols):
            if not visited[neighbor_row][neighbor_col]:
                symbol = room_grid[neighbor_row][neighbor_col]
                temperature = calculate_temperature(symbol)
                fuel_load = calculate_fuel_load(symbol)
                
                # Calculate tentative distance considering temperature and fuel load
                tentative_distance = calculate_tentative_distance(temperature, fuel_load, max_temperature_threshold, fuel_combustion_rate)
                
                if tentative_distance < distances[neighbor_row][neighbor_col]:
                    distances[neighbor_row][neighbor_col] = tentative_distance
                    priority_queue.put((tentative_distance, (neighbor_row, neighbor_col)))
    
    # Backtrack to construct safest path
    current_row, current_col = exit_row, exit_col
    safest_path = []
    while current_row != start_row or current_col != start_col:
        safest_path.append((current_row, current_col))
        min_distance = infinity
        next_cell = None
        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col, rows, cols):
            if distances[neighbor_row][neighbor_col] < min_distance:
                min_distance = distances[neighbor_row][neighbor_col]
                next_cell = (neighbor_row, neighbor_col)
        current_row, current_col = next_cell
    
    safest_path.append((start_row, start_col))
    safest_path.reverse()
    return safest_path

# Example usage
rows = 10
cols = 10
start_row, start_col = 0, 0
exit_row, exit_col = 9, 9
fire_row, fire_col = 5, 5
max_temperature_threshold = 100
fuel_combustion_rate = 0.1

room_grid = [
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'f', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', 'os', 'os', 'os', 'os', 'os', 'os', 'os', 'os', '#'],
    ['#', '#', '#', '#', '#', '#', '#', '#', '#', '#']
]

safest_path = evacuate_with_properties(room_grid, start_row, start_col, exit_row, exit_col, fire_row, fire_col, max_temperature_threshold, fuel_combustion_rate)
print("Safest path:", safest_path)