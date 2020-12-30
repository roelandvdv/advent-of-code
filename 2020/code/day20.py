# Load data
import numpy as np

def load_data(filename = "2020/data/day20test.txt"): # = 
    with open(filename, "r") as f:
        input = f.read()

    tiles = input.split("\n\n")

    tile_dict = {}
    for tile in tiles:
        lines = tile.split("\n")
        tile_id = int(lines[0].split(" ")[1][:-1])
        tile_data = np.array(
            [[int(character.replace(".", "0").replace("#", "1")) for character in line] for line in lines[1:]]
        )
        tile_dict[tile_id] = tile_data
    return tile_dict

tile_dict = load_data("2020/data/day20test.txt")


    # total image can be flipped and rotated, so some degrees of freedom

# data structure:
# - ids, full arrays
#OR
# - ids, top, right, left, bottom line (rotation, flip)

# - grid with IDs

id_list = list(tile_dict.keys())

#grid[m,n] = doing
#get_available_edges(m,n)

# Grid Class
# Tile Class (wth method to return edges, etc.)

# prepare
# put one ID on grid
# recalculate grid todo list (list of all neighbouring positions)
# update tile todo list (remove tile id, tile object)
# start
# select any position in grid todo list (iterate over them)
# get edges that must match, together with their position
#   - get neighbouring IDs
#   - get left side of right ID from dict, etc.
# find matching ID with rotation and flip by (itertools?)
# - iterate over IDs
#       - iterate over edges/rotation (4)
#           - iterate over flip (4)
# for every step, match 1-4 edges (right=right, top=top, etc.)
# if match:
# - update grid with id
# - update dict with rotation and flip (???)
#       - do it by actually flipping/rotating (or reordering lists)
# - update grid todo list
# - update tile todo list
# if no match:
# - put id to back of todo_list
# break if tile todo list is empty


class Grid():
    """
    Main class for grid.
    """
    def __init__(self, tile_dict):
        self.tile_dict = tile_dict
        
        self.grid = np.zeros((5, 5))
        self.tile_todo = [] # list of ids
        self.grid_todo = [] # necessary, or calculate on the fly?

        self.tiles = [] # children?

        self.prepare()

    def prepare(self):

        # create tile todo
        self.tile_todo = list(self.tile_dict.keys())

        # update grid and tile todo
        start_coordinates = (2, 2)
        new_grid = self.grid
        new_grid[start_coordinates] = self.tile_todo.pop(0)
        new_grid[(3,3)] = self.tile_todo.pop(0)
        self.grid = new_grid

        # create first tile object

        # create grid todo
        self.grid_todo = self.get_adjacents()

    def get_adjacents(self):
        """
        Get all adjacents positions.
        Use gradient for edge detection.
        https://stackoverflow.com/questions/32334322/find-adjacent-elements-in-a-2d-numpy-grid
        """
        dy, dx = np.gradient(self.grid)
        edges_x = np.abs(dx) > 0
        edges_y = np.abs(dy) > 0
        neighbour_array = (edges_x | edges_y) & ~(self.grid > 0)
        coords = np.argwhere(neighbour_array)
        return coords

    def get_neighbours(self, id):
        """
        Get adjacents to specific tile id
        """
        return True


class Tile():
    """
    Main class for tile.

    needs id or not?
    """
    def __init__(self, tile_id, tile_data):
        self.tile_id = tile_id
        self.rotation = 0 # 0,1,2,3 (clockwise)
        self.flip = 0 # 0, 1, 2, 3 (0 = none, 1 = horizontally, 2 = vertically, 3 = both)
        self.tile_data = tile_data

    def set_orientation(self, rotation, flip):
        self.rotation = rotation
        self.flip = flip

    def get_edges(self):
        """Return edges in certain order. top, right, bottom, left.
        First rotation, then flip.
        
        Do this with numpy instead, just rotate and flip tile data?"""

        flip_x = self.flip in [1, 3]
        flip_y = self.flip in [2, 3]

        list_of_edges = [
            self.tile_data[0,:], # top
            self.tile_data[:,-1], # right
            self.tile_data[-1,:], # bottom
            self.tile_data[:,0] # left
        ]

        list_of_edges_rotated = list_of_edges[(4 - self.rotation):] + list_of_edges[:(4 - self.rotation)]
        list_of_edges_rotated_and_flipped = list_of_edges_rotated.copy()
        if flip_x:
            list_of_edges_rotated_and_flipped[0] = list_of_edges_rotated[0][::-1]
            list_of_edges_rotated_and_flipped[2] = list_of_edges_rotated[2][::-1]
        if flip_y:
            list_of_edges_rotated_and_flipped[1] = list_of_edges_rotated[1][::-1]
            list_of_edges_rotated_and_flipped[3] = list_of_edges_rotated[3][::-1]
        if flip_x & flip_y:
            list_of_edges_rotated_and_flipped = [edge[::-1] for edge in list_of_edges_rotated]
        
        return list_of_edges_rotated_and_flipped





#############

def get_available_edges(grid, coords):
    """
    Return list of positions that are empty.
    Order: top, bottom, left, right

    """
    neighbors = [
        grid[coords[0] - 1, coords[1]] == 0,
        grid[coords[0] + 1, coords[1]] == 0,
        grid[coords[0], coords[1] - 1] == 0,
        grid[coords[0], coords[1] + 1] == 0,
    ]
    return neighbors

###############

grid = np.zeros((5, 5))
grid[1,2] = 1
grid[4, 2] = 4
print(grid)
m, n = 2, 2

get_available_edges(grid, (m, n))