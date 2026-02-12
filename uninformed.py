import math

MAZE_WIDTH = 37
MAZE_HEIGHT = 25
WALL = "O"

start_position = (24, 35)
end_position = (0, 2)

stack = [start_position]

def uninformed_search():
    for _ in range(1000):
        current_position = stack.pop()
        # print_maze()
        # print(current_position)
        # print(stack)
        mark_position(current_position)
        if current_position == end_position:
            print("I found the end!")
            print_maze()
            return
        for coord in get_neighbors(current_position):
            stack.append(coord)

    print('Hello world from the uninformed search algorithm.')


# coordinates: [row][col]
# [0][0]    [0][1]  [0][2] ... [0, 36]
# [1][0]    [1][1]  [1][2]
# [2][0]    [2][1]  [2][2]
# ...
# [24][0]

maze = [[1] * MAZE_WIDTH for _ in range(MAZE_HEIGHT)]

def import_maze(file_name):
    print('Importing maze.')
    maze_file = open(file_name)
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH+1): # We use MAZE_WIDTH+1 because the new line character
            char_read = maze_file.read(1)
            if col == MAZE_WIDTH:
                break # Throw away the last character of the line (either a newline or an EOF)
            maze[row][col] = char_read
    print('Finished importing maze.')

def print_maze():
    for row in range(MAZE_HEIGHT):
        for col in range(MAZE_WIDTH):
            print(maze[row][col], end='')
        print()

def mark_position(coord):
    if maze[coord[0]][coord[1]] != WALL and maze[coord[0]][coord[1]] != "*":
        maze[coord[0]][coord[1]] = "*"
    else:
        print("Oops, you walked into a wall!")

def straight_line_distance(coord1, coord2):
    return math.sqrt((coord2[0] - coord1[0]) ** 2 + (coord2[1] - coord1[1]) ** 2)

def get_neighbors(coord):
    row = coord[0]
    col = coord[1]
    neighbors = []
    if col != 0 and maze[row][col - 1] != WALL and maze[row][col - 1] != "*":
        neighbors.append((row, col - 1))
    if col != MAZE_WIDTH-1 and maze[row][col + 1] != WALL and maze[row][col + 1] != "*":
        neighbors.append((row, col + 1))
    if row != 0 and maze[row - 1][col] != WALL and maze[row - 1][col] != "*":
        neighbors.append((row - 1, col))
    if row != MAZE_HEIGHT-1 and maze[row + 1][col] != WALL and maze[row + 1][col] != "*":
        neighbors.append((row + 1, col))
    return neighbors

if __name__ == '__main__':
    print('Beginning uninformed search.')
    import_maze('maze.txt')
    mark_position(start_position)
    uninformed_search()
    print('Finished uninformed search.')
