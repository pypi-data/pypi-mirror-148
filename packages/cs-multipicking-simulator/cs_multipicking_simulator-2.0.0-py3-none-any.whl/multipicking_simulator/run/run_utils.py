import os
import pickle
from datetime import date, datetime, timedelta
from itertools import combinations
from json import loads
from math import asin, cos, radians, sin, sqrt
from typing import Any, Dict, Iterable, List, Set, Tuple

import numpy as np
import pandas as pd
import requests
import requests.exceptions
from multipicking_simulator.extract.data_extraction_queries import \
    opzone_mp_settings_parameter_query
from multipicking_simulator.extract.data_extraction_utils import (dump_pickle,
                                                        load_pickle,
                                                        query_to_table)
from requests import post
from shapely import wkt
from shapely.geometry import Point

from .. import constants

MP_SIMULATOR_ROOT_DIR = constants.MP_SIMULATOR_ROOT_DIR
DATA_DIR = constants.DATA_DIR

pre_url = "http://localhost:8501"
pre_url_capacity = "http://estimator-model:8501"

# NOTE: REMEMBER THAT 'localhost' HAS TO BE CHANGED TO 'estimator-model' for capacity team simulator

def simulation(simulation_values: Dict[Any, Any]) -> str:
    """
    Simulate an operational day with the given simulation parameters.
    """
    ###############################
    # STEP 1: FETCH REQUIRED DATA #
    ###############################

    zone_id = simulation_values['zone_id']
    date = simulation_values['date']

    # Get simulation parameters
    non_geo_params = get_simulation_non_geo_parameters(simulation_values)
    geo_params, geo_opzone_df = get_simulation_geo_parameters(simulation_values)

    matching_algorithm = constants.MATCHING_ALGORITHMS[non_geo_params["ALGORITHM"]]

    print(f"Zone ID: {zone_id} | Date: {date} | OM exec. length set: {non_geo_params['OM_EXECUTION_LENGTH']} | Algorithm: {non_geo_params['ALGORITHM']} | Instances: {non_geo_params['INSTANCES']}")

    if non_geo_params['CONVERSION_BY_HOUR'] is None and non_geo_params['NOT_MATCHED_PROBABILITY'] is None:
        print("Simulation failed: At least one of CONVERSION_BY_HOUR or NOT_MATCHED_PROBABILITY must be given.")
        return

    # Get order data
    feasible_orders = fetch_feasible_orders(
        zone_id,
        date,
        non_geo_params['PROMISED_DELIVERY_TIME_SHIFT'],
        non_geo_params['PICKING_ASSIGNABLE_TIME_SHIFT'],
        geo_opzone_df,
    )

    # Get OrderMatcher execution data
    om_execution_times = get_om_execution_times(
            zone_id=zone_id,
            date=date,
            step_in_seconds=non_geo_params["OM_EXECUTION_LENGTH"]
        )

    orders_dict = feasible_orders.set_index('order_id').to_dict(orient='index')

    # Get valid potential OrderMatcher pairs
    id_executions_dict, execution_id_dict = get_order_id_available_executions(zone_id, date, feasible_orders, om_execution_times)
    pair_executions, valid_pairs = get_executions_per_pair(feasible_orders, id_executions_dict)
    pass_hard_checks = pass_hard_rules_pairs_eff(orders_dict, valid_pairs, efficiency_constraint=constants.DEFAULT_MP_SIMULATOR_SETTINGS["EFFICIENCY_CONSTRAINT"])

    total_time_estimations, part_time_estimations = get_time_estimations(zone_id, date, orders_dict, pass_hard_checks)

    if geo_params["HAS_FROZEN_PRODUCTS_CHECK"]:
        valid_pairs = _check_has_frozen_products_eff(pass_hard_checks, orders_dict, part_time_estimations, geo_params["MAX_MINUTES_ALLOWED_FOR_FROZEN_PRODUCTS"])
    else:
        valid_pairs = pass_hard_checks

    potential_pairs_executions, execution_potential_pairs = get_potential_pairs(orders_dict, om_execution_times, valid_pairs, pair_executions, total_time_estimations)

    potential_pairs = list(potential_pairs_executions.keys())

    potential_pairs_weight_dict, pair_total_distance, pair_intra_client_distance = pair_utility_and_distance_eff(orders_dict, potential_pairs)

    ##############################
    # STEP 2: EXECUTE SIMULATION #
    ##############################

    algorithm_name = non_geo_params["ALGORITHM"]

    # print(f"Zone ID: {zone_id} | Date: {date} | OM exec. length set: {non_geo_params['OM_EXECUTION_LENGTH']} | Algorithm: {non_geo_params['ALGORITHM']} | Instances: {non_geo_params['INSTANCES']}")
    print(f"    > Start simulation | Algorithm: {algorithm_name}... ", end=' ')

    # Initialize Match trackers
    global_matched_pairs = []
    suspended_orders_dict = {}
    new_execution_potential_pairs = execution_potential_pairs.copy()

    for time_stamp in om_execution_times:

        potential_pairs_execution = new_execution_potential_pairs[time_stamp]

        if len(potential_pairs_execution) == 0:
            continue

        algorithm_parameters = {
            "potential_pairs": potential_pairs_execution,
            "potential_pairs_weight_dict": potential_pairs_weight_dict,
            "pair_total_distance": pair_total_distance,
            "pair_intra_client_distance": pair_intra_client_distance,
            'total_saving_limit': non_geo_params["TOTAL_SAVING_LIMIT"],
        }

        matched_pairs = matching_algorithm(algorithm_parameters)

        (
            final_matched_pairs,
            suspended_orders_dict
        ) = matched_or_eliminated(
            matched_pairs=matched_pairs,
            om_execution_times=om_execution_times,
            not_matched_probability=non_geo_params["NOT_MATCHED_PROBABILITY"],
            conversion_probability_by_hour=non_geo_params["CONVERSION_BY_HOUR"],
            time_stamp=time_stamp,
            suspended_orders_dict=suspended_orders_dict
        )

        global_matched_pairs += final_matched_pairs

        new_execution_potential_pairs = refresh_execution_potential_pairs(execution_potential_pairs, global_matched_pairs, suspended_orders_dict, time_stamp)

    print('Done!')

    (   day_total_orders,
        real_mp_pct,
        simulation_mp_pct,
        pct_multipicking_oos,
        simulation_mp_pct_oos,
        pct_mp_out_of_possible,
        avg_matched_distance,
        avg_non_matched_distance,
        avg_distance,
        total_saving_distribution,
    ) = simulation_results(feasible_orders, global_matched_pairs, pair_total_distance, pair_intra_client_distance, potential_pairs_weight_dict, zone_id, date)
    # TODO: Fit all this stuff in a nice and compact dictionary
    new_row_dict = {
        "zone_id": zone_id,
        "date": date,
        "real_mp_pct": real_mp_pct,
        "simulation_mp_pct": simulation_mp_pct,
        "avg_matched_distance": avg_matched_distance,
        "avg_non_matched_distance": avg_non_matched_distance,
        "avg_distance": avg_distance,
        "total_saving_distribution": total_saving_distribution,
        "pct_multipicking_oos": pct_multipicking_oos,
        "simulation_mp_pct_oos": simulation_mp_pct_oos,
        "move_promised_n_hours": non_geo_params["PROMISED_DELIVERY_TIME_SHIFT"],
        "move_picking_assignable_n_hours": non_geo_params["PICKING_ASSIGNABLE_TIME_SHIFT"],
        "picking_assignable_window_length": geo_params["PICKING_ASSIGNABLE_WINDOW_LENGTH"],
        "picking_assignable_lower_limit_heuristic": geo_params["PICKING_ASSIGNABLE_LOWER_LIMIT_HEURISTIC"],
        "delivery_slot_lower_buffer": geo_params["DELIVERY_SLOT_LOWER_BUFFER"],
        "delivery_slot_upper_buffer": geo_params["DELIVERY_SLOT_UPPER_BUFFER"],
        "min_delivery_slots_overlap": geo_params["MIN_DELIVERY_SLOTS_OVERLAP"],
        "not_matched_probability": non_geo_params["NOT_MATCHED_PROBABILITY"],
        "algorithm": non_geo_params["ALGORITHM"],
        "total_saving_limit": non_geo_params["TOTAL_SAVING_LIMIT"],
        "efficiency_constraint": non_geo_params["EFFICIENCY_CONSTRAINT"],
        "max_total_products": geo_params["MAX_ALLOWED_TOTAL_PRODUCTS"],
        "max_delivery_distance": geo_params["MAX_DELIVERY_DISTANCES"],
        "max_branch_to_delivery_distance": geo_params["MAX_BRANCH_TO_DELIVERY_DISTANCE"],
        "has_frozen_products_check": geo_params["HAS_FROZEN_PRODUCTS_CHECK"],
        "max_minutes_allowed_for_frozen_products": geo_params["MAX_MINUTES_ALLOWED_FOR_FROZEN_PRODUCTS"],
        "instance": non_geo_params["INSTANCES"],
        "day_total_orders": day_total_orders,
        "mp_potential_orders": feasible_orders.shape[0],
        "simulation_mp_pct": simulation_mp_pct,
        "pct_mp_out_of_possible": pct_mp_out_of_possible,
        "total_global_matches": len(global_matched_pairs),
    }

    # Get the filename
    filename = get_simulation_file_name(simulation_values)

    # Save the result
    insert_row_parameters(new_row_dict, filename)

    new_row_dict = {
        "zone_id": zone_id,
        "date": date,
        "real_mp_pct": real_mp_pct,
        "simulation_mp_pct": simulation_mp_pct,
        "pct_multipicking_oos": pct_multipicking_oos,
        "simulation_mp_pct_oos": simulation_mp_pct_oos

    }

    return new_row_dict


def get_simulation_non_geo_parameters(simulation_values,):  # In this function we come and get default values (and conversion by hour data) if they haven't been defined?

    zone_id = simulation_values.get('zone_id')
    date = simulation_values.get('date')

    simulation_non_geo_parameters_list = ['zone_id', 'date', 'output_folder'] + list(constants.DEFAULT_MP_SIMULATOR_SETTINGS)

    simulation_non_geo_parameters = {
        param_name: simulation_values.get(param_name, constants.DEFAULT_MP_SIMULATOR_SETTINGS.get(param_name))
        for param_name in simulation_non_geo_parameters_list
    }

    try:
        with open(f"{DATA_DIR}/sim_resources/conversion_by_hour/{zone_id}/conversion_by_hour_{zone_id}_{date}.pickle", "rb") as handle:  # Updated to new dir map
            conversion_by_hour_dict = pickle.load(handle)
    except BaseException:
        print(f'No conversion data found for {(zone_id, date)}')
        conversion_by_hour_dict = None

    simulation_non_geo_parameters['CONVERSION_BY_HOUR'] = conversion_by_hour_dict

    return simulation_non_geo_parameters


def get_simulation_geo_parameters(simulation_values,):
    """
    Get geo-opzone parameters for the simulation.  First we try getting the values from
    'simulation_values', then from 'geo_opzone_data', else, we extract the default values.
    """

    #geo_opzone_data = pd.read_csv(f"{MP_SIMULATOR_ROOT_DIR}/data/raw/op_zone_data.csv", decimal=".", sep=",")  # Read op_zone_data.csv

    try:
        geo_opzone_data = load_pickle('', 'op_zone_data')
    except FileNotFoundError:
        print('Timezone Dict error: op_zone_data.pickle not found in "data" directory. Now proceeding to fetch from Superpal...')
        op_zone_data = query_to_table(opzone_mp_settings_parameter_query(), db='superpal')
        print('Done!')
        dump_pickle(geo_opzone_data, '', 'op_zone_data')

    zone_id = simulation_values['zone_id']

    op_zone_mp_settings = loads(geo_opzone_data.loc[geo_opzone_data.zone_id == zone_id].iloc[0].value)  # Get MP_SETTINGS as a dict

    simulation_geo_parameters = dict(
        zone_id = zone_id,
    )

    mpd_parameter_list = constants.DEFAULT_OP_ZONE_MP_SETTINGS.keys()

    for param in mpd_parameter_list:
        simulation_geo_parameters[param] = get_mp_parameter(simulation_values, op_zone_mp_settings, param)

    op_zone_mp_settings_df = pd.DataFrame([simulation_geo_parameters]).rename(columns={'zone_id':'customer_zone_id'})

    return simulation_geo_parameters, op_zone_mp_settings_df


def fetch_feasible_orders(
    zone_id: int,
    date: date,
    move_promised_n_hours: int,
    move_picking_assignable_n_hours: int,
    geo_opzone_df: pd.DataFrame,
) -> pd.DataFrame:
    """
    what it should do:
        - load the order data (pickled)
        - transform n add any required data
            - merge data with opzone settings
            - add B2C distance
            - add time columns (promise hour, dom, dow)
        - filter any required conditions
    """

    order_details = get_order_details(zone_id, date)
    order_details = order_details.merge(geo_opzone_df, on='customer_zone_id')
    order_details = exclude_special_case_orders(order_details)
    feasible_orders = apply_hard_rules(order_details)

    return feasible_orders


def get_order_details(zone_id: int, date: str) -> pd.DataFrame:
    try:
        with open(f"{DATA_DIR}/sim_resources/order_details/{zone_id}/order_details_{zone_id}_{date}.pickle", "rb") as handle:
            orders = pickle.load(handle)

        #orders.drop(columns="parent_id", inplace=True, axis=1)
        orders = append_customer_to_branch_distance(orders)
        orders = transform_dates(orders)
        return orders
    except FileNotFoundError:
        print(f'No order detail pickle found for {(zone_id, date)}')
        raise


def append_customer_to_branch_distance(orders: pd.DataFrame) -> pd.DataFrame:
    orders['customer_location'] = orders.customer_location.apply(wkt.loads)
    orders['branch_location'] = orders.branch_location.apply(wkt.loads)
    orders['branch_to_customer_distance'] = orders.apply(
        lambda x: constants.HAVERSINE_TO_MANHATTAN_COEFF*haversine_distance(x.customer_location, x.branch_location),
        axis=1
        )
    return orders


def haversine_distance(point_a: Point, point_b: Point) -> float:
    """
    Calculate the great circle distance between two points
    on the earth
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(float, [point_a.x, point_a.y, point_b.x, point_b.y])
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return 1000 * c * r  # for meters


def exclude_special_case_orders(orders: pd.DataFrame) -> pd.DataFrame:
    special_cases = ((orders.store_name != "Costco") & (orders.country != "CA")) & (orders.order_kind != "GIFT_ORDER")
    return orders  # [special_cases]


def transform_dates(orders: pd.DataFrame) -> pd.DataFrame:
    orders['min_delivery_time'] = pd.to_datetime(orders['min_delivery_time'])
    orders['promised_datetime'] = pd.to_datetime(orders['promised_datetime'])
    orders["promise_hour"] = orders.promised_datetime.dt.hour
    orders["day_of_month"] = orders.promised_datetime.dt.day
    orders["day_of_week"] = orders.promised_datetime.dt.day_name()
    return orders


def apply_hard_rules(orders: pd.DataFrame) -> pd.DataFrame:
    hard_rules = (
        (orders.products_ordered < orders.MAX_ALLOWED_TOTAL_PRODUCTS)
        & (orders.branch_to_customer_distance < orders.MAX_BRANCH_TO_DELIVERY_DISTANCE)
        & (~orders.total_weight.isna())
    )
    return orders[hard_rules]


def get_om_execution_times(zone_id: int, date: datetime, step_in_seconds: int) -> Iterable[datetime]:
    """
    Returns a list of timestamps with a frequency of 'step_in_seconds' from
    'start_time' until  'end_time'. If 'step_in_seconds' was not provided, then we use the
    timestamps of the real executions of that day.
    """
    print("    > Get OM execution times... ", end='')
    try:
        if not step_in_seconds:
            with open(f'{DATA_DIR}/sim_resources/om_execution_times/{zone_id}/om_execution_times_{zone_id}_{date}.pickle', "rb") as handle:
                order_matcher_execution_times = pickle.load(handle)
            #order_matcher_execution_times = order_matcher_execution_times
        else:
            current_time = pd.to_datetime(f"{date} 04:00:00")
            order_matcher_execution_times = []

            while current_time <= pd.to_datetime(f"{date} 23:59:00"):
                order_matcher_execution_times.append(current_time)
                current_time += timedelta(seconds=step_in_seconds)
        print('OK')
        return order_matcher_execution_times
    except BaseException:
        print("Failed")
        raise


def hard_rules_check_filter_eff(orders_info_dict, order_1: int, order_2: int, efficiency_constraint: bool) -> bool:
    """
    Pairs go through a funnel of hard filters.  If a pair doesn't meet a condition, then
    the pair is dissolved.
    """
    order_1_info = orders_info_dict[order_1]
    order_2_info = orders_info_dict[order_2]

    return (
        _check_max_allowed_products_eff(order_1_info, order_2_info)
        and _check_max_allowed_distance_between_clients_eff(order_1_info, order_2_info)
        and _check_delivery_slot_compatibility_eff(order_1_info, order_2_info)
    )


orders_info_dict = dict()  # What's this? Do not delete yet. Map, then delete.

def sort_orders(table: pd.DataFrame, order_id_1: int, order_id_2: int) -> List[int]:
    """
    Pairs are sorted in the following way: The first order is the one
     that has the least distance to the customer branch (remember both orders
     share the same customer branch).
    """
    if order_id_1 in orders_info_dict:
        order_1_info = orders_info_dict[order_id_1]
    else:  # why would an order not be in the dict, but would in the df?
        order_1_info = table[table.order_id == order_id_1]
        orders_info_dict[order_id_1] = order_1_info

    if order_id_2 in orders_info_dict:
        order_2_info = orders_info_dict[order_id_2]
    else:
        order_2_info = table[table.order_id == order_id_2]
        orders_info_dict[order_id_2] = order_2_info

    branch_loc = order_1_info.branch_location.iloc[0]  # Don't like this
    order_1_loc = order_1_info.customer_location.iloc[0]
    order_2_loc = order_2_info.customer_location.iloc[0]

    b2c_1 = haversine_distance(branch_loc, order_1_loc)
    b2c_2 = haversine_distance(branch_loc, order_2_loc)

    return [order_id_1, order_id_2] if b2c_1 <= b2c_2 else [order_id_2, order_id_1]


def _check_max_allowed_products_eff(order_1_info: Dict[str, Any], order_2_info: Dict[str, Any]) -> bool:
    """
    Filter out all the pairs in which the sum of the products is more than the max allowed.
    """

    n_products_1 = order_1_info['products_ordered']
    n_products_2 = order_2_info['products_ordered']

    max_allowed_total_products = order_1_info['MAX_ALLOWED_TOTAL_PRODUCTS']

    return n_products_1 + n_products_2 < max_allowed_total_products  # < OR <=?


def _check_max_allowed_distance_between_clients_eff(order_1_info: Dict[str, Any], order_2_info: Dict[str, Any]) -> bool:
    """
    Filter out batches where clients are further away from each other than
    the max allowed distance.
    """

    max_distance_between_customers = order_1_info['MAX_DELIVERY_DISTANCES']
    distance = haversine_distance(order_1_info['customer_location'], order_2_info['customer_location'])

    return distance <= max_distance_between_customers


def _check_delivery_slot_compatibility_eff(order_1_info: Dict[str, Any], order_2_info: Dict[str, Any]) -> bool:
    """
    Filter out all pairs who's orders do not meet slot compatibility conditions:
    1) Slot overlap has to be bigger than the specified parameter
    2) The min delivery time of the first client has to be at least 15 minutes prior to the
    promised delivery time of the second client.
    """
    min_window_overlap = order_1_info['MIN_DELIVERY_SLOTS_OVERLAP']

    latest_min_delivery = max(
        order_1_info['min_delivery_time'],
        order_2_info['min_delivery_time'],
    )

    earliest_promised_delivery_time = min(
        order_1_info['promised_datetime'],
        order_2_info['promised_datetime']
    )

    slots_overlap = max(
        0,
        (earliest_promised_delivery_time - latest_min_delivery).seconds / 60,
    )

    allowed_time = order_1_info['SLOT_COMPATIBILITY']

    orders_are_compatible = (
        order_1_info['min_delivery_time'] + np.timedelta64(allowed_time, "m")
        <= order_2_info['promised_datetime']
    )

    return orders_are_compatible and slots_overlap >= min_window_overlap


def estimation_shopping_setup(data_list: List[Any]) -> List[Any]:
    """
    Returns shopping setup estimation.
    """
    url = f"{pre_url}/v1/models/shopping_setup/versions/3:predict"
    data = {"signature_name": "predict", "instances": data_list}
    response = post(url, json=data)
    response_percentile = [element["0.5"][0] for element in response.json()["predictions"]]
    return response_percentile


def estimation_shopping(data_list):
    """
    Returns shopping estimation.
    """
    url = f"{pre_url}/v1/models/shopping/versions/4:predict"
    data = {"signature_name": "predict", "instances": data_list}
    response = post(url, json=data)
    response_percentile = [element["0.6"][0] for element in response.json()["predictions"]]
    return response_percentile


def estimation_transportation_setup(data_list: List[Any]) -> List[Any]:
    """
    Returns transportation setup estimation.
    """
    url = f"{pre_url}/v1/models/transportation_setup/versions/3:predict"
    data = {"signature_name": "predict", "instances": data_list}
    response = post(url, json=data)
    response_percentile = [element["0.5"][0] for element in response.json()["predictions"]]

    return response_percentile


def estimation_transportation(data_list: List[Any]) -> List[Any]:
    """
    Returns transportation estimation.
    """
    url = f"{pre_url}/v1/models/transportation/versions/3:predict"
    data = {"signature_name": "predict", "instances": data_list}
    response = post(url, json=data)
    response_percentile = [element["0.5"][0] for element in response.json()["predictions"]]
    return response_percentile


def pair_utility_and_distance_eff(
    orders_info_dict,
    potential_pairs
):

    pair_intra_client_distance = {}
    pair_total_distance = {}
    pair_utility = {}

    for pair in potential_pairs:

        order_id_1, order_id_2 = pair

        order_1_info = orders_info_dict[order_id_1]
        order_2_info = orders_info_dict[order_id_2]

        distance_between_clients = haversine_distance(order_1_info['customer_location'], order_2_info['customer_location'])

        pair_intra_client_distance[pair] = distance_between_clients

        pair_distance = order_1_info['branch_to_customer_distance'] + distance_between_clients

        pair_total_distance[pair] = pair_distance

        utility = (
            order_1_info['branch_to_customer_distance'] + order_2_info['branch_to_customer_distance']
            - (distance_between_clients + order_1_info['branch_to_customer_distance'])
        )

        pair_utility[pair] = utility


    return pair_utility, pair_total_distance, pair_intra_client_distance


def simulation_results(processed_data, global_matched_pairs, pair_total_distance, pair_intra_client_distance, potential_pairs_weight_dict, zone_id, date):
    # Think about separating the result processing stage from the simulation running itself.
    matched_orders = []
    for order_1, order_2 in global_matched_pairs:
        matched_orders.append(order_1)
        matched_orders.append(order_2)

    total_saving_distribution = {k: v for k, v in potential_pairs_weight_dict.items() if k in global_matched_pairs}

    shopping_setup_distance = 0

    not_matched_orders_data = processed_data[~processed_data.order_id.isin(matched_orders)].reset_index(drop=True)
    total_non_matched_distance = np.sum(not_matched_orders_data.branch_to_customer_distance)

    matched_pairs_distance = {
        pair: distance for pair, distance in pair_total_distance.items() if pair in global_matched_pairs
    }
    total_matched_distance = np.sum(list(matched_pairs_distance.values()))

    matched_intra_client_distance = {
        pair: distance for pair, distance in pair_intra_client_distance.items() if pair in global_matched_pairs
    }

    total_matched_distance_between_clients = np.sum(list(matched_intra_client_distance.values()))

    avg_match_distance_between_clients = total_matched_distance_between_clients / len(global_matched_pairs)

    total_distance_simulation = total_non_matched_distance + total_matched_distance

    total_matched_orders = 2 * len(global_matched_pairs)
    total_non_matched_orders = not_matched_orders_data.shape[0]

    pct_mp_out_of_possible = 100 * total_matched_orders / (total_matched_orders + total_non_matched_orders)

    mp = load_pickle(f'sim_resources/daily_zone_mpd_stats/{zone_id}', 'daily_zone_mpd_stats', (zone_id,), (date,))
    #mp = pd.read_csv(f"{MP_SIMULATOR_ROOT_DIR}/data/sim_resources/daily_zone_mpd_stats/{zone_id}/mpd_stats_{zone_id}_{date}.csv", sep=",", decimal=".")

    day_total_orders = mp.iloc[0].total_day_orders
    total_scheduled_orders = mp.iloc[0].total_scheduled_orders
    real_mp_pct = mp.iloc[0].dispatcher_pct
    pct_multipicking_oos = mp.iloc[0].pct_multipicking_oos

    simulation_mp_pct = 100 * (total_matched_orders / day_total_orders)
    simulation_mp_pct_oos = 100 * (total_matched_orders / total_scheduled_orders)

    avg_matched_distance = total_matched_distance / total_matched_orders
    avg_non_matched_distance = total_non_matched_distance / total_non_matched_orders
    avg_distance = (total_matched_distance + total_non_matched_distance) / (total_matched_orders + total_non_matched_orders)


    return (
        day_total_orders,
        real_mp_pct,
        simulation_mp_pct,
        pct_multipicking_oos,
        simulation_mp_pct_oos,
        pct_mp_out_of_possible,
        avg_matched_distance,
        avg_non_matched_distance,
        avg_distance,
        total_saving_distribution,
    )


def insert_row_parameters(new_row_dict, file_name):

    column_names = list(new_row_dict.keys())
    values = list(new_row_dict.values())

    new_row = pd.DataFrame([values], columns=column_names)

    save_dir = os.path.dirname(file_name)
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    with open(file_name, "wb") as handle:
        pickle.dump(new_row, handle, protocol=pickle.HIGHEST_PROTOCOL)

    print(f'Results saved in {file_name}.', end='\n\n')


def matched_or_eliminated(
    matched_pairs: Set[Tuple[int, int]],
    om_execution_times: Set[Tuple[int, int]],
    not_matched_probability,
    conversion_probability_by_hour: float,
    time_stamp,
    suspended_orders_dict
):
    final_matched_pairs = []
    suspended_pairs_list = []

    if not_matched_probability != None:
        conversion_probability = 1 - not_matched_probability
    else:
        conversion_probability = conversion_probability_by_hour[time_stamp.hour]

    for pair in matched_pairs:

        match_is_converted = np.random.uniform() < conversion_probability

        if match_is_converted:
            final_matched_pairs.append(pair)

        else:
            suspended_pairs_list.append(pair)

    start_time = time_stamp
    end_time = time_stamp + timedelta(minutes=3)  # TODO: new TTL?
    suspended_periods = [ex for ex in om_execution_times if start_time <= ex <= end_time]

    for o1, o2 in suspended_pairs_list:
        suspended_orders_dict[o1] = suspended_periods
        suspended_orders_dict[o2] = suspended_periods

    return (
        final_matched_pairs,
        suspended_orders_dict,
    )


def get_simulation_file_name(simulation_values):

    output_folder = simulation_values["output_folder"]

    now_time = datetime.now()

    filename = f"{DATA_DIR}/results/{output_folder}/{output_folder}_{now_time}.pickle"

    non_geo_params = get_simulation_non_geo_parameters(simulation_values)

    geo_params, _ = get_simulation_geo_parameters(simulation_values)

    return filename


def get_order_id_available_executions(
    zone_id: int, date: datetime, data: pd.DataFrame, om_execution_times: list
) -> Dict[datetime, list]:
    """
    Returns a dictionary with all the avaible order ids for a particular execution
    """

    print("    > Get each OM executions available order IDs... ", end='')

    order_0 = data.iloc[0]
    lower_limit = timedelta(minutes=int(order_0.PICKING_ASSIGNABLE_LOWER_LIMIT_HEURISTIC))
    upper_limit = timedelta(minutes=int(order_0.PICKING_ASSIGNABLE_LOWER_LIMIT_HEURISTIC - order_0.PICKING_ASSIGNABLE_LOWER_LIMIT_HEURISTIC))

    id_executions_dict = {}

    for _, row in data.iterrows():

        order_id = row.order_id
        pat = row.picking_assignable_time
        # is_asap = row.is_asap
        # created = row.created
        # if is_asap:
        #     available_executions = [ex for ex in om_execution_times if created <= ex <= pat]
        #     id_executions_dict[order_id] = available_executions
        # else:
        #     start_time = pat - lower_limit
        #     end_time = pat - upper_limit
        #     available_executions = [ex for ex in om_execution_times if start_time <= ex <= end_time]
        #     id_executions_dict[order_id] = available_executions

        start_time = pat - lower_limit
        end_time = pat - upper_limit
        available_executions = [ex for ex in om_execution_times if start_time <= ex <= end_time]
        id_executions_dict[order_id] = available_executions

    execution_id_dict = {}
    for id, executions in id_executions_dict.items():
        for moment in executions:
            execution_id_dict.setdefault(moment, []).append(id)

    missing_executions = set(om_execution_times) - set(execution_id_dict.keys())

    execution_id_dict.update({execution: [] for execution in missing_executions})

    print('OK')

    return id_executions_dict, execution_id_dict


def get_executions_per_pair(table, execution_id_dict):

    print("    > Get OM executions per matched pair... ", end='')

    pair_executions = {}
    unique_customer_branches = list(table.store_branch_id.unique())

    for cb in unique_customer_branches:
        order_ids_in_cb = table[table.store_branch_id == cb].order_id
        cb_combinations = combinations(order_ids_in_cb, 2)
        for o1, o2 in cb_combinations:
            executions_o1 = execution_id_dict[o1]
            executions_o2 = execution_id_dict[o2]
            common_executions = set(executions_o1).intersection(set(executions_o2))
            pair_executions[(o1, o2)] = common_executions

    final_pair_executions = {}
    for pair, common_executions in pair_executions.items():
        if common_executions:
            sorted_pair = tuple(sort_orders(table, pair[0], pair[1]))
            final_pair_executions[sorted_pair] = common_executions

    valid_pairs = list(final_pair_executions.keys())

    print('OK')

    return final_pair_executions, valid_pairs


def pass_hard_rules_pairs_eff(orders_info_dict, valid_pairs, efficiency_constraint):

    print("    > Apply MPD hard rules... ", end='')
    pass_hard_checks = {
                pair: hard_rules_check_filter_eff(
                    orders_info_dict=orders_info_dict, order_1=pair[0], order_2=pair[1], efficiency_constraint=efficiency_constraint
                )
                for pair in valid_pairs
    }


    pass_hard_checks = [key for key, value in pass_hard_checks.items() if value]

    print('OK')
    return pass_hard_checks


def get_total_time_estimations_max(orders_info_dict, pass_hard_checks):


    data_list_shopping_setup = []
    data_list_shopping = []
    data_list_transportation_setup = []
    data_list_transportation_first = []
    data_list_transportation_second = []

    total_time_estimations = {}
    part_time_estimations = {}


    #print('start building input')
    for pair in pass_hard_checks:
        order_1, order_2 = pair


        order_1_info = orders_info_dict[order_1]
        order_2_info = orders_info_dict[order_2]

        data_list_shopping_setup.append(shopping_setup_input_max(order_1_info, order_2_info))
        data_list_shopping.append(shopping_input_max(order_1_info, order_2_info))
        data_list_transportation_setup.append(transportation_setup_input_max(order_1_info, order_2_info))
        data_list_transportation_first.append(transportation_input_max(order_1_info, order_2_info, "BRANCH"))
        data_list_transportation_second.append(transportation_input_max(order_1_info, order_2_info, "CUSTOMER"))

    #print('start making requests')
    total_pair_estimations = len(data_list_shopping_setup)
    n_batches = 100
    length_batches = int(total_pair_estimations / n_batches) + 1

    for batch in range(n_batches):
        #print('batch: ', batch+1, 'pct', 100*(batch+1)/n_batches),'%'

        pass_hard_checks_aux = pass_hard_checks[length_batches * batch: length_batches * (batch + 1)]

        if len(pass_hard_checks_aux) == 0:
            break

        data_list_shopping_setup_aux = data_list_shopping_setup[length_batches * batch: length_batches * (batch + 1)]
        data_list_shopping_aux = data_list_shopping[length_batches * batch: length_batches * (batch + 1)]
        data_list_transportation_setup_aux = data_list_transportation_setup[length_batches * batch: length_batches * (batch + 1)]
        data_list_transportation_first_aux = data_list_transportation_first[length_batches * batch: length_batches * (batch + 1)]
        data_list_transportation_second_aux = data_list_transportation_second[length_batches * batch: length_batches * (batch + 1)]

        try:
            estimations_shopping_setup = estimation_shopping_setup(data_list_shopping_setup_aux)
            estimations_shopping = estimation_shopping(data_list_shopping_aux)
            estimations_transportation_setup = estimation_transportation_setup(data_list_transportation_setup_aux)
            estimations_transportation_first = estimation_transportation(data_list_transportation_first_aux)
            estimations_transportation_second = estimation_transportation(data_list_transportation_second_aux)
        except requests.exceptions.ConnectionError:
            print('There was a problem connecting to the Estimator model.')
            raise

        part_time_estimations_aux = {
            pass_hard_checks_aux[i]: [{
                "estimation_shopping_setup":estimations_shopping_setup[i],
                "estimation_shopping": estimations_shopping[i],
                "estimation_transportation_setup": estimations_transportation_setup[i],
                "estimation_transportation": estimations_transportation_first[i]
                },
                {
                "estimation_shopping_setup": estimations_shopping_setup[i],
                "estimation_shopping": estimations_shopping[i],
                "estimation_transportation_setup": estimations_transportation_setup[i],
                "estimation_transportation": estimations_transportation_first[i] + estimations_transportation_second[i]
                }]

            for i in range(len(pass_hard_checks_aux))
        }


        part_time_estimations.update(part_time_estimations_aux)


        total_time_estimations_aux = {
            pass_hard_checks_aux[i]: [
                estimations_shopping_setup[i]
                + estimations_shopping[i]
                + estimations_transportation_setup[i]
                + estimations_transportation_first[i],
                estimations_shopping_setup[i]
                + estimations_shopping[i]
                + estimations_transportation_setup[i]
                + estimations_transportation_first[i]
                + estimations_transportation_second[i],
            ]
            for i in range(len(pass_hard_checks_aux))
        }

        total_time_estimations.update(total_time_estimations_aux)
    return total_time_estimations, part_time_estimations


def _check_has_frozen_products_eff(valid_pairs, orders_info_dict, part_time_estimations, max_minutes_allowed_for_frozen_products):

    print("    > Apply frozen product restriction... ", end='')
    pass_frozen_products_check = {
                pair: _check_has_frozen_products(
                    orders_info_dict=orders_info_dict, pair=pair, part_time_estimations=part_time_estimations, max_minutes_allowed_for_frozen_products=max_minutes_allowed_for_frozen_products
                )
                for pair in valid_pairs
    }

    valid_pairs = [key for key, value in pass_frozen_products_check.items() if value]
    print('OK')
    return valid_pairs


def get_potential_pairs(orders_info_dict, om_execution_times, pass_hard_checks, pair_executions, total_time_estimations):

    print("    > Apply on-time restrictions... ", end='')

    potential_pairs_executions = {}

    for pair in pass_hard_checks:
        executions = pair_executions[pair]

        for time_stamp in executions:

            check_min_promised = check_min_and_promised_max(
                orders_info=orders_info_dict,
                pair=pair,
                total_time_estimations=total_time_estimations,
                time_stamp=time_stamp,
            )


            if check_min_promised:
                potential_pairs_executions.setdefault(pair, []).append(time_stamp)


    execution_potential_pairs = {}
    for pair, executions in potential_pairs_executions.items():
        for moment in executions:
            execution_potential_pairs.setdefault(moment, []).append(pair)


    missing_executions = set(om_execution_times) - set(execution_potential_pairs.keys())

    execution_potential_pairs.update({execution: [] for execution in missing_executions})

    print('OK')
    return potential_pairs_executions, execution_potential_pairs


def check_min_and_promised_max(orders_info, pair, total_time_estimations, time_stamp):

    order_id_1 = pair[0]
    order_id_2 = pair[1]

    order_1_info = orders_info[order_id_1]

    order_2_info = orders_info[order_id_2]

    orders_info = [order_1_info, order_2_info]

    for index in range(len(orders_info)):
        min_time = orders_info[index]['min_delivery_time']

        promised_time = orders_info[index]['promised_datetime']

        estimated_delivery_time = time_stamp + timedelta(minutes=total_time_estimations[pair][index])

        if (
            estimated_delivery_time - timedelta(minutes=int(orders_info[index]['DELIVERY_SLOT_LOWER_BUFFER']))
            < min_time
        ) or (
            estimated_delivery_time + timedelta(minutes=int(orders_info[index]['DELIVERY_SLOT_UPPER_BUFFER']))
            > promised_time
        ):
            return False
    return True


def _check_has_frozen_products(orders_info_dict, pair, part_time_estimations, max_minutes_allowed_for_frozen_products):


    order_id_1 = pair[0]
    order_id_2 = pair[1]

    order_1_info = orders_info_dict[order_id_1]

    order_2_info = orders_info_dict[order_id_2]

    orders_info = [order_1_info, order_2_info]


    for index in range(2):

        has_frozen_product = orders_info[index]['has_frozen_product']

        if has_frozen_product:

            estimation = part_time_estimations[pair][index]

            picking_minutes = estimation['estimation_shopping_setup'] + estimation['estimation_shopping']
            delivery_minutes = estimation['estimation_transportation_setup'] + estimation['estimation_transportation']

            defrosting_time = (picking_minutes / 2) + delivery_minutes

            if defrosting_time > max_minutes_allowed_for_frozen_products:
                return False

        else:
            continue

    return True


def shopping_setup_input_max(order_1_info: pd.DataFrame, order_2_info: pd.DataFrame) -> Dict[str, Any]:
    """
    Returns input for shopping setup estimation.
    """
    city_name = order_1_info["city_name"]
    store_name = order_1_info["store_name"]
    day_of_month = order_1_info["day_of_month"]
    day_of_week = order_1_info["day_of_week"]
    promise_hour = order_1_info["promised_datetime"].hour
    on_demand = 0
    num_products_by_unit = order_1_info["n_products_by_unit"] + order_2_info["n_products_by_unit"]
    num_products_by_weight = order_1_info["n_products_by_weight"] + order_2_info["n_products_by_weight"]
    num_custom_products = order_1_info["n_custom_products"] + order_2_info["n_custom_products"]
    total_weight = order_1_info["total_weight"] + order_2_info["total_weight"]
    storebranch_id = order_1_info["store_branch_id"]
    storebranch_lat = order_1_info["branch_location"].y
    storebranch_lng = order_1_info["branch_location"].x
    num_orders = 2

    return {
        "city": city_name,
        "store": store_name,
        "day_of_month": int(day_of_month),
        "day_of_week": day_of_week,
        "promise_hour": promise_hour,
        "on_demand": on_demand,
        "num_products_by_unit": int(num_products_by_unit),
        "num_products_by_weight": int(num_products_by_weight),
        "num_custom_products": int(num_custom_products),
        "total_weight": float(total_weight),
        "storebranch_id": int(storebranch_id),
        "storebranch_lat": float(storebranch_lat),
        "storebranch_lng": float(storebranch_lng),
        "num_orders": int(num_orders),
    }


def shopping_input_max(order_1_info: pd.DataFrame, order_2_info: pd.DataFrame) -> Dict[str, Any]:
    """
    Returns input for shopping estimation.
    """
    city_name = order_1_info["city_name"]
    store_name = order_1_info["store_name"]
    day_of_month = order_1_info["day_of_month"]
    day_of_week = order_1_info["day_of_week"]
    promise_hour = order_1_info["promised_datetime"].hour
    on_demand = 0
    unique_categories = order_1_info["unique_categories"] + order_2_info["unique_categories"]
    unique_top_level_categories = (
        order_1_info["unique_top_level_categories"] + order_2_info["unique_top_level_categories"]
    )
    num_products_by_unit = order_1_info["n_products_by_unit"] + order_2_info["n_products_by_unit"]
    num_products_by_weight = order_1_info["n_products_by_weight"] + order_2_info["n_products_by_weight"]
    num_custom_products = order_1_info["n_custom_products"] + order_2_info["n_custom_products"]
    total_weight = order_1_info["total_weight"] + order_2_info["total_weight"]
    storebranch_id = order_1_info["store_branch_id"]
    storebranch_lat = order_1_info["branch_location"].y
    storebranch_lng = order_1_info["branch_location"].x
    num_orders = 2

    return {
        "city": city_name,
        "store": store_name,
        "day_of_month": int(day_of_month),
        "day_of_week": day_of_week,
        "promise_hour": promise_hour,
        "on_demand": on_demand,
        "unique_categories": int(unique_categories),
        "unique_top_level_categories": int(unique_top_level_categories),
        "num_products_by_unit": int(num_products_by_unit),
        "num_products_by_weight": int(num_products_by_weight),
        "num_custom_products": int(num_custom_products),
        "total_weight": float(total_weight),
        "storebranch_id": int(storebranch_id),
        "storebranch_lat": float(storebranch_lat),
        "storebranch_lng": float(storebranch_lng),
        "num_orders": int(num_orders),
    }


def transportation_setup_input_max(order_1_info: pd.DataFrame, order_2_info: pd.DataFrame) -> Dict[str, Any]:
    """
    Returns input for transportation setup estimation.
    """
    city_name = order_1_info["city_name"]
    store_name = order_1_info["store_name"]
    day_of_month = order_1_info["day_of_month"]
    day_of_week = order_1_info["day_of_week"]
    promise_hour = order_1_info["promised_datetime"].hour
    on_demand = 0
    num_products_by_unit = order_1_info["n_products_by_unit"] + order_2_info["n_products_by_unit"]
    num_products_by_weight = order_1_info["n_products_by_weight"] + order_2_info["n_products_by_weight"]
    num_custom_products = order_1_info["n_custom_products"] + order_2_info["n_custom_products"]
    total_weight = order_1_info["total_weight"] + order_2_info["total_weight"]
    storebranch_id = order_1_info["store_branch_id"]

    return {
        "city": city_name,
        "store": store_name,
        "day_of_month": int(day_of_month),
        "day_of_week": day_of_week,
        "promise_hour": promise_hour,
        "on_demand": on_demand,
        "num_products_by_unit": int(num_products_by_unit),
        "num_products_by_weight": int(num_products_by_weight),
        "num_custom_products": int(num_custom_products),
        "total_weight": float(total_weight),
        "storebranch_id": int(storebranch_id),
    }


def transportation_input_max(order_1_info: pd.DataFrame, order_2_info: pd.DataFrame, origin_point_type: str) -> Dict[str, Any]:
    """
    Returns input for transportation estimation.
    """
    city_name = order_1_info["city_name"]
    store_name = order_1_info["store_name"]
    day_of_month = order_1_info["day_of_month"]
    day_of_week = order_1_info["day_of_week"]
    promise_hour = order_1_info["promised_datetime"].hour
    on_demand = 0
    num_products_by_unit = order_1_info["n_products_by_unit"] + order_2_info["n_products_by_unit"]
    num_products_by_weight = order_1_info["n_products_by_weight"] + order_2_info["n_products_by_weight"]
    num_custom_products = order_1_info["n_custom_products"] + order_2_info["n_custom_products"]
    total_weight = order_1_info["total_weight"] + order_2_info["total_weight"]
    storebranch_id = order_1_info["store_branch_id"]

    if origin_point_type == "BRANCH":
        origin_lat = order_1_info["branch_location"].y
        origin_lon = order_1_info["branch_location"].x
        destination_lat = order_1_info["customer_location"].y
        destination_lon = order_1_info["customer_location"].x
    else:
        origin_lat = order_1_info["customer_location"].y
        origin_lon = order_1_info["customer_location"].x
        destination_lat = order_2_info["customer_location"].y
        destination_lon = order_2_info["customer_location"].x

    return {
        "city": city_name,
        "store": store_name,
        "day_of_month": int(day_of_month),
        "day_of_week": day_of_week,
        "promise_hour": promise_hour,
        "on_demand": on_demand,
        "num_products_by_unit": int(num_products_by_unit),
        "num_products_by_weight": int(num_products_by_weight),
        "num_custom_products": int(num_custom_products),
        "total_weight": float(total_weight),
        "origin_point_type": origin_point_type,
        "storebranch_id": int(storebranch_id),
        "origin_lat": origin_lat,
        "origin_lng": origin_lon,
        "destination_lat": destination_lat,
        "destination_lng": destination_lon,
    }


def refresh_execution_potential_pairs(execution_potential_pairs, global_matched_pairs, suspended_orders_dict, time_stamp):

    global_matched_orders = set()
    for o1, o2 in global_matched_pairs:
        global_matched_orders.update({o1,o2})


    new_execution_potential_pairs = {}
    for t, pairs in execution_potential_pairs.items():
        # if t <= time_stamp:
        #     continue
        new_pairs = []
        for pair in pairs:
            o1, o2 = pair
            if o1 not in global_matched_orders and o2 not in global_matched_orders:
                if o1 not in suspended_orders_dict.keys() or t not in suspended_orders_dict[o1]:
                    if o2 not in suspended_orders_dict.keys() or t not in suspended_orders_dict[o2]:
                        new_pairs.append(pair)


        new_execution_potential_pairs[t] = new_pairs


    return new_execution_potential_pairs


def get_mp_parameter(simulation_values: Dict[str, Any], op_zone_mp_settings: Dict[str, Any], param_name: str) -> Any:
    return simulation_values.get(param_name, op_zone_mp_settings.get(param_name, constants.DEFAULT_OP_ZONE_MP_SETTINGS[param_name]))


def get_time_estimations(zone_id: int, date: str, orders_dict: Dict, pass_hard_checks):

    print("    > Get total time estimations... ", end='')
    try:
        # Load both total_time and part_time_estimations
        with open(f"{DATA_DIR}/sim_resources/all_total_time_estimations/{zone_id}/all_total_time_estimations_{zone_id}_{date}.pickle", "rb",) as handle:
            total_time_estimations = pickle.load(handle)

        with open(f"{DATA_DIR}/sim_resources/part_time_estimations/{zone_id}/part_time_estimations_{zone_id}_{date}.pickle", "rb",) as handle:
            part_time_estimations = pickle.load(handle)

        # We have to check if the pairs passed in pass_hard_checks are ALL present in the saved estimations
        # otherwise, we should query the estimator for the missing ones:

        assert set(total_time_estimations.keys()) == set(part_time_estimations.keys()), 'Keys for estimations not matching.'
        loaded_pairs = set(total_time_estimations.keys())
        required_pairs = set(pass_hard_checks)

        if not required_pairs.issubset(loaded_pairs):
            print('Missing orders in loaded data. Querying Estimator...', end='')
            # If not all pairs are present in the loaded ones, then we go to the Estimator
            missing_pairs = list(required_pairs.difference(loaded_pairs))
            try:
                total_time_estimations_aux, part_time_estimations_aux = get_total_time_estimations_max(orders_dict, missing_pairs)

                # Update loaded dictionaries
                total_time_estimations.update(total_time_estimations_aux)
                part_time_estimations.update(part_time_estimations_aux)

                # Update stored pickles
                dump_pickle(total_time_estimations, f'sim_resources/all_total_time_estimations/{zone_id}', 'all_total_time_estimations', (zone_id,), (date,))
                dump_pickle(part_time_estimations, f'sim_resources/part_time_estimations/{zone_id}', 'part_time_estimations', (zone_id,), (date,))

            except requests.exceptions.ConnectionError:
                print('Failed. Unable to connect with Estimator')
                raise

        print('OK')

    except FileNotFoundError:
        print('Files not found. Quering Estimator... ', end='')
        try:
            # intento ir a buscar las estimaciones, pero si me faltan para algunos pedidos tengo que ir a buscarlas al modelo (rellenar)
            total_time_estimations, part_time_estimations = get_total_time_estimations_max(orders_dict, pass_hard_checks)

            dump_pickle(total_time_estimations, f'sim_resources/all_total_time_estimations/{zone_id}', 'all_total_time_estimations', (zone_id,), (date,))
            dump_pickle(part_time_estimations, f'sim_resources/part_time_estimations/{zone_id}', 'part_time_estimations', (zone_id,), (date,))

            print('OK')
        except requests.exceptions.ConnectionError:
            print('Failed. Unable to connect with Estimator.')
            raise

    return total_time_estimations, part_time_estimations

