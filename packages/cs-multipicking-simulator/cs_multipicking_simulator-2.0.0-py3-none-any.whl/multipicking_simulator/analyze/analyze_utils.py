import os
import pickle

import pandas as pd

from ..constants import DATA_DIR


def open_results(output_folder: str) -> pd.DataFrame:
        dir_path = os.path.join(DATA_DIR, f'results/{output_folder}')
        results_df = pd.DataFrame()
        for file in os.listdir(dir_path):
            full_path = os.path.join(dir_path, file)

            try:
                with open(full_path, 'rb') as f:
                    aux_df = pickle.load(f)
                results_df = pd.concat([results_df, aux_df])
            except:
                raise
        return results_df

if __name__ == '__main__':

    dir_path = "/Users/pablomahuzier/Documents/python_projects/cs-operational-simulator/cornershop-operational-simulator/mp_simulator/mp_simulator/data/results/mp_sim_execution_valpo"

    df = open_results(dir_path)

    g_df = df.groupby(['zone_id','date']).mean()

    cols = [
        "real_mp_pct",
        "simulation_mp_pct",
        "pct_multipicking_oos",
        "simulation_mp_pct_oos",
        "day_total_orders",
        "mp_potential_orders",
        "pct_mp_out_of_possible",
        "total_global_matches"
    ]
    print(g_df[cols])