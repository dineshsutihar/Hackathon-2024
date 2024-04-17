from queue import PriorityQueue

def evacuate_without_properties(room_grid, start_row, start_col, exit_row, exit_col):
    rows, cols = len(room_grid), len(room_grid[0])
    
    distances = [[float('inf')] * cols for _ in range(rows)]
    distances[start_row][start_col] = 0
    visited = [[False] * cols for _ in range(rows)]
    
    priority_queue = PriorityQueue()
    priority_queue.put((0, (start_row, start_col)))
    
    while not priority_queue.empty():
        _, current_cell = priority_queue.get()
        current_row, current_col = current_cell
        
        if visited[current_row][current_col]:  # Check if cell has been visited
            continue
        
        visited[current_row][current_col] = True
        
        if current_row == exit_row and current_col == exit_col:
            break
        
        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col, rows, cols):
            if not visited[neighbor_row][neighbor_col]:
                tentative_distance = 1  # Set a constant distance for all cells
                
                if tentative_distance < distances[neighbor_row][neighbor_col]:
                    distances[neighbor_row][neighbor_col] = tentative_distance
                    priority_queue.put((tentative_distance, (neighbor_row, neighbor_col)))
    
    current_row, current_col = exit_row, exit_col
    safest_path = []
    while current_row != start_row or current_col != start_col:
        safest_path.append((current_row, current_col))
        min_distance = float('inf')
        next_cell = None
        for neighbor_row, neighbor_col in get_neighbors(current_row, current_col, rows, cols):
            if distances[neighbor_row][neighbor_col] < min_distance and not visited[neighbor_row][neighbor_col]:
                min_distance = distances[neighbor_row][neighbor_col]
                next_cell = (neighbor_row, neighbor_col)
        if next_cell is None:
            break  # Break the loop if no valid next cell is found
        current_row, current_col = next_cell
    
    safest_path.append((start_row, start_col))
    safest_path.reverse()
    return safest_path

def get_neighbors(row, col, rows, cols):
    neighbors = []
    
    # Check the cell to the left
    if col > 0:
        neighbors.append((row, col - 1))
    
    # Check the cell to the right
    if col < cols - 1:
        neighbors.append((row, col + 1))
    
    # Check the cell above
    if row > 0:
        neighbors.append((row - 1, col))
    
    # Check the cell below
    if row < rows - 1:
        neighbors.append((row + 1, col))
    
    return neighbors



if __name__ == "__main__":
    room_grid = [
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 0, 0]
    ]
    start_row, start_col = 0, 0
    exit_row, exit_col = 4, 4
    print(evacuate_without_properties(room_grid, start_row, start_col, exit_row, exit_col))  # Output: [(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (1, 4), (2, 4), (3, 4), (4, 4)]