import numpy as np
import pickle
from day20 import load_data, Grid, Tile

# Load data and initialize Grid instance
tile_dict = load_data("2020/data/day20.txt")
grid = Grid(tile_dict, size=22)

# Loop to align all tiles (could also be while loop)
for k in range(0, 150):
    grid.align_tile()
    print(len(grid.tile_todo))

print(grid.grid)
# 3461, 3083, 3433, 2287

# Save object to pickle for use in second part of puzzle
f = open('day20.pkl', 'wb')
pickle.dump(grid, f)
f.close()