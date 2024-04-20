# main.py
import random
import networkx as nx
from Room import Room
from Edge import Edge
from dijkstra import dijkstra
import asyncio
from combo import FireSimulator
import multiprocessing

# Create a new Graph object
G = nx.Graph()

# Create Room objects
rooms = [Room(f"F{i//5+1}-{i%5+1}", False, i//5, i in [0, 4], room_size=30, no_of_doorsandexits=random.randint(1, 2), people_position=[random.randint(0, 30), random.randint(0, 30)], is_wallflamable=False) for i in range(30)]  # Emergency exits are only at rooms "F1-1" and "F1-5"

# Create Edge objects
edges = [Edge(f"F{i//5+1}-{i%5+1}", f"F{(i+1)//5+1}-{(i+1)%5+1}", random.randint(1, 10)) for i in range(29)]  # Connect each room to the next one

# Add ladders between the first and third rooms of each floor and the corresponding rooms of the next floor
for i in range(0, 25, 5):
    edges.append(Edge(f"F{i//5+1}-1", f"{(i+5)//5+1}-1", random.randint(1, 10)))  # Ladder between first rooms
    if i+2 < 25:  # To avoid index out of range for the last floor
        edges.append(Edge(f"F{i//5+1}-3", f"{(i+5)//5+1}-3", random.randint(1, 10)))  # Ladder between third rooms

# Add nodes and edges to the graph
for room in rooms:
    G.add_node(room.room_number, is_fire=room.is_fire, floor_number=room.floor_number, is_emergency_exit=room.is_emergency_exit)
for edge in edges:
    G.add_edge(edge.source, edge.destination, weight=edge.weight)

# Define source room that is the room where the evacuation starts
source_room = "F4-1"

emergency_exit_rooms = [room.room_number for room in rooms if room.is_emergency_exit]

# Room layout matrix

# Initialize building layout matrix
global matrix
matrix= [
    ['#', '#', '#', '#', '#', '#', '#', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', 'F', 'F', '.', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '.', '.', '.', '.', 'P', '.', '#'],
    ['#', '.', '.', '.', '.', '.', '.', '#'],
    ['#', '#', '#', '#', 'DE', '#', '#', '#']
]
# simulator = FireSimulator(matrix)
# asyncio.run(simulator.ignite_fire())

# Run Dijkstra's algorithm
shortest_path, sum_of_weight = dijkstra(G, source_room, emergency_exit_rooms)

# Output results
print("Shortest path to emergency exits:", shortest_path) 
print("Sum of weights along the shortest path:", sum_of_weight)
