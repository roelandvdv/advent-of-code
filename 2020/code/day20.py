import numpy as np

# TODO: make expanding grid, so approach the coordinates differently
# TODO: use lookups of edges instead of brute force, should be much faster. needs only eight entries per tile

def load_data(filename = "2020/data/day20test.txt"):
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


class Grid():
    """
    Main class for grid.
    """
    def __init__(self, tile_dict, size=5):
        self.tile_dict = tile_dict
        self.size = size
        self.grid = np.zeros((size, size))
        self.tile_todo = [] # list of ids
        self.tiles = {} #contains all tiles as id: object dictionary

        self.prepare()


    def prepare(self):
        """Called on init of grid object."""

        # Create tile todo
        self.tile_todo = list(self.tile_dict.keys())

        # Create all tile objects and put in tiles dict
        for tile_id in self.tile_todo:
            self.tiles[tile_id] = Tile(tile_id, self.tile_dict[tile_id])

        # Select a tile id
        first_tile_id = self.tile_todo.pop(0)

        # Update grid with new tile
        start_coordinates = (int(np.floor(self.size/2)), int(np.floor(self.size/2)))
        new_grid = self.grid
        new_grid[start_coordinates] = first_tile_id
        self.grid = new_grid


    def align_tile(self):
        """Try to align new tile.
        
        Currently it goes through all tiles per coordinate, which is
        fast at first but slower later.
        
        Going through all coordinates per tile should be faster later.
        """

        if self.tile_todo:
            # Select an available position
            success = False
            adjacent_coords_list = self.get_adjacents()
            for coords in adjacent_coords_list:

                # Get list of neighbouring tiles to that position. These are fixed.
                fixed_tiles_list = self.get_neighbours(coords)

                # Try all tiles in todo. Not always success for every coordinate because of edges.
                for tile_id in self.tile_todo:
                    success = self.try_orientations(tile_id, coords, fixed_tiles_list)
                    if success:
                        break
                
                # Break to recalculate adjacent_coords_list.
                if success:
                    # Update grid
                    self.grid[coords[0], coords[1]] = tile_id
                    # Update todo
                    self.tile_todo.remove(tile_id)
                    break

        return None


    def try_orientations(self, id0, coords0, fixed_tiles_list):
        """Try all orientations of id0 and see if it matches with fixed list."""
        tile_object = self.tiles[id0]
        for rotation in [0, 1, 2, 3]:
            for flip in [0, 1, 2, 3]:
                tile_object.set_orientation(rotation, flip)
                success = all([self.is_match(fixed_tile_ids, id0, coords0) for fixed_tile_ids in fixed_tiles_list])
                if success:
                    return True # orientation is still set correctly


    def align_all(self):
        print(self.grid)
        k = 0
        while self.tile_todo and k < 100:
            self.align_tile()
            print(self.grid)
            print(self.tile_todo)
            print(k)
            k += 1


    def get_coords(self, id):
        """Get coordines of tile from grid, by id."""
        coords = np.argwhere(self.grid == id)
        assert len(coords) == 1
        return coords[0] # numpy array


    def get_object(self, id):
        """Returns object by id."""
        return self.tiles[id]


    def get_adjacents(self):
        """
        Get all adjacents positions.
        Use gradient for edge detection.
        https://stackoverflow.com/questions/32334322/find-adjacent-elements-in-a-2d-numpy-grid

        TODO: consider most interesting positions first?
        """
        dy, dx = np.gradient(self.grid)
        edges_x = np.abs(dx) > 0
        edges_y = np.abs(dy) > 0
        neighbour_array = (edges_x | edges_y) & ~(self.grid > 0)
        coords = np.argwhere(neighbour_array)
        return coords


    def get_neighbours(self, id_coord: tuple):
        """
        Get existing neighbours to specific tile position
        id: tuple
        """
        grid = self.grid
        id_list = [
            grid[id_coord[0] - 1, id_coord[1]],
            grid[id_coord[0] + 1, id_coord[1]],
            grid[id_coord[0], id_coord[1] - 1],
            grid[id_coord[0], id_coord[1] + 1]
        ]
        return [id for id in id_list if id != 0]


    def is_match(self, id0, id1, test_coords):
        """
        Check whether the edges of two adjacent ids match.
        
        1. find orientation (four posibilities)
        2. select correct edges for each case
        3. compare edges
        """
        coords0 = self.get_coords(id0)
        coords1 = test_coords
        i1 = coords0[0]
        j1 = coords0[1]
        i2 = coords1[0]
        j2 = coords1[1]

        edges0 = self.get_object(id0).get_edges() # top, right, bottom, left
        edges1 = self.get_object(id1).get_edges()

        if (i2 == i1 + 1) & (j2 == j1): # 2nd is below
            return (edges0[2] == edges1[0]).all()
        if (i2 == i1 - 1) & (j2 == j1): # 2nd is above
            return (edges0[0] == edges1[2]).all()
        if (i2 == i1) & (j2 == j1 + 1): # 2nd is right
            return (edges0[1] == edges1[3]).all()
        if (i2 == i1) & (j2 == j1 - 1): # 2nd is left
            return (edges0[3] == edges1[1]).all()
        return False


class Tile():
    """
    Main class for tile.
    """
    def __init__(self, tile_id, tile_data):
        self.tile_id = tile_id
        self.rotation = 0 # 0,1,2,3 (clockwise)
        self.flip = 0 # 0, 1, 2, 3 (0 = none, 1 = left-right, 2 = up-down, 3 = both)
        self.tile_data = tile_data


    def set_orientation(self, rotation, flip):
        self.rotation = rotation
        self.flip = flip


    def get_tile_data(self):
        tile_data = np.rot90(self.tile_data, -self.rotation)

        if self.flip in [1, 3]:
            tile_data = np.fliplr(tile_data)
        if self.flip in [2, 3]:
            tile_data = np.flipud(tile_data)
        if self.flip == 3:
            tile_data = np.flip(tile_data)
        return tile_data

    
    def get_tile_data_without_edges(self):
        tile_data = self.get_tile_data()
        return tile_data[1:-1, 1:-1]


    def get_edges(self):
        """Return edges in certain order. top, right, bottom, left.
        First rotation, then flip.
        """
        tile_data = self.get_tile_data()

        list_of_edges = [
            tile_data[0,:], # top
            tile_data[:,-1], # right
            tile_data[-1,:], # bottom
            tile_data[:,0] # left
        ]
        return list_of_edges # numpy array
