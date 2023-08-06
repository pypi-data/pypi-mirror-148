# Dispatcher (OR) Multipicking Simulator

The Multipicking Dispatcher Simulator is a tool, developed by the Dispatcher Operational-Research
team as a Python package, with the objective of supporting decision making in the process of setting Multipicking
Dispatcher parameters, by simulating estimates on a set of operational KPI.

## Prerequisites

Before you begin, besides the package you'll need to count with:
- Python 3 installed in your machine.
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) (developed with `version 4.6.1 (76265)`).
- An adequate image to mount the `estimator_v3` models.

## Installation

Eventually, you'll be able to install the `cs-dispatcher-multipicking-simulator` by running, in a Terminal instance:
```
pip install cs-dispatcher-multipicking-simulator
```

## Using the Multipicking Simulator

### 0. Run Docker container with `estimator_v3` models.

In runtime, the simulator will have to fetch estimation data which, in case of not existing
will be queried to the `estimator_v3` model you've started in Docker. To start the container
for the first time:

1. Go to the directory containing the models (probably named "estimator_v3" somewhere)
2. There should be a `serve_estimator.sh` file. Open up a terminal in this directory.
3. Execute the following command: ```bash serve_estimator.sh```. This should initialize the container.
4. Open Docker Desktop and check if the container is running.

These models are mounted in an image of `tensorflow-serving` which may not run properly in
Apple M1 machines. If you have this type of machine, please contact the maintainer in Slack (@Pelao)
for further help.

### 1. Setting de input Data Directory
Before running the simulator, you must set the directory where you are storing the required input data. This must be only done once (or whenever you want to update the directory). You can read the set data directory with the `mps.get_data_dir()` function.

```
import mp_simulator as mps

# If you haven't set the data directory yet:
data_dir_path = 'path/to/data/storage'
mps.set_data_dir(data_dir_path)
```
```
>> mps.get_data_dir()
'path/to/data/storage'
```
This directory will need to have the required data divided into the following directories and subfolders:
- `raw/`
    - `actual_mpd_pairs`
    - `daily_zone_mpd_stats`
    - `logs`
    - `mpd_precandidate_orders`
    - `order_details`
- `sim_resources/`
    - `conversion_by_hour`
    - `daily_zone_mpd_stats`
    - `om_execution_times`
    - `order_details`
    - `all_total_time_estimations`
    - `part_time_estimations`
- `results`

After setting the data directory the Simulator will know where to fetch the input data from.

### 2. Run simulations

First, we import the `simulation` function:

```
from mp_simulator import simulation
```
The `simulation` function receives a `dict` containing simulation parameters and their values.
At least, the user must pass three: `zone_id`, `date`, and `output_folder`.

```
simulation_parameters = {
    "zone_id": 129,
    "date": '2022-04-23',
    "output_folder": 'my_first_simulation'
}

simulation(simulation_parameters)
```

This will run a simulation, with
default zone `MULTIPICKING_SETTINGS` for zone `129` and date `2022-04-23`, and finally
save it in `results/my_first_simulation` located inside the set data directory.

If we want to simulate many days and zones (which surely will be the case), one way we
could use is to make calls to `simulation` iteratively:

```
# Set the zones, dates and parameters we want to use.
zones_list = [129, 130, 131]
dates_list = ['2022-04-23', '2022-04-24', '2022-04-25']
output_folder = 'results_folder_name'

# Initialize an empty list to store the simulation parameters
params_list = []

# Iteratively fill the list.
for zone_id in zones_list:

    for date in dates_list:

        simulation_params = {
            'zone_id': zone_id,
            'date': date,
            'output_folder': output_folder
        }

        params_list.append(simulation_params)

# Iteratively run the simulations.
for simulation_params in params_list:
    simulation(simulation_params)
```

### 3. Open results

To open the simulation results as a `pandas.DataFrame`, we can use the `open_results`
function from the `analyze` module:

```
from mp_simulator.analyze import open_results

results_df = open_results('results_folder_name')
```

## Quick start

- Install docker: https://docs.docker.com/get-docker/
- Run docker
- Open a terminal and run: 'docker-compose up'
- Open http://127.0.0.1:8888/?token=capacity on your browser
- Browse to 'mp_simulator/notebooks/capacity/simulation' to run your first multipicking simulation
- To stop the simulator just press “ctrl + c”

## Configurable parameters:
1. move_promised_n_hours (you can increase/decrease the promised time of orders),
2. move_picking_assignable_n_hours (you can increase/decrease the pat of orders),
3. instance (if you want to repeat a simulation manyy tmes with the same parameters),
4. max_delivery_distance,
5. max_branch_to_delivery_distance,
6. max_total_products,
7. delivery_slot_lower_buffer,
8. delivery_slot_upper_buffer,
9. picking_assignable_window_length,
10. picking_assignable_lower_limit_heuristic,
11. min_delivery_slots_overlap

Good luck!