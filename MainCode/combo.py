import asyncio
from queue import PriorityQueue


class FireSimulator:
    def __init__(self, matrix, fire_interval=1, spread_interval=1):
        self.matrix = matrix
        self.fire_interval = fire_interval
        self.spread_interval = spread_interval
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.on_fire = set()
        self.escaped = False
        self.people = {(y, x) for y in range(self.height) for x in range(self.width) if self.matrix[y][x] == 'P'}
        self.doors = {(y, x) for y in range(self.height) for x in range(self.width) if self.matrix[y][x] == 'DE'}
        self.safe_people = set()

    async def ignite_fire(self):
        while not self.escaped:
            await asyncio.sleep(self.fire_interval)
            for y in range(self.height):
                for x in range(self.width):
                    if self.matrix[y][x] == 'F':
                        self.on_fire.add((y, x))
            self.print_state()
            await self.spread_fire()
            self.matrix = self.evacuate_without_properties(self.matrix)  # Add this line
            self.print_state()

            # Check if 'F' has reached all '#'
            if all(self.matrix[y][x] == 'F' for y in range(self.height) for x in range(self.width) if self.matrix[y][x] == '#'):
                break

            while True:
                # Your existing code here...

                # Check if 'P' has reached 'DE'
                if any(self.matrix[y][x] == 'DE' for y in range(self.height) for x in range(self.width) if self.matrix[y][x] == 'P'):
                    # Replace 'DE' with 'P'
                    for y in range(self.height):
                        for x in range(self.width):
                            if self.matrix[y][x] == 'DE':
                                self.matrix[y][x] = 'P'
                    return  # Stop the async method

                if not self.people or self.on_fire == {(y, x) for y in range(self.height) for x in range(self.width)}:
                    break

        # After fire is extinguished, initiate evacuation
        self.matrix = self.evacuate_without_properties(self.matrix)
        self.print_state()

    async def spread_fire(self):
        while not self.escaped:
            await asyncio.sleep(self.spread_interval)
            next_fire = set()
            for y in range(self.height):
                for x in range(self.width):
                    if (y, x) in self.on_fire:
                        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                            ny, nx = y + dy, x + dx
                            if 0 <= ny < self.height and 0 <= nx < self.width:
                                if self.matrix[ny][nx] == '.':
                                    next_fire.add((ny, nx))
                                elif self.matrix[ny][nx] == 'DE':
                                    self.escaped = True
            self.on_fire |= next_fire
            self.print_state()
            self.matrix = self.evacuate_without_properties(self.matrix)  # Add this line
            self.print_state()
            if not self.people or self.on_fire == {(y, x) for y in range(self.height) for x in range(self.width)}:
                self.escaped = True

        # After fire is extinguished, initiate evacuation
        self.matrix = self.evacuate_without_properties(self.matrix)
        self.print_state()

    def print_state(self):
        for y in range(self.height):
            for x in range(self.width):
                if (y, x) in self.on_fire:
                    print('F', end=' ')
                else:
                    print(self.matrix[y][x], end=' ')
            print()
        print()

    def evacuate_without_properties(self, matrix):
        for person in self.people:
            door_distances = self.calculate_distances(person, self.doors)
            nearest_door = min(self.doors, key=lambda door: door_distances[door])
            path = self.shortest_path(person, nearest_door)
            if path and len(path) > 1:  # Check if path exists and has at least two elements
                next_step = path[1]  # Get the next step towards the nearest door
                if self.matrix[next_step[0]][next_step[1]] != 'F':  # Check if next step is not on fire
                    matrix[person[0]][person[1]] = '.'  # Change current position to empty
                    matrix[next_step[0]][next_step[1]] = 'P'  # Move person to next step
                    self.people.remove(person)
                    self.people.add(next_step)
                    if next_step in self.doors:  # Check if person has reached a door
                        self.escaped = True  # Stop the simulation
        return matrix


    def calculate_distances(self, start, targets):
        distances = {target: float('inf') for target in targets}
        distances[start] = 0

        priority_queue = PriorityQueue()
        priority_queue.put((0, start))

        while not priority_queue.empty():
            dist, current = priority_queue.get()
            if current in targets:
                distances[current] = dist
            for neighbor in self.get_neighbors(current):
                new_dist = dist + 1
                if self.matrix[neighbor[0]][neighbor[1]] == 'F':  # If the cell is on fire
                    new_dist += 1000  # Add a high cost to the distance
                if neighbor in distances and new_dist < distances[neighbor]:
                    distances[neighbor] = new_dist
                    priority_queue.put((new_dist, neighbor))

        return distances

    def shortest_path(self, start, end):
        distances = [[float('inf')] * self.width for _ in range(self.height)]
        distances[start[0]][start[1]] = 0
        previous_cells = [[None] * self.width for _ in range(self.height)]

        priority_queue = PriorityQueue()
        priority_queue.put((0, start))

        while not priority_queue.empty():
            dist, current = priority_queue.get()
            if current == end:
                break
            for neighbor in self.get_neighbors(current):
                new_dist = dist + 1
                if new_dist < distances[neighbor[0]][neighbor[1]]:
                    distances[neighbor[0]][neighbor[1]] = new_dist
                    previous_cells[neighbor[0]][neighbor[1]] = current
                    priority_queue.put((new_dist, neighbor))

        # Reconstruct the path from end to start
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_cells[current[0]][current[1]]
        path.reverse()

        return path

    def get_neighbors(self, cell):
        y, x = cell
        neighbors = []
        for dy, dx in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < self.height and 0 <= nx < self.width:
                neighbors.append((ny, nx))
        return neighbors
    


# if __name__ == '__main__':
#     # Example usage
#     matrix = [
#         ['#', '#', '#', '#', '#', '#', 'DE','#','#', '#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.', '#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.','#'],
#         ['#', '.', '.', '.', '.', '.', 'P','.','.','#'],
#         ['#', '.', '.', '.', '.', '.', '.', '.','.','#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.', '#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.', '#'],
#         ['#', '.', '.', 'F', 'F', '.', '.','.','.', '#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.', '#'],
#         ['#', '.', '.', '.', '.', '.', '.','.','.', '#'],
#         ['#', '#', '#', '#', '#', '#', '#','#','#', '#']
#     ]

#     simulator = FireSimulator(matrix)
#     asyncio.run(simulator.ignite_fire())
