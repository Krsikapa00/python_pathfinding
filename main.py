import numpy as np
import matplotlib.pyplot as plt

class Node():
    def __init__ (self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
        


found = False
# Variables for grid dimensions
grid_width = 10
grid_height = 10
grid = []
# fills the empty grid with 1's to start
for x in range(grid_width):
    grid.append([])
    for y in range(grid_height):
        grid[x].append(1)

start = [3,2]
start_node = Node(None,start)
end = [3,3]
end_node = Node(None,end)

grid[start[0]][start[1]] = "S"
grid[end[0]][end[1]] = "E"
dist_from_start = 0
current_pos_list = []
next_pos_list = []
current_pos_list.append(start_node)


def printGrid(updated_grid):
    for i in range(len(updated_grid)):
        print(updated_grid[i])


# creates list of possible new positions based on where current node is
def create_new_positions(current_pos):
    dir = [[0,1],[1,0],[0,-1],[-1,0]]
    list_of_children = []

    for dir_change in dir:

        possible_child_pos = (current_pos.position[0] + dir_change[0], current_pos.position[1] + dir_change[1])
        
        # New position must be within bounds of grid
        if (possible_child_pos[0] < 0 or 
            possible_child_pos[1] < 0 or 
            possible_child_pos[0] >= grid_width or 
            possible_child_pos[1] >= grid_height):
            continue

        # check if new position is standable (Standable when value on grid is 1)
        if (grid[possible_child_pos[0]][possible_child_pos[1]] != 1):
            continue

        new_child = Node(current_pos,possible_child_pos)
        list_of_children.append(new_child)

    return list_of_children

# Loop until end is found. For now loop 6 times to cover entire 5x5 grid
while (found == False):

    for cur_pos in current_pos_list:
        # print(cur_pos)
        new_positions = create_new_positions(cur_pos)

        for pos in new_positions:
            grid[pos[0]][pos[1]] = dist_from_start + 1
            next_pos_list.append(pos)

    if len(next_pos_list) == 0:
        break

    current_pos_list = next_pos_list
    next_pos_list = []
    # print(new_positions)
    printGrid(grid)
    print("")
    dist_from_start += 1

import sys
import pygame
from pygame.locals import *


# SETUP CONSTANTS AND GLOBAL VARIABLES
WIDTH = 
HEIGHT = 

# OBJECTS


fps = 
clock = pygame.time.Clock()
pygame.init()
SCREEN = pygame.display.set_mode(['WIDTH', 'HEIGHT'])
main = True

# MAIN LOOP
while main:


#HANDLE EVENTS
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           pygame.quit()
           sys.exit()
           main = False

#LOGIC

#DRAWINGS: (first screen fill then layer everything else)


#UPDATE SCREEN
   pygame.display.flip()


#LIMIT FRAMES PER SECOND
   clock.tick(fps)