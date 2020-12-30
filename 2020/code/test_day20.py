import numpy as np
from day20 import load_data, Grid, Tile


tile_dict = load_data("2020/data/day20test.txt")
tile_2311 = np.array(
    [
        [0, 0, 1, 1, 0, 1, 0, 0, 1, 0],
        [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
        [1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
        [1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
        [1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 1, 0, 0, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 0, 0, 1, 1, 1]
    ]
)



def test_load_data():
    assert (tile_dict[2311] == tile_2311).all()


def test_data_length():
    assert len(tile_dict) == 9


test_grid = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 3, 3],
        [0, 3, 3, 3, 3],
        [0, 0, 3, 3, 3]
    ]
)

test_coords = np.array(
    [
        (1, 2),
        (1, 3),
        (1, 4),
        (2, 1),
        (3, 0),
        (4, 1)
    ]
)

def test_get_adjacents():
    grid = Grid(tile_dict)
    grid.grid = test_grid

    assert (grid.get_adjacents() == test_coords).all()


test_edges = [
    [0, 0, 1, 1, 0, 1, 0, 0, 1, 0], # top
    [0, 0, 0, 1, 0, 1, 1, 0, 0, 1], # right
    [0, 0, 1, 1, 1, 0, 0, 1, 1, 1], # bottom
    [0, 1, 1, 1, 1, 1, 0, 0, 1, 0] # left
]

def test_get_edges_0():
    tile = Tile(1, tile_2311)
    result = [list(entry) for entry in tile.get_edges()]
    assert result == test_edges


def test_get_edges_90():
    tile = Tile(1, tile_2311)
    tile.rotation = 1

    test_edges_90 = [
        test_edges[3],
        test_edges[0],
        test_edges[1],
        test_edges[2]
    ]

    result = [list(entry) for entry in tile.get_edges()]
    assert result == test_edges_90


def test_get_edges_flipped_x():
    tile = Tile(1, tile_2311)
    tile.flip = 1 # horizontally

    test_edges_flipped = [
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 0], # top
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 1], # right
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0], # bottom
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 0] # left
    ]

    result = [list(entry) for entry in tile.get_edges()]
    assert result == test_edges_flipped
