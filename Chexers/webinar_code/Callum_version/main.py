""" main.py

"""

from state_class import *
from IDS import *

if __name__ == "__main__":
    # Initialisation
    root = State(3,3)
    IDS(root, debug=False)
