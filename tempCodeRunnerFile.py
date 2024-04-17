    def shortest_path(self, start, end):
        distances = [[float('inf')] * self.width for _ in range(self.height)]
        distances[start[0]][start[1]] = 0

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
                    priority_queue.put((new_dist, neighbor))

        path = [end]
        while end != start:
            for neighbor in self.get_neighbors(end):
                if distances[neighbor[0]][neighbor[1]] < distances[end[0]][end[1]]:
                    path.append(neighbor)
                    end = neighbor
                    break

        return path[::-1]