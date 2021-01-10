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


def test_grid_pepare():
    test_grid = np.array(
        [
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 2311, 0, 0],
            [0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0]
        ]
    )

    grid = Grid(tile_dict)
    assert (grid.grid == test_grid).all()


test_grid = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 3, 4, 5],
        [0, 7, 6, 8, 9],
        [0, 0, 10, 11, 12]
    ]
)


def test_get_coords():
    grid = Grid(tile_dict)
    grid.grid = test_grid

    assert (grid.get_coords(6) == [3, 2]).all()


def test_get_adjacents():
    grid = Grid(tile_dict)
    grid.grid = test_grid

    adjacents = np.array(
        [
            (1, 2),
            (1, 3),
            (1, 4),
            (2, 1),
            (3, 0),
            (4, 1)
        ]
    )

    assert (grid.get_adjacents() == adjacents).all()


def test_get_neighbours():
    grid = Grid(tile_dict)
    grid.grid = test_grid

    test_coord = (2, 1)
    neighbours = np.array(
        [
            (2, 2),
            (3, 1)
        ]
    )
    neighbours = [3, 7]
    assert grid.get_neighbours(test_coord).sort() == neighbours.sort()


def test_get_tile_data_without_edges():
    tile = Tile(1, tile_2311)

    tile_2311_without_edges = np.array(
        [
            [1, 0, 0, 1, 0, 0, 0, 0],
            [0, 0, 0, 1, 1, 0, 0, 1],
            [1, 1, 1, 0, 1, 0, 0, 0],
            [1, 0, 1, 1, 0, 1, 1, 1],
            [1, 0, 0, 0, 1, 0, 1, 1],
            [1, 0, 1, 0, 1, 0, 0, 1],
            [0, 1, 0, 0, 0, 0, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 1],
        ]
    )

    assert (tile.get_tile_data_without_edges() == tile_2311_without_edges).all()


def test_get_tile_data_without_edges_90():
    tile = Tile(1, tile_2311)
    tile.rotation = 1

    tile_2311_without_edges_90 = np.array(
        [
            [1, 0, 1, 1, 1, 1, 0, 1],
            [1, 1, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 1, 0, 1, 1],
            [0, 0, 1, 1, 0, 1, 1, 0],
            [1, 0, 0, 0, 1, 0, 0, 0],
            [0, 1, 0, 1, 1, 0, 0, 0],
            [1, 0, 1, 1, 1, 0, 1, 0]
        ]
    )

    assert (tile.get_tile_data_without_edges() == tile_2311_without_edges_90).all()


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
        test_edges[3][::-1],
        test_edges[0],
        test_edges[1][::-1],
        test_edges[2]
    ]

    result = [list(entry) for entry in tile.get_edges()]
    assert result == test_edges_90


def test_get_edges_flipped_x():
    tile = Tile(1, tile_2311)
    tile.flip = 1 # horizontally

    test_edges_flipped = [
        [0, 1, 0, 0, 1, 0, 1, 1, 0, 0], # top
        [0, 1, 1, 1, 1, 1, 0, 0, 1, 0], # left > right
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 0], # bottom
        [0, 0, 0, 1, 0, 1, 1, 0, 0, 1], # right > left
    ]

    result = [list(entry) for entry in tile.get_edges()]
    assert result == test_edges_flipped


def test_is_match_0():
    """Place two tiles and test whether the edges match."""
    test_grid = np.array(
        [
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 3, 1],
            [0, 2, 6, 8],
        ]
    )

    tile_3 = np.array(
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
    tile_6 = np.array(
        [
            [0, 0, 1, 1, 1, 0, 0, 1, 1, 1],
            [1, 1, 0, 0, 1, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 1, 1, 0, 0, 1, 0],
            [1, 1, 1, 1, 0, 1, 0, 0, 0, 1],
            [1, 1, 0, 1, 1, 0, 1, 1, 1, 0],
            [1, 1, 0, 0, 0, 1, 0, 1, 1, 1],
            [0, 1, 0, 1, 0, 1, 0, 0, 1, 1],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [1, 1, 1, 0, 0, 0, 1, 0, 1, 0],
            [1, 0, 1, 1, 1, 0, 0, 1, 1, 1]
        ]
    )

    grid = Grid(tile_dict)
    grid.grid = test_grid
    tiles = {
        3: Tile(3, tile_3),
        6: Tile(6, tile_6)
    }
    grid.tiles = tiles
    assert grid.is_match(3, 6, (3, 2))
    

test_tile_dict = {
    1: np.array(
        [
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [1, 1, 1, 1],
            [0, 0, 1, 0]
        ]
    ),
    2: np.array(
        [
            [1, 1, 1, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]
        ]
    )
}


result_grid = np.array(
    [
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 2, 1, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]
)


def test_align_tile():
    grid = Grid(test_tile_dict)
    grid.align_tile()
    assert (grid.grid == result_grid).all()


def test_align_all():
    grid = Grid(test_tile_dict)
    grid.align_all()
    assert (grid.grid == result_grid).all()
