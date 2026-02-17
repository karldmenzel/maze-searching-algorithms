
MAZE_WIDTH = 37
MAZE_HEIGHT = 25
WALL = "O"

# coordinates: [row][col]
# [0][0]    [0][1]  [0][2] ... [0, 36]
# [1][0]    [1][1]  [1][2]
# [2][0]    [2][1]  [2][2]
# ...
# [24][0]

# The start and end are two spaces wide.
# Here we assume that we are starting and ending at the furthest out spaces.
# The path cost would be two less if we moved the start and end in.
start_position = (24, 35)
end_position = (0, 1)

# The maze, represented by an array of characters.
maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

# The list of nodes we have yet to expand, ranked by their lowest f value.
open_list = []

# The list of nodes we have already expanded.
closed_list = []

class Node:
    def __init__(self, coords, parent, f, g, h):
        self.coords = coords
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h
    def __str__(self):
        return f"{str(self.coords)}, {str(self.parent)}, {str(self.f)}"

############ Search Helper Functions ############

# Used to sort the custom Node class with Python's built-in sort function.
def compare(x):
    return x.f

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

# Takes two tuples and returns the Manhattan distance between them.
def manhattan_distance(coord1, coord2):
    return abs(coord1[0] - coord2[0]) + abs(coord1[1] - coord2[1])

# Takes a tuple representing a coordinate, and returns all valid neighbors.
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

# Takes the last node, and builds the path by checking all the parent nodes.
def built_final_path(goal_node):
    path = []
    i = goal_node
    while i.parent is not None:
        path.append(i)
        parent_node = find_node(i.parent)
        i = parent_node

    # Manually add the start node since it doesn't have a parent, but we know it has to be last.
    path.append(start_node)

    return path

############ Text Helper Functions ############

# Takes a file name and loads the maze into memory.
def import_maze(file_name):
    maze_file = open(file_name)
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH+1): # We use MAZE_WIDTH+1 because the new line character
            char_read = maze_file.read(1)
            if col == MAZE_WIDTH:
                break # Throw away the last character of the line (either a newline or an EOF)
            maze[row][col] = char_read

# Takes coordinates and returns the node in the closed list which corresponds to them.
def find_node(search_coord):
    for x in closed_list:
        if x.coords == search_coord:
            return x
    return None

# Print the maze.
def print_maze():
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH):
            print(maze[row][col], end='')
        print()

# Takes a position and marks it with a character.
def mark_position(coord, char):
    if maze[coord[0]][coord[1]] != WALL:
        maze[coord[0]][coord[1]] = char
    else:
        print("Oops, you walked into a wall!")

# Print the path on the maze, and add up the total cost.
def format_result(result_path):
    cost_of_path = 0
    for node in result_path:
        mark_position(node.coords, '*')
        cost_of_path += 1
    return cost_of_path

############ The Search ############

def a_star_search():
    while len(open_list) > 0:
        # Sort the open list so that we get the lowest f value, to expand that node next.
        open_list.sort(key=compare)
        current_node = open_list.pop(0)

        # Are we at the end? If so, return the current node so that we can construct the path by looking at the parents.
        if current_node.coords == end_position:
            return current_node

        # We are expanding the current node, so we don't need to search it again. Add it to the closed list.
        closed_list.append(current_node)

        # Get the coordinates of all valid neighbors.
        neighbors_coords = get_neighbors(current_node.coords)
        for neighbor_coords in neighbors_coords:

            # If we have already visited it, move on.
            if is_in_closed_list(neighbor_coords):
                continue

            # Since all path lengths are 1, we just increment g by 1.
            g = current_node.g + 1
            h = manhattan_distance(neighbor_coords, end_position)
            f = g + h
            neighbor_node = Node(neighbor_coords, current_node.coords, f, g, h)

            # Find if/where the neighbor is in the open list.
            list_spot = is_in_open_list(neighbor_coords)

            # If this neighbor is not in the open list, add them.
            if list_spot == -1:
                open_list.append(neighbor_node)
            else:
                # If this neighbor is in the open list, with a higher path cost, update that path cost.
                if open_list[list_spot].f > neighbor_node.f:
                    open_list[list_spot] = neighbor_node

    # If we finish searching through the open list and we have not found a solution yet, there is no solution.
    if len(open_list) > 0:
        print("No solution found")
        exit(1)
    return

############ Main Function ############

if __name__ == '__main__':
    import_maze('maze.txt')

    # Initialize the starting node, and add it to the open list..
    start_node_h = manhattan_distance(start_position, end_position)
    start_node = Node(start_position, None, start_node_h, 0, start_node_h)
    open_list.append(start_node)

    last_node = a_star_search()

    final_path = built_final_path(last_node)

    path_cost = format_result(final_path)

    print_maze()

    print(f"\nThis path cost {path_cost} moves (but could be two moves shorter it we adjusted the start and end).")
