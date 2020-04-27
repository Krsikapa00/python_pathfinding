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

def update_screen(fps=60):
    # grid
    for space in grid_spaces_list:
        pygame.draw.rect(SCREEN, space.colour, (space.x, space.y, SIDE_LENGTH, SIDE_LENGTH))

    # start and end node
    pygame.draw.rect(SCREEN, start_space.colour,
                     (start_space.x, start_space.y, SIDE_LENGTH, SIDE_LENGTH))
    pygame.draw.rect(SCREEN, end_space.colour, (end_space.x, end_space.y, SIDE_LENGTH, SIDE_LENGTH))
    pygame.display.flip()
    pygame.time.delay(fps)

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

def check_closed_list(child):
    for closed_node in closed_list:
        if child.position == closed_node.position:
            # if closed_node.g <= child.g:
            #     return True
            # open_list.append(closed_node)
            # closed_list.remove(closed_node)
            return True
    return False

def check_open_list(child):
    for open_node in open_list:
        if child.position == open_node.position:
            # if open_node.g > child.g:
            #     open_node.g = child.g
            #     open_node.parent = child.g
            return True
    return False

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

start_node.h = (abs(end_node.position[0] - start_node.position[0])
                + abs(end_node.position[1] - start_node.position[1]))
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
            if node.f <= current_node.f:
                current_node = node
                current_index = index
        if (current_node.position[0] == end_space.x and current_node.position[1] == end_space.y):
            create_path(current_node)
            animation = False
            continue

        open_list.remove(current_node)
        highlight_space(current_node.position, BLUE)
        children_list = create_children(current_node)

        # If even one of the new spaces ends up being valid and added then it will turn true
        for child in children_list:
            if (child.position[0] == end_space.x and child.position[1] == end_space.y):
                create_path(child)
                animation = False
                break
            # # G is the distance of the path of the parents
            child.g = (current_node.g + SIDE_LENGTH)
            child.h = ((abs(end_node.position[0]-child.position[0])) +
                       (abs(end_node.position[1] - child.position[1])))

            child.f = child.g + child.h

            if check_open_list(child):
                continue
            elif check_closed_list(child):
                continue
            else:
                highlight_space(child.position, PINK)
                open_list.append(child)
                # print(child.g, "  ", child.h, "  ", child.f)

        closed_list.append(current_node)

    elif len(open_list) == 0:
        print("NO PATH")
    # DRAWINGS

    update_screen()