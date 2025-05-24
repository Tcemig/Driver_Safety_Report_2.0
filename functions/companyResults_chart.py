import pandas as pd
import sqlite3
import datetime as dt
from dateutil.relativedelta import relativedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.query import sqlite3_query
from functions.categoricalResults_chart import map_group


def overviewProgramPerformance_data(ending_date_str):
    """
    This function generates the data for the overview program performance chart.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - dt.timedelta(days=168)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName'])

    # Map week by week backwards a week is saturaty to friday and create a new column labeling the week
    df['recordDate'] = pd.to_datetime(df['recordDate'])
    # Calculate the previous Saturday for each date
    df['week_start'] = df['recordDate'] - pd.to_timedelta((df['recordDate'].dt.weekday + 2) % 7, unit='d')
    # Format as string for easier grouping/plotting
    df['week_label'] = df['week_start'].dt.strftime('%Y-%m-%d')

    weekly_counts_eventSize = df.groupby(['week_label']).size().reset_index(name='event_size')
    weekly_counts_groupSize = df.groupby(['week_label']).agg({'vehicleName': 'nunique'}).reset_index()
    weekly_counts_groupSize.rename(columns={'vehicleName': 'group_size'}, inplace=True)

    # Merge the two DataFrames on the 'week_label' column
    merged_df = pd.merge(weekly_counts_eventSize, weekly_counts_groupSize, on='week_label')

    # Calculate the average event size per group size
    merged_df['avg_event_size'] = merged_df['event_size'] / merged_df['group_size']

    return merged_df

# overviewProgramPerformance_data('2025-05-20')


def covEventsAndIncidents(ending_date_str):
    """
    This function generates the data for the COV events and incidents chart.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - relativedelta(months=5)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName', 'behaviorsName'])

    # Map week by week backwards a week is saturaty to friday and create a new column labeling the week
    df['recordDate'] = pd.to_datetime(df['recordDate'])
    # Calculate the previous Saturday for each date
    df['week_start'] = df['recordDate'] - pd.to_timedelta((df['recordDate'].dt.weekday + 2) % 7, unit='d')
    # Format as string for easier grouping/plotting
    df['week_label'] = df['week_start'].dt.strftime('%Y-%m-%d')
    df['group'] = df.apply(map_group, axis=1)

    df = df[df['group'].isin(['COV'])]

    # Filter out rows where 'behaviorsName' is empty
    df = df[df['behaviorsName'] != '']

    weekly_counts_eventSize = df.groupby(['week_label', 'group']).size().reset_index(name='event_size')

    weekly_counts_groupSize = df.groupby(['week_label', 'group']).agg({'vehicleName': 'nunique'}).reset_index()
    weekly_counts_groupSize.rename(columns={'vehicleName': 'group_size'}, inplace=True)
    weekly_counts_combined = pd.merge(
        weekly_counts_eventSize,
        weekly_counts_groupSize,
        on=['week_label', 'group'],
        how='outer'
    )
    

    skip=1


covEventsAndIncidents('2025-05-20')


