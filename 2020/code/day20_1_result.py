import numpy as np
from day20 import load_data, Grid, Tile

tile_dict = load_data("2020/data/day20.txt")
grid = Grid(tile_dict, size=22)
for k in range(0, 150): # debugging is slow
    grid.align_tile()
    print(len(grid.tile_todo))

print(grid.grid)

# 3461, 3083, 3433, 2287