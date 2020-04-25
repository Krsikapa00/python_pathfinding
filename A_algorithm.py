import numpy as np
import matplotlib.pyplot as plt



class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0

def printGrid(updated_grid):
    for i in range(len(updated_grid)):
        print(updated_grid[i])


grid_width = 10
grid_height = 10
grid = []
# fills the empty grid with 1's to start
for x in range(grid_width):
    grid.append([])
    for y in range(grid_height):
        grid[x].append(1)

# OBSTACLES FOR TESTINGS



start = [7,7]
start_node = Node(None,start)
end = [9,9]
end_node = Node(None,end)

# list of possible spaces to use
open_list = []
# list of removed options/spaces
closed_list = []

open_list.append(start_node)

def create_path(node):
    current_node = node 
    while current_node is not None:
        pos = current_node.position
        grid[pos[0]][pos[1]] = 2
        current_node = current_node.parent
    printGrid(grid)

while len(open_list) != 0:
    
    current_node = open_list[0]
    current_index = 0
    for index, node in enumerate(open_list):
        if node.f <= current_node.f:
            current_node = node
            current_index = index
    open_list.remove(current_node)
    closed_list.append(current_node.position)

    if current_node.position == end:
        create_path(current_node)
        print(current_node.position)
        break

    directions = [[1,0],[0,1],[-1,0],[0,-1]]
    for direction in directions:
        new_pos = [current_node.position[0]+ direction[0], current_node.position[1] + direction[1]]

        # New position must be within bounds of grid
        if (new_pos[0] < 0 or 
            new_pos[1] < 0 or 
            new_pos[0] >= grid_width or 
            new_pos[1] >= grid_height):
            continue

        # check if new position is standable (Standable when value on grid is 1)
        if (grid[new_pos[0]][new_pos[1]] != 1):
            continue

        new_node = Node(current_node, new_pos)

        new_node.g = abs(new_pos[0] - start[0]) + abs(new_pos[1] - start[1])
        new_node.h = (end[0]-new_pos[0])**2 + (end[1] - new_pos[1])**2
        new_node.f = new_node.g + new_node.h

        valid_new_node = False
        if new_node.position not in closed_list:
            valid_new_node = True
            for node in open_list:
                if new_node.position == node.position:
                    valid_new_node = False
                    break

        if valid_new_node == True:
            open_list.append(new_node)
    
    if len(open_list) == 0:
        print("NO PATH")
    # for node in open_list:
    #     print(node.position)
    # print(" ")

    