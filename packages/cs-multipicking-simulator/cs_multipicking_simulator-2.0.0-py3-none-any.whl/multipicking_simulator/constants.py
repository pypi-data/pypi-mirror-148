import json
from os.path import abspath, dirname, join, exists
from pathlib import Path

from .matching_algorithms import *


def set_data_dir(path: str):
    with open(f"{MP_SIMULATOR_ROOT_DIR}/config.json", 'r') as f:
        config = json.load(f)

    if not exists(path):
        print("Given path doesn't exist. Try again.")
    else:
        config['data_dir'] = path
        try:
            with open(f"{MP_SIMULATOR_ROOT_DIR}/config.json", 'w') as f:
                json.dump(config, f)
            print(f'MP Simulator data directory set to {path}. Please restart IPython/Notebook Kernel to implement changes.')
        except:
            print('Something went wrong...')
            raise


def get_data_dir() -> str:
    with open(f"{MP_SIMULATOR_ROOT_DIR}/config.json", 'r') as f:
        config = json.load(f)

    return config['data_dir']


# Directory constants
MP_SIMULATOR_ROOT_DIR = Path(dirname(abspath(__file__)))
DATA_DIR = get_data_dir() if get_data_dir() is not None else join(MP_SIMULATOR_ROOT_DIR, 'data')

# MPD default settings constants
DEFAULT_OP_ZONE_MP_SETTINGS = dict(
    MAX_ALLOWED_TOTAL_PRODUCTS = 50,
    MAX_DELIVERY_DISTANCES = 3000.0,
    MAX_BRANCH_TO_DELIVERY_DISTANCE = 6000.0,
    DELIVERY_SLOT_LOWER_BUFFER = 0,
    DELIVERY_SLOT_UPPER_BUFFER = 0,
    MIN_DELIVERY_SLOTS_OVERLAP = 55,
    HAS_FROZEN_PRODUCTS_CHECK = False,
    MAX_MINUTES_ALLOWED_FOR_FROZEN_PRODUCTS = 150,
    PICKING_ASSIGNABLE_WINDOW_LENGTH = 55,
    PICKING_ASSIGNABLE_LOWER_LIMIT_HEURISTIC = 60,
    SLOT_COMPATIBILITY = 15,
)

DEFAULT_MP_SIMULATOR_SETTINGS = dict(
    PROMISED_DELIVERY_TIME_SHIFT = 0,
    PICKING_ASSIGNABLE_TIME_SHIFT = 0,
    ALGORITHM = 'SORTED_DISTANCE_OLD_ORDER_MATCHER',
    EFFICIENCY_CONSTRAINT = False,
    OM_EXECUTION_LENGTH = False,
    AS_A_SERVICE = False,
    TOTAL_SAVING_LIMIT = 0,
    ANGLE_LIMIT = 180,
    INSTANCES = 1,
    NOT_MATCHED_PROBABILITY = None
)

# Matching algorithms
MATCHING_ALGORITHMS = dict(
    OLD_ORDER_MATCHER=old_order_matcher,
    SORTED_DISTANCE_OLD_ORDER_MATCHER=sorted_distance_old_order_matcher,
    SORTED_UTILITY_OLD_ORDER_MATCHER=sorted_utility_old_order_matcher,
    GUROBI_MAX_MATCHES=gurobi_max_matches,
    GUROBI_WITH_COSTS=gurobi_with_costs,
    GUROBI_INTRA_DISTANCE=gurobi_intra_distance,
    SORTED_UTILITY_OLD_ORDER_MATCHER_V2=sorted_utility_old_order_matcher_v2,
)

# Calculation constants
HAVERSINE_TO_MANHATTAN_COEFF = 1.2732