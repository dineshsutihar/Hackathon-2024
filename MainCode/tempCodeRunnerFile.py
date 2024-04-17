 def evacuate_without_properties(self, matrix):
        for person in self.people:
            door_distances = self.calculate_distances(person, self.doors)
            nearest_door = min(self.doors, key=lambda door: door_distances[door])
            path = self.shortest_path(person, nearest_door)
            if path:
                next_step = path[1]  # Get the next step towards the nearest door
                if self.matrix[next_step[0]][next_step[1]] != 'F':  # Check if next step is not on fire
                    matrix[person[0]][person[1]] = '.'  # Change current position to empty
                    matrix[next_step[0]][next_step[1]] = 'P'  # Move person to next step
        return matrix
