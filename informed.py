import math

MAZE_WIDTH = 37
MAZE_HEIGHT = 25
WALL = "O"

start_position = (24, 35)
end_position = (0, 2)

maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

# coordinates: [row][col]
# [0][0]    [0][1]  [0][2] ... [0, 36]
# [1][0]    [1][1]  [1][2]
# [2][0]    [2][1]  [2][2]
# ...
# [24][0]

class Node:
    def __init__(self, coords, parent, f, g, h):
        self.coords = coords
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h
    def __str__(self):
        return f"{str(self.coords)}, {str(self.parent)}, {str(self.f)}"

open_list = []
closed_list = []

def search():
    while len(open_list) > 0:
        current_node = open_list.pop(0)
        print(current_node)
        neighbors = get_neighbors(current_node.coords)
        for neighbor in neighbors:
            if neighbor == end_position:
                print("Found it!")
                # TODO figure out how to end
                return
            else:
                g = current_node.g + 1
                h = straight_line_distance(neighbor, end_position)
                f = g + h
                neighbor_node = Node(neighbor, current_node, f, g, h)
                if better_route_open(neighbor_node):
                    continue
                if better_route_closed(neighbor_node):
                    continue
                open_list.append(neighbor_node)
        #         TODO sort the open_list
        closed_list.append(current_node)
    return

def better_route_open(new_node):
    for old_node in open_list:
        if old_node.coords == new_node.coords and old_node.f < new_node.f:
            return True
    return False

def better_route_closed(new_node):
    for old_node in closed_list:
        if old_node.coords == new_node.coords and old_node.f < new_node.f:
            return True
    return False

def import_maze(file_name):
    maze_file = open(file_name)
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH+1): # We use MAZE_WIDTH+1 because the new line character
            char_read = maze_file.read(1)
            if col == MAZE_WIDTH:
                break # Throw away the last character of the line (either a newline or an EOF)
            maze[row][col] = char_read

def print_maze():
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH):
            print(maze[row][col], end='')
        print()

def mark_position(coord, char):
    if maze[coord[0]][coord[1]] != WALL:
        maze[coord[0]][coord[1]] = char
    else:
        print("Oops, you walked into a wall!")

def straight_line_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

def get_neighbors(coord):
    row = coord[0]
    col = coord[1]
    neighbors = []
    if col != 0 and maze[row][col - 1] != WALL:
        neighbors.append((row, col - 1))
    if row != 0 and maze[row - 1][col] != WALL:
        neighbors.append((row - 1, col))
    if col != MAZE_WIDTH-1 and maze[row][col + 1] != WALL:
        neighbors.append((row, col + 1))
    if row != MAZE_HEIGHT-1 and maze[row + 1][col] != WALL:
        neighbors.append((row + 1, col))
    return neighbors

if __name__ == '__main__':
    import_maze('maze.txt')

    start_node_h = straight_line_distance(start_position, end_position)
    start_node = Node(start_position, None, start_node_h, 0, start_node_h) # TODO should f be 0?
    open_list.append(start_node)

    # search()
