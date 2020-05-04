from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

class Queue():
    def __init__(self):
        self.queue = []
    def enqueue(self, value):
        self.queue.append(value)
    def dequeue(self):
        if self.size() > 0:
            return self.queue.pop(0)
        else:
            return None
    def size(self):
        return len(self.queue)
# First pass solution: 
# Record the room in visited
# Get all the exits with the room.
# Move in one direction, add this to the traversal path and pop it off the directions associated with the room
# Work out the opposite direction and add this to a reverse path so that backtracking is possible and remove the opposite direction from the unexplored paths
# Get exits for the new room and keep note of this (in visited)
# Move in a random direction again and add to the traversal path and pop it off the possible directions
# Keep moving until you reach a dead end
# When there are no more unexplored exits - backtrack along the last direction on the backtracked path and remove it from the backtracked path and add it to the traversal path
# Check that room for unexplored directions and repeat the process again
# This keeps going until the number of rooms visited reaches the length of the rooms graph

# Fill this out with directions to walk
# traversal_Path = ['n', 'n']
traversal_Path = [ ]

opposites = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

previous_room = [None]

room_queue = {}
visited = {}

def check_direction(roomId):
    directions = []
    if 'n' in room_graph[roomId][1].keys():
        directions.append('n')
    if 'e' in room_graph[roomId][1].keys():
        directions.append('e')
    if 's' in room_graph[roomId][1].keys():
        directions.append('s')
    if 'w' in room_graph[roomId][1].keys():
        directions.append('w')
    return directions

while len(visited) < len(room_graph):
    room_id = player.current_room.id
    if room_id not in room_queue:
        visited[room_id] = room_id
        room_queue[room_id] = check_direction(room_id)
    
    if len(room_queue[room_id]) < 1:
        previous_direction = previous_room.pop()
        traversal_Path.append(previous_direction)
        player.travel(previous_direction)
    
    else:
        next_direction = room_queue[room_id].pop(0)
        traversal_Path.append(next_direction)
        previous_room.append(opposites[next_direction])
        player.travel(next_direction)



# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_Path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_Path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")





# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_Path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_Path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")