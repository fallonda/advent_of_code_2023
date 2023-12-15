from src.utils import read_in_as_array
import numpy as np
from math import ceil
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from importlib import reload
import src.day_10.funcs
reload(src.day_10.funcs)
from src.day_10.funcs import pad_array, Animal
from skimage.segmentation import flood_fill

# First example. 
example = read_in_as_array("./src/day_10/example.txt")
example = np.array([[y for y in x] for x in example])
padded_eg = pad_array(example)        
example_animal = Animal(padded_eg)
example_animal.first_move()
example_animal.move_until_end()
example_animal.correct_edges()
example_animal.create_binary_maze()
example_animal.binary_maze
# Find unique internal spaces for flood filling. 
example_animal.get_seeds()

# Second example
example_2 = read_in_as_array("./src/day_10/example_2.txt")
example_2 = np.array([[y for y in x] for x in example_2])
padded_eg_2 = pad_array(example_2)

ex_2 = Animal(padded_eg_2)
ex_2.run_all(dir=1)
ex_2.fill_tile_types()

# Full input
full_input = read_in_as_array("./src/day_10/full_input.txt")
full_input = np.array([[y for y in x] for x in full_input])
pd_full_input = pad_array(full_input)

fi = Animal(pd_full_input)
fi.run_all(dir = 1)
len(fi.get_seeds())

w_start_shown = fi.binary_maze.copy()
w_start_shown[fi.start_pos] = 2
w_start_shown[fi.edges[-1]] = 3
plt.imshow(w_start_shown)
plt.show()

filled = w_start_shown.copy()
for i in fi.unique_rhs:
    filled = flood_fill(filled, i, 4)
    
plt.imshow(filled)
plt.show()

# Internal area:
print((filled == 4).sum())





