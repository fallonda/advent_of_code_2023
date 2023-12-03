from src.utils import read_text
import numpy as np


def read_in_as_array(path):
    """Reads text file in and converts it to a 1d
    numpy array."""
    file_in = read_text(path)
    as_array = np.loadtxt(
        file_in,
        dtype = "str",
        comments = None
    )
    return as_array