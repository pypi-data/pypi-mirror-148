from typing import Dict, Any, Set, Tuple
from random import shuffle
import gurobipy as gp
from gurobipy import GRB

def old_order_matcher(algorithm_parameters: Dict[str, Any]) -> Set[Tuple[int, int]]:
    """
    Returns matches of orders in a greedy way.
    """
    potential_pairs = algorithm_parameters["potential_pairs"]

    shuffle(potential_pairs)
    global_matches = set()
    matched_orders = set()
    for pair in potential_pairs:
        order_1, order_2 = pair
        if order_1 in matched_orders or order_2 in matched_orders:
            continue
        else:
            global_matches.add(pair)
            matched_orders.add(order_1)
            matched_orders.add(order_2)

    return global_matches


def sorted_distance_old_order_matcher(algorithm_parameters: Dict[str, Any]) -> Set[Tuple[int, int]]:
    """
    Returns matches of orders in a greedy way but first sorting them
    by distance between clients.
    """
    potential_pairs = algorithm_parameters["potential_pairs"]
    pair_intra_client_distance = algorithm_parameters["pair_intra_client_distance"]

    potential_pairs_intra_client_distance_dict = {p: pair_intra_client_distance[p] for p in potential_pairs}

    potential_pairs = [pair for pair, distance in sorted(potential_pairs_intra_client_distance_dict.items(), key=lambda item: item[1], reverse=True)]

    global_matches = set()
    matched_orders = set()
    for pair in potential_pairs:
        order_1, order_2 = pair
        if order_1 in matched_orders or order_2 in matched_orders:
            continue
        else:
            global_matches.add(pair)
            matched_orders.add(order_1)
            matched_orders.add(order_2)

    return global_matches


def sorted_utility_old_order_matcher(algorithm_parameters: Dict[str, Any]) -> Set[Tuple[int, int]]:
    """
    Returns matches of orders in a greedy way but first sorting them
    by distance between clients.
    """

    potential_pairs = algorithm_parameters["potential_pairs"]
    pair_utility = algorithm_parameters["potential_pairs_weight_dict"]
    total_saving_limit = algorithm_parameters['total_saving_limit']

    potential_pairs_utility = {p: pair_utility[p] for p in potential_pairs}

    if total_saving_limit >= 0:
        potential_pairs_utility = {k: v for k, v in potential_pairs_utility.items() if v >= total_saving_limit}

    potential_pairs = [k for k, v in sorted(potential_pairs_utility.items(), key=lambda item: item[1], reverse=True)]

    global_matches = set()
    matched_orders = set()
    for pair in potential_pairs:
        order_1, order_2 = pair
        if order_1 in matched_orders or order_2 in matched_orders:
            continue
        else:
            global_matches.add(pair)
            matched_orders.add(order_1)
            matched_orders.add(order_2)

    return global_matches


def sorted_utility_old_order_matcher_v2(algorithm_parameters: Dict[str, Any]) -> Set[Tuple[int, int]]:
    """
    Returns matches of orders in a greedy way but first sorting them
    by distance between clients.
    """

    potential_pairs = algorithm_parameters["potential_pairs"]
    pair_utility = algorithm_parameters["potential_pairs_weight_dict"]

    potential_pairs_utility = {k: v for k, v in pair_utility.items() if k in potential_pairs}

    global_matches = set()
    matched_orders = set()
    for pair in potential_pairs:
        order_1, order_2 = pair
        if order_1 in matched_orders or order_2 in matched_orders:
            continue
        else:
            global_matches.add(pair)
            matched_orders.add(order_1)
            matched_orders.add(order_2)

    return global_matches


def gurobi_max_matches(algorithm_parameters):
    """
    Returns matches of orders in a global optimized way.
    """
    potential_pairs = algorithm_parameters["potential_pairs"]

    orders = []
    for order_1, order_2 in potential_pairs:
        orders.append(order_1)
        orders.append(order_2)

    n_mp_dict = {2: {"name": "pairs", "indexes": [x for x in potential_pairs], "weight": 1}}

    model_mp = create_n_mp_max_matches(orders, n_mp_dict)

    model_mp.optimize()

    vars = model_mp.getVars()
    var_names = {var for var in vars if var.x == 1}

    gurobi_matched_pairs = [
        (int(var.VarName.split("[")[1].split(",")[0]), int(var.VarName.split("[")[1].split(",")[1].split("]")[0]))
        for var in var_names
    ]

    return gurobi_matched_pairs


def gurobi_with_costs(algorithm_parameters):
    """
    Returns matches of orders in a global optimized way.
    """
    potential_pairs = algorithm_parameters["potential_pairs"]
    potential_pairs_weight_dict = algorithm_parameters["potential_pairs_weight_dict"]

    # This part is to always prioritize maximizing the number of pairs of MP: we
    # give a big fixed to each utility so it is always better to make 2 matches instead of
    # 1 that is really good.

    # fixed_utility = sum(potential_pairs_weight_dict.values())
    # potential_pairs_weight_dict = {
    #     key: value + fixed_utility
    #     for key, value in potential_pairs_weight_dict.items()
    # }

    orders = []
    for pair in potential_pairs:
        order_1, order_2 = pair
        orders.append(order_1)
        orders.append(order_2)

    n_mp_dict = {2: {"name": "pairs", "indexes": [x for x in potential_pairs], "weight": potential_pairs_weight_dict}}

    model_mp = create_n_mp_with_costs(orders, n_mp_dict)

    model_mp.optimize()

    vars = model_mp.getVars()
    var_names = {var for var in vars if var.x == 1}

    gurobi_matched_pairs = [
        (int(var.VarName.split("[")[1].split(",")[0]), int(var.VarName.split("[")[1].split(",")[1].split("]")[0]))
        for var in var_names
    ]

    return gurobi_matched_pairs


def gurobi_intra_distance(algorithm_parameters):
    """
    Returns matches of orders in a global optimized way, minimzing the distance between clients.
    """

    M = 100000
    potential_pairs = algorithm_parameters["potential_pairs"]
    pair_intra_client_distance = algorithm_parameters["pair_intra_client_distance"]

    potential_pairs_intra_client_distance_dict = {p: M - pair_intra_client_distance[p] for p in potential_pairs}

    potential_pairs = [pair for pair, modified_distance in sorted(potential_pairs_intra_client_distance_dict.items(), key=lambda item: item[1], reverse=True)]


    orders = []
    for pair in potential_pairs:
        order_1, order_2 = pair
        orders.append(order_1)
        orders.append(order_2)


    n_mp_dict = {2: {"name": "pairs", "indexes": potential_pairs, "weight": potential_pairs_intra_client_distance_dict}}

    model_mp = create_n_mp_intra_distance(orders, n_mp_dict)

    model_mp.optimize()

    vars = model_mp.getVars()
    var_names = {var for var in vars if var.x == 1}

    gurobi_matched_pairs = [
        (int(var.VarName.split("[")[1].split(",")[0]), int(var.VarName.split("[")[1].split(",")[1].split("]")[0]))
        for var in var_names
    ]

    return gurobi_matched_pairs


# GUROBI MODEL GENERATION

def create_n_mp_max_matches(orders, n_mp_dict):
    """
    Create the optimization model.
    """
    # create model
    model = gp.Model("matching")

    # set parameters
    #model.setParam("OutputFlag", 0)
    model.setParam("MIPGap", 0.01)

    # create variables
    variable_dict = {}
    for values_dict in n_mp_dict.values():
        variable_dict[values_dict["name"]] = model.addVars(
            values_dict["indexes"],
            vtype=GRB.BINARY,
            name=values_dict["name"],
        )

    # create constraints
    for i in orders:
        i_tuples = {
            values_dict["name"]: [tup for tup in values_dict["indexes"] if i in tup]
            for values_dict in n_mp_dict.values()
        }

        lin_expr_i = ""
        for values_dict in n_mp_dict.values():
            lin_expr_i += gp.quicksum(variable_dict[values_dict["name"]][tup] for tup in i_tuples[values_dict["name"]])

        model.addConstr(lin_expr_i <= 1)

    # set objective function
    objective_function = ""
    for values_dict in n_mp_dict.values():
        objective_function += values_dict["weight"] * gp.quicksum(variable_dict[values_dict["name"]])

    model.setObjective(objective_function, GRB.MAXIMIZE)

    return model


def create_n_mp_with_costs(orders, n_mp_dict):
    """
    Create the optimization model.
    """
    # create model
    model = gp.Model("matching")

    # set parameters
    model.setParam("OutputFlag", 0)
    model.setParam("MIPGap", 0.01)

    # create variables
    variable_dict = {
        values_dict["name"]: model.addVars(
            values_dict["indexes"],
            vtype=GRB.BINARY,
            name=values_dict["name"],
        )
        for values_dict in n_mp_dict.values()
    }

    # create constraints
    for i in orders:
        i_tuples = {
            values_dict["name"]: [tup for tup in values_dict["indexes"] if i in tup]
            for values_dict in n_mp_dict.values()
        }

        lin_expr_i = ""
        for values_dict in n_mp_dict.values():
            lin_expr_i += gp.quicksum(variable_dict[values_dict["name"]][tup] for tup in i_tuples[values_dict["name"]])

        model.addConstr(lin_expr_i <= 1)

    model.update()

    objective_function = ""
    for values_dict in n_mp_dict.values():
        potential_pairs_cost = values_dict["weight"]
        objective_function = gp.quicksum(
            model.getVarByName(f"pairs[{pair[0]},{pair[1]}]") * potential_pairs_cost[pair]
            for pair in values_dict["indexes"]
        )

    model.setObjective(objective_function, GRB.MAXIMIZE)

    return model


def create_n_mp_intra_distance(orders, n_mp_dict):
    """
    Create the optimization model.
    """
    # create model
    model = gp.Model("matching")

    # set parameters
    model.setParam("OutputFlag", 0)
    model.setParam("MIPGap", 0.01)

    # create variables
    variable_dict = {
        values_dict["name"]: model.addVars(
            values_dict["indexes"],
            vtype=GRB.BINARY,
            name=values_dict["name"],
        )
        for values_dict in n_mp_dict.values()
    }

    # create constraints
    for i in orders:
        i_tuples = {
            values_dict["name"]: [tup for tup in values_dict["indexes"] if i in tup]
            for values_dict in n_mp_dict.values()
        }

        lin_expr_i = ""
        for values_dict in n_mp_dict.values():
            lin_expr_i += gp.quicksum(variable_dict[values_dict["name"]][tup] for tup in i_tuples[values_dict["name"]])

        model.addConstr(lin_expr_i <= 1)

    model.update()

    objective_function = ""
    for values_dict in n_mp_dict.values():
        potential_pairs_cost = values_dict["weight"]
        objective_function = gp.quicksum(
            model.getVarByName(f"pairs[{pair[0]},{pair[1]}]") * potential_pairs_cost[pair]
            for pair in values_dict["indexes"]
        )

    model.setObjective(objective_function, GRB.MAXIMIZE)

    return model