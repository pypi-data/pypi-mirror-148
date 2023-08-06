"""
This module contains functions required for the Data Extraction process of the MP Simulator
"""

import datetime
import os
from os.path import exists
import pickle
from typing import Any

import numpy as np
import pandas as pd
import pandas.io.sql as sqlio
import psycopg2
from .data_extraction_queries import *
from .datadog_utils import *
from .athena_utils import AthenaWrapper
from .. import constants

SUPERPAL_USER = os.environ.get("SUPERPAL_USER")
SUPERPAL_PASSWORD =  os.environ.get("SUPERPAL_PASSWORD")
SEGMENT_PASSWORD = None
MP_SIMULATOR_ROOT_DIR = constants.MP_SIMULATOR_ROOT_DIR
DATA_DIR = constants.DATA_DIR


def create_dates_tuple(start: str, end: str) -> tuple:
    """
    Creates a set of dates based on the given day limits (both inclusive). Dates are returned
    inside a tuple, sorted, in yyyy-mm-dd string formatting.

    Parameters
    ----------
    start : str
            Start date in 'yyyy-mm-dd' format.
    end :   str
            End date in 'yyyy-mm-dd' format.

    Returns
    -------
    str_date_list: tuple
            Tuple containing the daily date strings.

    """

    datetime_list = pd.date_range(start, end).to_pydatetime()
    str_date_list = [d.strftime("%Y-%m-%d") for d in datetime_list]

    return tuple(str_date_list)


def create_zone_ids_tuple(zone_ids_list: list) -> tuple:  # This can now be deleted. No need for it.
    """
    Generate a tuple from the given zone ID list.
    """
    if len(zone_ids_list)==1:
        return tuple(zone_ids_list)  # TODO Check why do we need to repeat the id in order for it to work. Check with Superpal
    else:
        return tuple(zone_ids_list)  # I changed the name from zone_id_tuple to zone_ids_tuple


def query_to_table(query: str, db: str) -> pd.DataFrame:
    """
    Send query to Postgres and transform it into a pandas DF. Queries can be sent
    to Segment Warehouse (segment) or Superpal replica 4 (superpal).  'User' and both
    passwords should be changed at the start of this file.

    Parameters
    ----------
    query (str):
        String containing the SQL query.
    db (str):
        Database to direct the query. Can be any from ['segment', 'superpal'].

    Returns
    -------
    table (pd.DataFrame):
        Result table as a pandas.DataFrame object.
    """

    if db == "segment":
        conn = psycopg2.connect(
            database="segment_warehouse",
            user=SUPERPAL_USER,
            password=SEGMENT_PASSWORD,
            host="dbproxy-warehouse.internal.cornershop.io",
            port=5432,
        )
    else:
        conn = psycopg2.connect(
            database="superpal",
            user=SUPERPAL_USER,
            password=SUPERPAL_PASSWORD,
            host="dbproxy-replica04.internal.cornershop.io",
            port=5432,
        )
    try:
        table = sqlio.read_sql_query(query, conn)
    except psycopg2.errors.InsufficientPrivilege:
        print('Query failed. Insufficient privileges.')
        return
    conn = None

    return table


def dump_pickle(obj, subpath: str, data_kind: str, zone_ids_tuple: tuple=None, dates_tuple: tuple=None):
    """
    Pickles the given object into its corresponding directory following input from user.
    Pickled objects are saved with a '.pickle' extension.

    Parameters
    ----------
    obj (Any):
        The object to be pickled.
    subpath (str):
        The 'data' directory subfolder where the data corresponds.
    data_kind (str):
        Keyword with the kind of data the object holds (in order to sort into its corresponding subdirectory)
    zone_ids_tuple (tuple, optional):
        Tuple containing the Zone IDs for identification.
    dates_tuple (tuple, optional):
        Tuple containing the data's date range for identification.
    """
    if zone_ids_tuple is not None:
        zone_ids_str = '_'.join([str(id) for id in zone_ids_tuple])
    else:
        zone_ids_str = ''

    if dates_tuple is not None:
        if len(dates_tuple) > 1:
            dates_str = '_'.join([min(dates_tuple), max(dates_tuple)])
        else:
            dates_str = str(dates_tuple[0])
    else:
        dates_str = ''

    # save_dir = f"{MP_SIMULATOR_ROOT_DIR}/data/{subpath}"
    save_dir = f"{DATA_DIR}/{subpath}"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    try:
        with open(f"{DATA_DIR}/{subpath}/{data_kind}_{zone_ids_str}_{dates_str}.pickle", 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    except:
        print(f'Dump unsuccesful for f"{DATA_DIR}/{subpath}/{data_kind}_{zone_ids_str}_{dates_str}.pickle"')
        raise


def load_pickle(subpath: str, data_kind: str, zone_ids_tuple: tuple=None, dates_tuple: tuple=None, ext='.pickle') -> Any:
    """
    Unpickles the specified data object.

    Parameters
    ----------
    subpath (str):
        The 'data' directory subfolder where the data corresponds. [INSERT AVAILABLE OPTIONS]
    data_kind (str):
        Keyword with the kind of data the object holds (in order to sort into its corresponding subdirectory)
    zone_ids_tuple (tuple, optional):
        Tuple containing the Zone IDs for identification.
    dates_tuple (tuple, optional):
        Tuple containing the data's date range for identification.
    """

    if zone_ids_tuple is not None:
        zone_ids_str = '_'.join([str(id) for id in zone_ids_tuple])
    else:
        zone_ids_str = ''

    if dates_tuple is not None:
        if len(dates_tuple) > 1:
            dates_str = '_'.join([min(dates_tuple), max(dates_tuple)])
        else:
            dates_str = str(dates_tuple[0])
    else:
        dates_str = ''

    full_path = f"{DATA_DIR}/{subpath}/{data_kind}_{zone_ids_str}_{dates_str}{ext}"
    try:
        with open(full_path, 'rb') as handle:
            obj = pickle.load(handle)
    except FileNotFoundError:
        print(f'File {full_path} not found.')
        return

    return obj


def get_filepath(subpath: str, data_kind: str, zone_ids_tuple: tuple=None, dates_tuple: tuple=None, ext='.pickle') -> str:
    """
    Returns the relative filepath to the required pickle (by default), or file.
    """
    if zone_ids_tuple is not None:
        zone_ids_str = '_'.join([str(id) for id in zone_ids_tuple])

    if dates_tuple is not None:
        dates_str = '_'.join([min(dates_tuple), max(dates_tuple)])

    return f"{DATA_DIR}/{subpath}/{data_kind}_{zone_ids_str}_{dates_str}{ext}"


def extract_order_details(mpd_precandidates_id_list: list, max_batch_size=1000):
    """
    Batch (if necessary) the extraction of the order detail relative to the order IDs passed to the function.
    Batches max size is determined by `max_batch_size` and the IDs get divided into equal parts.
    """

    n_ids = len(mpd_precandidates_id_list)

    n_batches = calculate_batches(n_ids, max_batch_size)
    len_batches = int(len(mpd_precandidates_id_list) / n_batches) + 1

    order_details_df = pd.DataFrame()
    extracted_ids = []
    wrapper = AthenaWrapper(schema_name='cornershop_warehouse')
    for i in range(n_batches):
        order_list_i = mpd_precandidates_id_list[i*len_batches:(i+1)*len_batches]
        all_order_ids_string = str(tuple(order_list_i))
        # try
        order_details_df_aux = athena_query_to_table(athena_order_detail_query(
            ids_tuple_str=all_order_ids_string),
            db='na',
            wrapper=wrapper
            )
        print(f"{round(100*(i+1/n_batches))}% Done")
        order_details_df = pd.concat([order_details_df, order_details_df_aux])
    return order_details_df


def split_data_by_zone_date(df_dict: dict, zone_ids_tuple: tuple, dates_tuple: tuple):
    """
    Split and store the data given in `df_dict` into corresponding directories by zone.

    Parameters
    ==========
    df_dict (dict):
        `df_dict` keys must be the names of the 'data_kind', and values the actual DataFrames. For example:
        `df_dict = {'order_details': order_details_df, 'daily_zone_mpd_stats': daily_zone_mpd_stats_df}`
    """

    for zone_id in zone_ids_tuple:
        for date in dates_tuple:
            for data_kind, df in df_dict.items():
                if df is not None:
                    try:
                        data_subset = df[(df.customer_zone_id == zone_id)&(df.date == date)]
                    except AttributeError:  # Some "datas" have zone_id others have customer_zone_id
                        data_subset = df[(df.zone_id == zone_id)&(df.date == date)]

                    zone_date_subpath = f'{DATA_DIR}/sim_resources/{data_kind}/{zone_id}'

                    if not os.path.exists(zone_date_subpath):
                        os.makedirs(zone_date_subpath)

                    save_path = f'{zone_date_subpath}/{data_kind}_{zone_id}_{date}.pickle'

                    if data_kind != 'om_execution_times':
                        data_subset.to_pickle(save_path)
                    else:
                        om_execution_times_list = list(list(np.sort(data_subset['timestamp'].tolist())))
                        dump_pickle(om_execution_times_list, f'sim_resources/{data_kind}/{zone_id}', data_kind, (zone_id, ), (date, ))

            print(f'{zone_id} - {date}: split ok.')


def get_logs(query_name: str, zone_ids_tuple: tuple, dates_tuple: tuple, index=None):
    """
    Queries DataDog API for the specified data and stores them in `/data/raw/logs`.

    Parameters
    ==========
    query_name : str
        `{'mpd_matches', 'om_executions'}` depending on what data the user wants.
    """

    log_filter_zone_id_str = ' OR '.join([str(id) for id in zone_ids_tuple])

    if query_name == 'mpd_matches':
        query = 'Multipicking Order package found'
    elif query_name == 'om_executions':
        query = 'Multipicking candidate Orders'

    filtered_query = f'{query} @data.zone_id:({log_filter_zone_id_str})'

    prefix_zone_ids, prefix_dates = get_zone_date_suffix(zone_ids_tuple, dates_tuple)
    prefix = f'{DATA_DIR}/raw/logs/{query_name}/{query_name}_{prefix_zone_ids}_{prefix_dates}'

    date_from = datetime.datetime.strptime(min(dates_tuple), "%Y-%m-%d").strftime("%Y-%m-%dT%H:%M:%SZ")
    date_to = datetime.datetime.strptime(max(dates_tuple), "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59Z")

    print(f'Getting logs for {filtered_query}...')
    print('-'*30)

    tries = full_logs(query=filtered_query, date_from=date_from, date_to=date_to, next_log_id=not None, prefix=prefix, index = index)


def _logs_to_mpd_matches(zone_ids_tuple: tuple, dates_tuple: tuple) -> pd.DataFrame:
    """
    Transform MPD Matches logs to DataFrame form for the given zone and dates.
    """

    prefix_zone_ids, prefix_dates = get_zone_date_suffix(zone_ids_tuple, dates_tuple)

    prefix = f'{DATA_DIR}/raw/logs/mpd_matches/mpd_matches_{prefix_zone_ids}_{prefix_dates}'

    try:
        logs_list = open_data_dog_logs(prefix)
    except FileNotFoundError:
        print(f'Logs not found for {prefix}')
        return

    time_zone_dict = get_time_zone_dict()

    log_data_list = []
    for log in logs_list:
        zone_id = log['content']['attributes']['data']['zone_id']
        time_zone = time_zone_dict[zone_id]
        timestamp = pd.to_datetime(log['content']['timestamp']).tz_convert(time_zone).tz_localize(None)
        orders = str(log['content']['attributes']['data']['orders'])
        log_data_list.append([zone_id, timestamp, orders])

    mpd_matches_df = pd.DataFrame(log_data_list, columns = ['zone_id', 'timestamp', 'orders'])
    mpd_matches_df['date'] = mpd_matches_df['timestamp'].dt.date.astype('str')

    return mpd_matches_df


def get_conversion_by_hour(zone_ids_tuple: tuple, dates_tuple: tuple):
    """
    Return a dictionary containing a probability between 0 and 1 (value), for each hour of the day (key)
    for each date.
    """

    mpd_matches_df = _logs_to_mpd_matches(zone_ids_tuple, dates_tuple)
    actual_mpd_pairs_df = load_pickle('raw/actual_mpd_pairs', 'actual_mpd_pairs', zone_ids_tuple, dates_tuple)

    issue_cases = []
    for zone_id in zone_ids_tuple:
        for date in dates_tuple:
            try:  # Should check what cases are the ones that raise exceptions (maybe keyerror exceptions the main reason?)
                # Filter logs for zone and date
                logs_df = mpd_matches_df[(mpd_matches_df.zone_id==zone_id) & (mpd_matches_df.date==date)].copy()
                print('logs_df len:',len(logs_df))
                # Reassure orders col is str ? (should already be though)
                logs_df['orders'] = logs_df['orders'].astype('str')

                # Get last recorded match for each 'orders' entry. NOTE: up to this moment, orders is a string not a set, so '['A', 'B']' != '['B', 'A']'
                g_data = logs_df[['orders', 'timestamp']].groupby('orders', as_index=False).max().rename(columns = {'timestamp': 'last_matched'})
                data = logs_df.merge(g_data, on = 'orders')[['orders', 'timestamp', 'last_matched']]

                # Flag those records where we have the 'last match' between two orders
                data['is_last'] = np.where(data.timestamp==data.last_matched, True, False)

                # Now we check what batches of MP were actually done during that day
                table_mp_i = actual_mpd_pairs_df[(actual_mpd_pairs_df.customer_zone_id==zone_id) & (actual_mpd_pairs_df.date.astype(str)==date)].copy()

                # Format orders just like we have in the 'data' DataFrame (as list-like string), and include reversed case. NOTE: Why not store a set in orders straight away?
                table_mp_i['orders'] = table_mp_i.apply(lambda x: str([x.order_id_1, x.order_id_2]), axis=1)
                table_mp_i['switched_orders'] = table_mp_i.apply(lambda x: str([x.order_id_2, x.order_id_1]), axis=1)

                # Generate a set (duplicates get dropped) with all pairs actually assigned throughout the day
                real_batches = set(list(table_mp_i.orders)+list(table_mp_i.switched_orders))

                # Get the set of total pairs generated by the OM (even the ones that didn't get assigned in the end)
                om_pairs = set(logs_df.orders)

                non_matched_pairs = om_pairs-real_batches
                matched_pairs = om_pairs.intersection(real_batches)

                # Flag OM matches (the order pair) whether they were fulfilled as MP or not
                data['was_matched'] = data.orders.isin(real_batches)
                # Flag OM matches (the order pair, but also specifically the moment) that were fulfilled as MP
                data['was_matched_in_this_moment'] = data['is_last'] & data['was_matched']

                # Extract hour from the timestamp for grouping
                data['hour'] = data['timestamp'].dt.hour

                # Extract "probabilty of converting an OM match into an actual MP assignment" information from the data
                mean_probability = data.groupby('hour', as_index=False).mean()  # NOTE: What should we do with slots that don't have enough (0 or only a few) data points?

                conversion_by_hour_dict = {}
                available_hours = list(mean_probability.hour)

                for i in range(0,24):
                    if i not in available_hours:
                        conversion_by_hour_dict[i] = 0
                    else:
                        conversion_by_hour_dict[i] = list(mean_probability[mean_probability.hour==i].was_matched_in_this_moment)[0]

                dump_pickle(conversion_by_hour_dict, f'sim_resources/conversion_by_hour/{zone_id}', 'conversion_by_hour', (zone_id, ), (date, ))

                print(f'Conversion by hour pickled for: {zone_id} - {date}')

            except ValueError:
                print(f'Error: Zone {zone_id} Date {date} conversion by hour dict not created.')
            except BaseException as err:
                print(f'Error in {zone_id}-{date}: {type(err)}: {err}')
                explain_exception(err)
                issue_cases.append((zone_id, date))
                raise

            if len(issue_cases) > 0:
                print('Issue cases:', issue_cases)


def logs_to_om_executions(zone_ids_tuple: tuple, dates_tuple: tuple):
    """
    Transform OrderMatcher execution logs into a DataFrame and store it for simulator use.
    """

    prefix_zone_ids, prefix_dates = get_zone_date_suffix(zone_ids_tuple, dates_tuple)

    prefix = f'{DATA_DIR}/raw/logs/om_executions/om_executions_{prefix_zone_ids}_{prefix_dates}'

    try:
        om_execution_logs = open_data_dog_logs(prefix)
    except FileNotFoundError:
        print(f'No logs found for "raw/logs/om_executions/om_executions_{prefix_zone_ids}_{prefix_dates}".')
        return

    log_data_list = []
    complicated_zones = []

    for log in om_execution_logs:
        host = log['content']['host'][:29]
        if host != 'celery-multipicking-scheduler':
            continue  # TODO: what's this for?
        content = log['content']
        zone_id = content['attributes']['data']['zone_id']
        timestamp = content['timestamp']
        log_data_list.append([zone_id, timestamp])

    om_executions_df = pd.DataFrame(log_data_list, columns=['zone_id', 'timestamp'])

    time_zone_dict = get_time_zone_dict()

    om_executions_df = om_executions_df[om_executions_df.zone_id.isin(zone_ids_tuple)]
    om_executions_df['timestamp'] = pd.to_datetime(om_executions_df['timestamp'])
    om_executions_df['timezone'] = om_executions_df['zone_id'].map(time_zone_dict)
    om_executions_df['timestamp'] = om_executions_df.apply(lambda x: x.timestamp.tz_convert(x.timezone).tz_localize(None), axis = 1)
    om_executions_df['date'] = om_executions_df['timestamp'].dt.date.astype('str')

    df_dict = {'om_execution_times':om_executions_df}
    split_data_by_zone_date(df_dict, zone_ids_tuple, dates_tuple)


def get_zone_date_suffix(zone_ids_tuple: tuple, dates_tuple: tuple) -> tuple:
    """
    Transform the zone IDs and dates tuple into strings for adding to filename strings.
    """
    suffix_zone_ids = '_'.join([str(id) for id in zone_ids_tuple])

    if len(dates_tuple) == 1:
        suffix_dates = str(dates_tuple[0])
    else:
        suffix_dates = '_'.join([dates_tuple[0], dates_tuple[-1]])

    return suffix_zone_ids, suffix_dates


def get_time_zone_dict():
    """
    Return a dictionary with each zone as a key, and their corresponding timezone.
    e.g. 'America/Santiago'.
    """
    try:
        op_zone_data = load_pickle('', 'op_zone_data')
        return dict(zip(op_zone_data.zone_id, op_zone_data.timezone))
    except FileNotFoundError:
        print('Timezone Dict error: op_zone_data.pickle not found in "data" directory. Now proceeding to fetch from Superpal...')
        op_zone_data = query_to_table(opzone_mp_settings_parameter_query(), db='superpal')
        print('Done!')
        dump_pickle(op_zone_data, '', 'op_zone_data')
        return dict(zip(op_zone_data.zone_id, op_zone_data.timezone))


def extract_raw(zone_ids_tuple: tuple, dates_tuple: tuple):
    """
    Extract and pickle for each of the required raw data inputs which will be transformed into simulator input.
    """

    # Actual MPD matched pairs
    if not exists(get_filepath('raw/actual_mpd_pairs', 'actual_mpd_pairs', zone_ids_tuple, dates_tuple)):
        actual_mp_pairs_df = query_to_table(query=actual_mpd_pairs_query(dates_tuple, zone_ids_tuple), db='superpal')  # Using one liner (and new utils files)
        dump_pickle(actual_mp_pairs_df, 'raw/actual_mpd_pairs', 'actual_mpd_pairs', zone_ids_tuple, dates_tuple)
        print('Actual MPD pairs: Done!')
    else:
        print('Actual MPD pairs: Already exist')

    # Daily zone %MPD stats
    if not exists(get_filepath('raw/daily_zone_mpd_stats', 'daily_zone_mpd_stats', zone_ids_tuple, dates_tuple)):
        mpd_stats_df = query_to_table(query=daily_zone_mpd_stats_query(dates_tuple, zone_ids_tuple), db='superpal')  # Using one liner (and new utils files)
        dump_pickle(mpd_stats_df, 'raw/daily_zone_mpd_stats', 'daily_zone_mpd_stats', zone_ids_tuple, dates_tuple)
        print('Daily %MPD Stats: Done!')
    else:
        print('Daily %MPD Stats: Already exist')

    # MPD Precandidate orders
    if not exists(get_filepath('raw/mpd_precandidate_orders', 'mpd_precandidate_orders', zone_ids_tuple, dates_tuple)):
        mpd_precandidates_df = query_to_table(query=mpd_precandidates_query(dates_tuple, zone_ids_tuple), db='superpal')
        dump_pickle(mpd_precandidates_df, 'raw/mpd_precandidate_orders', 'mpd_precandidate_orders', zone_ids_tuple, dates_tuple)
        print('MPD Precandidate orders: Done!')
    else:
        mpd_precandidates_df = load_pickle('raw/mpd_precandidate_orders', 'mpd_precandidate_orders', zone_ids_tuple, dates_tuple)
        print('MPD Precandidate orders: Already exist')

    # MPD Precandidate order details
    order_details_df = extract_order_details(list(mpd_precandidates_df.id), max_batch_size=3000)
    dump_pickle(order_details_df, 'raw/order_details', 'order_details', zone_ids_tuple, dates_tuple)
    print('MPD Precandidates order details: Done!')


def calculate_batches(n_ids: int, max_batch_size=2000) -> int:
    """
    Calculates number of batches given a number of ids the user needs to extract for Order detail.
    """
    return (n_ids // max_batch_size) + (n_ids % max_batch_size > 0)


def explain_exception(ex: BaseException):
    trace = []
    tb = ex.__traceback__
    while tb is not None:
        trace.append({
            "filename": tb.tb_frame.f_code.co_filename,
            "name": tb.tb_frame.f_code.co_name,
            "lineno": tb.tb_lineno
        })
        tb = tb.tb_next
    print(str({
        'type': type(ex).__name__,
        'message': str(ex),
        'trace': trace
    }))


def athena_query_to_table(query: str, db='cornershop_warehouse', wrapper=None) -> pd.DataFrame:

    if not isinstance(wrapper, AthenaWrapper):
        wrapper = AthenaWrapper(db)

    result_df = wrapper.execute(query)

    # Handle time fields (they come with the timezone appended at the end)
    time_cols = ['picking_assignable_time','min_delivery_time','promised_datetime']
    for col in time_cols:
        result_df[col] = pd.to_datetime(result_df[col].apply(lambda x: x[:23]))

    # Orders without custom products have nan
    fill_dict = {
        'n_custom_products':0
    }
    result_df.fillna(value=fill_dict, inplace=True)

    # Change float dtype to int
    int_cols = ['order_id',
        'products_ordered',
        'city_id',
        'customer_zone_id',
        'store_id',
        'store_branch_id',
        'n_products_by_unit',
        'n_products_by_weight',
        'unique_categories',
        'unique_top_level_categories',
        'n_custom_products']
    result_df[int_cols] = result_df[int_cols].astype(int)

    return result_df


def athena_extract_order_details(mpd_precandidates_id_list: list):
    all_order_ids_string = str(tuple(mpd_precandidates_id_list))
    return athena_query_to_table(athena_order_detail_query(all_order_ids_string))