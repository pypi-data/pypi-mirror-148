"""
Set of functions to retrieve DataDog logs.
"""

import json
import numpy as np
import pandas as pd
import time

def get_all_logs(query, date_from='now - 7d', date_to='now', next_log_id=None, index=None):
    """
    Returns logs from DataDog
    """
    import requests
    # auxiliary
    logs = []
    # constants
    #datadog_api_key = "0dffcfa3c8c16a3cb208c7b61dac3e75"
    #datadog_app_key = "29b19ea42751a22085417be98aaee9766a2b8cc3"
    datadog_app_key = "14e62b49206b09867db16233665b4780e71c68aa"
    datadog_api_key = "3f2dd3b86b7a456353438f5ccfe8c6e8"

    url = "https://api.datadoghq.com/api/v1/logs-queries/list"
    # request args
    query_params = {
        "query": query,
        "time": {
            "from": date_from,
            "to": date_to
        },
        "limit": 1000
    }
    if index is not None:
        query_params.update({"index": index})

    print(query_params)

    while(True):
        if next_log_id is not None and isinstance(next_log_id, str):
            query_params.update({'startAt': next_log_id})
            print(f"> Querying with startAt: {next_log_id}")
        # do request
        response = requests.post(
            url,
            headers = {
                "DD-API-KEY": datadog_api_key,
                "DD-APPLICATION-KEY": datadog_app_key
            },
            json=query_params
        )
        try:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            remaining_requests = int(response.headers['X-RateLimit-Remaining'])
        except:
            print(response.headers)
        print(f'> Request finished with status code {response.status_code}.')
        try:  # delete after
            print(
                f'> {remaining_requests} requests remaining. Next reset in {reset_time/60:.2f} mins')
        except UnboundLocalError:
            print('> Unable to determine remaining requests.')
            reset_time = np.nan
            remaining_requests = np.nan
        print(f'> Request finished with status code {response.status_code}.')
        if response.status_code != 200:
            return logs, reset_time, remaining_requests, next_log_id
        response_json = response.json()
        # append new logs to logs list
        new_logs = response_json.get('logs')
        print(f'> Got {len(new_logs)} new logs.')
        logs += new_logs
        # decide if we should make another request
        if response_json.get('nextLogId') is not None:
            next_log_id = response_json.get('nextLogId')
        else:
            print(f'> Returning {len(logs)} logs.')
            next_log_id = None
            return logs, reset_time, remaining_requests, next_log_id
        try:
            reset_time = int(response.headers['X-RateLimit-Reset'])
            remaining_requests = int(response.headers['X-RateLimit-Remaining'])
        except:
            print(response.headers)


def timeout(sleeping_time):
    """ Sleeps a given time and print every minute the sleeping remaining time
    Args:
        sleeping_time(int): seconds to sleep.
    """
    while sleeping_time > 0:
        aux_sleeping_time = min(sleeping_time, 60)
        print(f"> Sleeping {sleeping_time/60:.2f} minutes...")
        time.sleep(aux_sleeping_time)
        sleeping_time -= aux_sleeping_time


def full_logs(query, date_from, date_to, next_log_id = not None, prefix='f', index = None):

    """
    Retrieves all logs corresponding to a query.  If the number of logs per hour is reached,
    this functions sleeps and waits until the remaining requests are restored, and then
    continues to get the remaining logs.
    """

    return_logs=[]
    tries = 0
    final_table = pd.DataFrame()

    while next_log_id is not None:
        logs, reset_time, remaining_requests, next_log_id = get_all_logs(
            query = query,
            date_from = date_from,
            date_to = date_to,
            next_log_id=next_log_id,
            index = index
        )
        return_logs += logs
        tries += 1
        print(
            f"Current nº tries : {tries},   Current length of logs {len(return_logs)}")
        # sleep if no remaining requests available
        if remaining_requests == 0:

            timeout(reset_time)



    with open(f"{prefix}.txt","w+") as fp:   #Pickling
        fp.write(json.dumps(return_logs))


    return tries


def open_data_dog_logs(prefix):

    with open(f"{prefix}.txt", "r") as fp:   # Unpickling
        logs_om = json.load(fp)

    return logs_om