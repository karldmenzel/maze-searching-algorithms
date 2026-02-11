def uninformed_search():
    print('Hello world from the uninformed search algorithm.')

MAZE_WIDTH = 37
MAZE_HEIGHT = 25

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

if __name__ == '__main__':
    print('Beginning uninformed search.')
    import_maze('maze.txt')
    print_maze()
    uninformed_search()
    print('Finished uninformed search.')
