
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
start_position = (24, 35)
end_position = (0, 1)

maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

# Depth first search is NOT OPTIMAL and is heavily dependent on the order in which nodes are expanded.
# As a result, the paths have strange blocks, where the search made a "snake" pattern.
def depth_first_search(current_node, history):
    if current_node in history:
        return None # We have already visited this node, no need to check it again
    history.append(current_node)
    if current_node == end_position:
        return history
    neighbors = get_neighbors(current_node)
    if neighbors is None or len(neighbors) == 0:
        history.pop() # This node has no neighbors, so cannot be the goal, so remove it
        return None
    for neighbor in neighbors:
        potential_path = depth_first_search(neighbor, history)
        if potential_path is not None and len(potential_path) > 0:
            return potential_path
    history.pop() # This node is not the goal, and none of its neighbors are, so remove this node
    return None

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

def format_result(result_path):
    if result_path is None or len(result_path) == 0:
        print("No solution found")
        exit(1)

    for index, pos in enumerate(result_path):
        mark_position(pos, '*')

if __name__ == '__main__':
    import_maze('maze.txt')

    path = depth_first_search(start_position, [])

    format_result(path)

    print_maze()
