# Common functions to use across challenges. 

def read_text(filepath):
    """Read in a text file"""
    with open(filepath, "r") as f:
        lines_in = f.readlines()
    return(lines_in)