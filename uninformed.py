import math

def uninformed_search():
    print('Hello world from the uninformed search algorithm.')

MAZE_WIDTH = 37
MAZE_HEIGHT = 25

start_position = (24, 35)
end_position = (0, 2)

# [row][col]
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

def mark_position(row, col):
    if maze[row][col] != "O":
        maze[row][col] = "*"
    else:
        print("Oops, you walked into a wall!")

def straight_line_distance(row1, col1, row2, col2):
    return math.sqrt((row2 - row1) ** 2 + (col2 - col1) ** 2)

if __name__ == '__main__':
    print('Beginning uninformed search.')
    import_maze('maze.txt')
    print_maze()
    uninformed_search()
    mark_position(start_position[0], start_position[1])
    print_maze()
    print('Finished uninformed search.')
