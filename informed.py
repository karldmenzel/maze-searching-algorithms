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

def compare(x):
    return x.f

def search():
    while len(open_list) > 0:
        # Sort the open list so that we get the lowest f value
        open_list.sort(key=compare)
        current_node = open_list.pop(0)

        # Are we at the end? If so great
        if current_node.coords == end_position:
            print("Found it!")
            return current_node

        # We are expanding the current node, so we don't need to search it again
        closed_list.append(current_node)

        neighbors_coords = get_neighbors(current_node.coords)
        for neighbor_coords in neighbors_coords:
            if is_in_closed_list(neighbor_coords):
                continue

            g = current_node.g + 1
            h = manhattan_distance(neighbor_coords, end_position)
            f = g + h
            neighbor_node = Node(neighbor_coords, current_node.coords, f, g, h)

            list_spot = is_in_open_list(neighbor_coords)
            if list_spot == -1:
                open_list.append(neighbor_node)
            else:
                open_list[list_spot] = neighbor_node
    if len(open_list) > 0:
        print("No solution found")
    return

def is_in_closed_list(x):
    for closed_node in closed_list:
        if x == closed_node.coords:
            return True
    return False

def is_in_open_list(x):
    for index, open_node in enumerate(open_list):
        if x == open_node.coords:
            return index
    return -1

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

def manhattan_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

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

def find_node(search_coord):
    for x in closed_list:
        if x.coords == search_coord:
            return x
    return None

if __name__ == '__main__':
    import_maze('maze.txt')

    start_node_h = manhattan_distance(start_position, end_position)
    start_node = Node(start_position, None, start_node_h, 0, start_node_h)
    open_list.append(start_node)

    last_node = search()

    path = []
    i = last_node
    while i.parent is not None:
        path.append(i)
        parent_node = find_node(i.parent)
        i = parent_node

    path.append(start_node)

    for node in path:
        mark_position(node.coords, '*')

    print_maze()