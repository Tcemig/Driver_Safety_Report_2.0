import datetime as dt
import pandas as pd
import json

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.query import sqlite3_query

def rawLytxData(ending_date_str, behavior_list):
    """
    This function generates the raw Lytx data for the given ending date.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - dt.timedelta(days=6)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    print(f"Generating raw Lytx data from {starting_date_str} to {ending_date_str}")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName', 'behaviorsName'])

    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)

    df = df[df['driverName'].notna()]
    df = df[df['behaviorsName'].notna()]
    df = df[df['behaviorsName'] != '']
    df = df[df['behaviorsName'].str.lower().isin([b.lower() for b in behavior_list])]

    data_dict = {}

    for b in behavior_list:
        behavior_dict = {}
        for v in df['vehicleName'].unique():
            temp_df = df[df['vehicleName'] == v]
            behavior_count = temp_df['behaviorsName'].str.contains(b, case=False, na=False).sum()
            if behavior_count == 0:
                continue

            driver_associated = temp_df['driverName'].iloc[0]
            if driver_associated == 'Driver Unassigned':
                driver_associated = v
            behavior_dict[v] = {'count': int(behavior_count), 'driver': driver_associated}
            behavior_dict = {k: v for k, v in behavior_dict.items() if v['count'] > 0}
            behavior_dict = dict(sorted(behavior_dict.items(), key=lambda item: item[1]['count'], reverse=True))
            # keep only top 10
            behavior_dict = {k: v for k, v in list(behavior_dict.items())[:10]}
            # add to data_df
            data_dict[b] = behavior_dict

    # drop all tables with no values
    data_dict = {k: v for k, v in data_dict.items() if len(v) > 0}

    # sort data_dict by len of values
    data_dict = dict(sorted(data_dict.items(), key=lambda item: len(item[1]), reverse=True))

    with open('data_dict.json', 'w') as f:
        json.dump(data_dict, f, indent=4)

    return data_dict
