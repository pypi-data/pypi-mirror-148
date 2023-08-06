"""
Cornershop by Uber - Dispatcher Ops Research

Multipicking Simulator
"""

from . import extract
from .constants import set_data_dir, get_data_dir
from . import constants
from .run.run_utils import simulation
from . import analyze

DATA_DIR = get_data_dir()

if DATA_DIR is not None:
    print(f"Multipicking Dispatcher Simulator Data directory set to {DATA_DIR}.")
else:
    print("Data directory not set. Please set the Data directory in your machine calling the 'set_data_dir(dir_path)' function before using the Simulator.")