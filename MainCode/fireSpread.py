import asyncio

class FireSimulator:
    def __init__(self, matrix, fire_interval=1, spread_interval=1):
        self.matrix = matrix
        self.fire_interval = fire_interval
        self.spread_interval = spread_interval
        self.height = len(matrix)
        self.width = len(matrix[0])
        self.on_fire = set()
        self.escaped = False
    
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
    
    async def ignite_fire(self):
        while not self.escaped:
            await asyncio.sleep(self.fire_interval)
            for y in range(self.height):
                for x in range(self.width):
                    if self.matrix[y][x] == 'F':
                        self.on_fire.add((y, x))
            self.print_state()
            await self.spread_fire()
    
    def print_state(self):
        for y in range(self.height):
            for x in range(self.width):
                if (y, x) in self.on_fire:
                    print('F', end=' ')
                else:
                    print(self.matrix[y][x], end=' ')
            print()
        print()


if __name__ == '__main__':
    # Example usage
    matrix = [
        ['#', '#', '#', '#', '#', '#', '#', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '#'],
        ['#', '.', '.', 'F', 'F', '.', '.', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '#'],
        ['#', '.', '.', '.', '.', '.', '.', '#'],
        ['#', '#', '#', '#', 'DE', '#', '#', '#']
    ]

    simulator = FireSimulator(matrix)
    asyncio.run(simulator.ignite_fire())
