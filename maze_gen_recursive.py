# This code is basn http://arcade.academy/examples/maze_recursive.html
#
# Modified by CS1527 Course Team on 30 January 2019
#
#

import random
from monster import FighterMonster, ThiefMonster, GamerMonster
from goblin import WealthGoblin, HealthGoblin, GamerGoblin


SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700

TILE_EMPTY = 0
TILE_CRATE = 1

# Maze must have an ODD number of rows and columns.
# Walls go on EVEN rows/columns.
# Openings go on ODD rows/columns
MAZE_HEIGHT = 51
MAZE_WIDTH = 51

def create_empty_grid(width, height, default_value=TILE_EMPTY):
    """ Create an empty grid. """
    grid = []
    for row in range(height):
        grid.append([])
        for column in range(width):
            grid[row].append(default_value)
    return grid


def create_outside_walls(maze):
    """ Create outside border walls."""

    # Create left and right walls
    for row in range(len(maze)):
        maze[row][0] = TILE_CRATE
        maze[row][len(maze[row]) - 1] = TILE_CRATE

    # Create top and bottom walls
    for column in range(1, len(maze[0]) - 1):
        maze[0][column] = TILE_CRATE
        maze[len(maze) - 1][column] = TILE_CRATE


def make_maze_recursive_call(maze, top, bottom, left, right):
    """
    Recursive function to divide up the maze in four sections
    and create three gaps.
    Walls can only go on even numbered rows/columns.
    Gaps can only go on odd numbered rows/columns.
    Maze must have an ODD number of rows and columns.
    """

    # Figure out where to divide horizontally
    start_range = bottom + 2
    end_range = top - 1
    y = random.randrange(start_range, end_range, 2)

    # Do the division
    for column in range(left + 1, right):
        maze[y][column] = TILE_CRATE

    # Figure out where to divide vertically
    start_range = left + 2
    end_range = right - 1
    x = random.randrange(start_range, end_range, 2)

    # Do the division
    for row in range(bottom + 1, top):
        maze[row][x] = TILE_CRATE

    # Now we'll make a gap on 3 of the 4 walls.
    # Figure out which wall does NOT get a gap.
    wall = random.randrange(4)
    if wall != 0:
        gap = random.randrange(left + 1, x, 2)
        maze[y][gap] = TILE_EMPTY

    if wall != 1:
        gap = random.randrange(x + 1, right, 2)
        maze[y][gap] = TILE_EMPTY

    if wall != 2:
        gap = random.randrange(bottom + 1, y, 2)
        maze[gap][x] = TILE_EMPTY

    if wall != 3:
        gap = random.randrange(y + 1, top, 2)
        maze[gap][x] = TILE_EMPTY

    # If there's enough space, to a recursive call.
    if top > y + 3 and x > left + 3:
        make_maze_recursive_call(maze, top, y, left, x)

    if top > y + 3 and x + 3 < right:
        make_maze_recursive_call(maze, top, y, x, right)

    if bottom + 3 < y and x + 3 < right:
        make_maze_recursive_call(maze, y, bottom, x, right)

    if bottom + 3 < y and x > left + 3:
        make_maze_recursive_call(maze, y, bottom, left, x)


def make_maze_recursion(maze_width, maze_height):
    """ Make the maze by recursively splitting it into four rooms. """
    maze = create_empty_grid(maze_width, maze_height)
    # Fill in the outside walls
    create_outside_walls(maze)

    # Start the recursive process
    make_maze_recursive_call(maze, maze_height - 1, 0, 0, maze_width - 1)
    # add_goblin_monster(maze)
    return add_goblin_monster(maze)


def print_maze(maze, wall="#", space="-", hero="H", goblin="G", monster="M"):
    """print out the maze in the terminal"""
    for row in maze:
        row_str = str(row)
        row_str = row_str.replace("1", wall)    # replace the wall character
        row_str = row_str.replace("0", space)   # replace the space character
        print("".join(row_str))


def add_goblin_monster(maze):  # Adding Goblins and Monsters to the maze recursively
    counter = 0

    while counter != 10:
        rand_row = random.randint(1, len(maze) - 2)
        rand_col = random.randint(1, len(maze[rand_row]) - 2)

        while maze[rand_row][rand_col] != 0:
            # Continue as long as don't find a 0 in the maze
            # I found this to be the most efficient way to ensure that there won't be an infinite loop
            list_row = random.sample(range(1, len(maze) - 1), len(maze) - 2)  # Generate a list of unique random numbers for the row
            list_col = random.sample(range(1, len(maze[rand_row]) - 1), len(maze[rand_row]) - 2)    # Generate a list of unique random numbers for the col
            try:    # using error catching because I need to break two for loops at the same time
                for y in list_row:
                    for x in list_col:
                        if maze[y][x] == 0:
                            rand_col = x
                            rand_row = y
                            raise IndexError    # again raising exception just to break out of loop
            except IndexError:
                continue

        if counter < 5:
            creature_type = random.randint(1, 3)
            if creature_type == 1:
                FighterMonster(rand_col, rand_row)
            elif creature_type == 2:
                ThiefMonster(rand_col, rand_row)
            else:
                GamerMonster(rand_col, rand_row)
                
            maze[rand_row][rand_col] = 4    # Adding Monsters
        else:
            creature_type = random.randint(1, 3)
            if creature_type == 1:
                WealthGoblin(rand_col, rand_row)
            elif creature_type == 2:
                HealthGoblin(rand_col, rand_row)
            else:
                GamerGoblin(rand_col, rand_row)

            maze[rand_row][rand_col] = 3    # Adding Goblins

        counter += 1

    # return monsters, goblins, maze
    return maze

if __name__ == "__main__":
    maze = make_maze_recursion(7, 7)
    print_maze(maze)
    print(maze,"#", "-")
    print(maze[2][1])
    print(maze[1][2])
    print(maze[3][2])
    print(maze[2][3])
