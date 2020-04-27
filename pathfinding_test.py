import sys
import pygame
from pygame.locals import *

WIDTH = 500
HEIGHT = 500
GRID_DIM = 20
SIDE_LENGTH = int(WIDTH/GRID_DIM)
SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])

# SETUP
BLUE = (25, 25, 200)
BLACK = (23, 23, 23)
WHITE = (254, 254, 254)
RED = (254, 0, 0)
GREEN = (0, 254, 0)
YELLOW = (254, 254, 0)
PINK = (254, 0, 254)
TEAL = (0, 254, 254)
# Grid will be a 50 by 50 place grid with each unit square a size of 10 by 10
fps = 10000
clock = pygame.time.Clock()
pygame.init()

SCREEN.fill(WHITE)

is_wall_clicked = False
is_start_clicked = False
is_end_clicked = False

# while animation is running all other options are not available
animation = False

main = True
# CLASSES
class Node():
    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, other):
        self.position == other.position

class grid_space():
    # start_end, 0 means normal space, 1 mean start, 2 means end
    def __init__(self, x, y, start_colour):
        self.x = x
        self.y = y
        self.colour = start_colour
        self.walkable = True
        self.changed = False

# SETUP FUNCTIONS
def grid_mouse_collision():
    mouse_pos = pygame.mouse.get_pos()
    for space in grid_spaces_list:
        if (mouse_pos[0] > space.x and mouse_pos[0] < (space.x + SIDE_LENGTH) and not space.changed
                and mouse_pos[1] > space.y and mouse_pos[1] < (space.y + SIDE_LENGTH)):
            return space
    return None

def switch_grid_walls():
    wall = grid_mouse_collision()
    if wall is not None:
        # space is curr walkable and will turn into wall
        if wall.walkable:
            wall.colour = BLACK
            wall.walkable = False
        elif not wall.walkable:
            wall.colour = WHITE
            wall.walkable = True
        wall.changed = True

def move_start_node():
    new_start = grid_mouse_collision()
    if new_start is not None:
        start_space.x = new_start.x
        start_space.y = new_start.y
        start_node.position = [new_start.x, new_start.y]


def move_end_node():
    new_start = grid_mouse_collision()
    if new_start is not None:
        end_space.x = new_start.x
        end_space.y = new_start.y
        end_node.position = [new_start.x, new_start.y]

# Checks if either start or end node is pressed
def special_node_pressed(x_pos, y_pos):
    mouse_pos = pygame.mouse.get_pos()
    if (mouse_pos[0] > x_pos and mouse_pos[0] < (x_pos + SIDE_LENGTH)
                and mouse_pos[1] > y_pos and mouse_pos[1] < (y_pos + SIDE_LENGTH)):
        return True
    return False

# ANIMATION FUNCTIONS
def check_if_walkable(node_pos):
    for spc in grid_spaces_list:
        if (spc.x == node_pos[0] and spc.y == node_pos[1] and not spc.walkable):
            return False
    return True

def highlight_space(new_space, colour):
    for space in grid_spaces_list:
        if space.x == new_space[0] and space.y == new_space[1]:
            space.colour = colour


def create_path(node):
    current_space = node
    while current_space is not None:
        highlight_space(current_space.position, YELLOW)
        current_space = current_space.parent
        pygame.display.flip()

def update_screen():
    # grid
    for space in grid_spaces_list:
        pygame.draw.rect(SCREEN, space.colour, (space.x, space.y, SIDE_LENGTH, SIDE_LENGTH))

    # start and end node
    pygame.draw.rect(SCREEN, start_space.colour,
                     (start_space.x, start_space.y, SIDE_LENGTH, SIDE_LENGTH))
    pygame.draw.rect(SCREEN, end_space.colour, (end_space.x, end_space.y, SIDE_LENGTH, SIDE_LENGTH))

    pygame.display.flip()
    pygame.time.delay(50)

def create_children(current_space):
    directions = [[SIDE_LENGTH, 0], [0, SIDE_LENGTH], [-SIDE_LENGTH, 0], [0, -SIDE_LENGTH]]
    children = []
    for direction in directions:
        new_pos = [current_space.position[0]+ direction[0],
                   current_space.position[1] + direction[1]]

        new_node = Node(current_space, new_pos)
        # New position must be within bounds of grid
        if (new_pos[0] < 0 or
                new_pos[1] < 0 or
                new_pos[0] >= WIDTH or
                new_pos[1] >= HEIGHT):
            continue
        # Check if new position is goal or a wall
        if not check_if_walkable(new_pos):
            continue

        children.append(new_node)
    return children


# Check both the current closed and open lists and add a valid space to each spot that has not been checked yet
# RETURN: new open_list, is_child_added, if_goal_found 
def add_layer(is_stuck, current_space):
    valid_spaces = []
    new_open_list = []
    temp_open_list = []
    if_goal_found = False
    # is_stuck is for when must have to add layer around all possible options
    if is_stuck:
        valid_spaces = open_list
        for closed_node in closed_list:
            valid_spaces.append(closed_node)
        temp_open_list = valid_spaces
    elif not is_stuck:
        new_open_list = open_list
        valid_spaces = [current_space]
        temp_open_list = open_list

    # Open space is the current spot and new_child is the potential child
    for open_space in valid_spaces:

        closed_list.append(open_space)
        highlight_space(open_space.position, TEAL)
        new_children = create_children(open_space)
        is_child_added = False

        for new_child in new_children:
            if (new_child.position[0] == end_space.x and new_child.position[1] == end_space.y):
                create_path(new_child)
                if_goal_found = True
                is_child_added = True
                break

            # G is the distance of the path of the parents
            new_child.g = (open_space.g + 1)
            new_child.h = ((end_node.position[0]-new_child.position[0])**2 +
                           (end_node.position[1] - new_child.position[1])**2)
            new_child.f = new_child.g + new_child.h

            print(new_child.h, "      ", open_space.h)
            if (not is_stuck and new_child.h > open_space.h
                    and open_space.position is not start_node.position):
                continue

            in_closed_list = False
            for node in closed_list:
                if new_child.position == node.position:
                    in_closed_list = True
            if in_closed_list:
                continue 

            # If the new space is already an available spot with a shorter path
            # to the starting point, replace it
            in_open_list = False
            for node in temp_open_list:
                if new_child.position == node.position:
                    if new_child.g < node.g:
                        node.g = new_child.g
                        node.parent = new_child.parent
                    else:
                        in_open_list = True
            if in_open_list:
                continue

            if is_stuck:
                highlight_space(new_child.position, PINK)
            else:
                highlight_space(new_child.position, BLUE)

            new_open_list.append(new_child)
            is_child_added = True

            update_screen()
        if if_goal_found:
            break

    return (new_open_list, is_child_added, if_goal_found)




# RESET FUNCTION
def reset():
    for space in grid_spaces_list:
        space.colour = WHITE
        space.walkable = True
    start_space.x = 25
    start_space.y = 25
    start_node.position = [25, 25]
    end_space.x = 450
    end_space.y = 450
    end_node.position = [450, 450]
    open_list.clear()
    open_list.append(start_node)
    # list of removed options/spaces
    closed_list.clear()

# Creates list of all spaces on board with their coordinates and colour
grid_spaces_list = []
for square_x in range(GRID_DIM):
    for square_y in range(GRID_DIM):
        new_space = grid_space(square_x * SIDE_LENGTH, square_y * SIDE_LENGTH, WHITE)
        grid_spaces_list.append(new_space)

# Setting initial starting and final positions
start_space = grid_space(25, 25, GREEN)
start_node = Node(None, [start_space.x, start_space.y])
end_space = grid_space(450, 450, RED)
end_node = Node(None, [end_space.x, end_space.y])

start_node.h = (abs(end_node.position[0] - start_node.position[0])**2
                + abs(end_node.position[1] - start_node.position[1])**2)
start_node.f = start_node.h
# list of possible spaces to use
open_list = []
open_list.append(start_node)
# list of removed options/spaces
closed_list = []

# MAIN LOOP
while main:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            main = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                animation = True
            elif event.key == pygame.K_RSHIFT:
                animation = False
            elif event.key == pygame.K_r:
                reset()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if special_node_pressed(start_space.x, start_space.y):
                is_start_clicked = True
            elif special_node_pressed(end_space.x, end_space.y):
                is_end_clicked = True
            else:
                is_wall_clicked = True

        elif event.type == pygame.MOUSEBUTTONUP:
            is_wall_clicked = False
            is_end_clicked = False
            is_start_clicked = False
            for space in grid_spaces_list:
                space.changed = False

    if not animation:
        # Calling collision function to change colours of grid if mouse is held down
        if is_wall_clicked:
            switch_grid_walls()
        elif is_end_clicked:
            move_end_node()
        elif is_start_clicked:
            move_start_node()

    # A_algorithm code
    elif len(open_list) != 0 and animation:
        current_node = open_list[0]
        current_index = 0
        for index, node in enumerate(open_list):
            if node.f < current_node.f:
                current_node = node
                current_index = index

        open_list.remove(current_node)

        open_list, child_added, goal_found = add_layer(False, current_node)

        if goal_found:
            animation = False
            continue

        if not child_added:
            print("RUNNN")
            print(" ")
            open_list.append(current_node)
            # Adds a layer of valid spaces to the existing ones
            open_list, child_added, goal_found = add_layer(True, None)

        if goal_found:
            animation = False


    elif len(open_list) == 0:
        print("NO PATH")
    # DRAWINGS

    update_screen()



# closed_list.append(current_node) #DONE
        # highlight_space(current_node.position, BLUE)#DONE
        # children_list = create_children(current_node)#DONE

        # # If even one of the new spaces ends up being valid and added then it will turn true
        # is_child_added = False
        # for child in children_list:
        #     if (child.position[0] == end_space.x and child.position[1] == end_space.y): #DONE
        #         create_path(child)#DONE
        #         animation = False#DONE
        #         is_child_added = True#DONE
        #         break#DONE

        #     # G is the distance of the path of the parents
        #     child.g = (current_node.g + 1)
        #     child.h = ((end_node.position[0]-child.position[0])**2 +
        #                (end_node.position[1] - child.position[1])**2)
        #     child.f = child.g + child.h

        #     # if path has to move backwards add a layer of open nodes to the current ones
        #     # run the Breadth algorithm one time around then proceed with the A* algorithm
        #     if child.h > current_node.h and current_node.position is not start_node.position: #DONE
        #         continue #DONE

        #     in_closed_list = False
        #     for node in closed_list:
        #         if child.position == node.position:
        #             in_closed_list = True
        #     if in_closed_list:
        #         continue


        #     # If the new space is already an available spot with a shorter path
        #     # to the starting point, replace it
        #     in_open_list = False
        #     for node in open_list:
        #         if child.position == node.position:
        #             if child.g <= node.g:
        #                 node.g = child.g
        #                 node.parent = child.parent
        #             else:
        #                 in_open_list = True
        #     if in_open_list:
        #         continue

        #     highlight_space(child.position, PINK)
        #     open_list.append(child)
        #     is_child_added = True