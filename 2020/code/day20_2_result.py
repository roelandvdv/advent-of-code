import numpy as np
import pickle
import matplotlib.pyplot as plt
from day20 import load_data

# Load grid object from previous, also has children list with tile data
# grid.grid for numpy array with IDs
# grid.tiles for list of children
f = open('2020/code/day20.pkl', 'rb')
grid = pickle.load(f)
f.close()

# Find indices where tiles are located in grid (necessary because it's padded with zeros)
indices = np.argwhere(grid.grid)

# Initialize image to be filled with tiles without borders (so 8 instead of 10 size)
N = 8
mins = np.min(indices, axis=0)
maxs = np.max(indices, axis=0)
image0 = np.zeros(N*(maxs - mins + 1)).astype(int)

# Iterate over tile IDs and place tile data in correct position
for row, col in indices:
    row0 = row - mins[0]
    col0 = col - mins[1]
    tile_id = int(grid.grid[row, col])
    sub_image = grid.tiles[tile_id].get_tile_data_without_edges()
    image0[(N*row0):(N*row0+N), (N*col0):(N*col0+N)] = sub_image

#plt.imshow(image0)
#plt.show()

# Load test image
#image0 = load_data("2020/data/day20test2.txt")[0]

# Load template
template = load_data("2020/data/day20monster.txt")[0]

# Function to flip or rotate image (could also be done for template instead)
def orient_image(image, rotation:int, flip:int):
    image = np.rot90(image, -rotation)
    if flip in [1, 3]:
        image = np.fliplr(image)
    if flip in [2, 3]:
        image = np.flipud(image)
    if flip == 3:
        image = np.flip(image)
    return image

# Iterate over orientations
counts = []
for rotation in [0, 1, 2, 3]: # duplicate combinations here
    for flip in [0, 1, 2, 3]:
        image = orient_image(image0, rotation, flip)
        shape = np.shape(image)
        
        # Iterate over row, cols and match template to part of image
        k = 0
        for r in range(0, shape[0]-3):
            for c in range(0, shape[1]-20):
                result = np.logical_or(
                    np.logical_and(image[r:(r+3), c:(c+20)], template),
                    np.logical_not(template)
                ).all()
                if result:
                    print("Monster found!")
                    print(rotation, flip)
                    k += 1
        counts.append(k)

print(counts)
answer = np.count_nonzero(image) - np.max(counts) * np.count_nonzero(template)
print(answer)