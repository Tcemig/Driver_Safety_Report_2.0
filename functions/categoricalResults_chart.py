import pandas as pd
import sqlite3
import datetime as dt
from dateutil.relativedelta import relativedelta

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.query import sqlite3_query

# map out group
custom_groups_dict = {
    0: 'COV',
    1: 'Linehaul',
    2: 'Contractor',
    3: 'Traning',
}

def map_group(row):
    group_name = row['groupName'] if row['groupName'] is not None else ""
    driver_name = row['driverName'] if row['driverName'] is not None else ""

    if any(x in group_name for x in ['Red-Cross', 'TCN', 'CEN']):
        return custom_groups_dict[2]
    elif 'Linehaul' in group_name:
        return custom_groups_dict[1]
    elif 'SoCal' in group_name:
        return custom_groups_dict[3]
    elif 'GG' in driver_name:
        return custom_groups_dict[2]
    elif 'Linehaul' in driver_name:
        return custom_groups_dict[1]
    else:
        return custom_groups_dict[0]


def infractionFrequencyChart_data(ending_date_str):
    """
    This function generates the data for the infraction frequency chart.
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
        
    df['group'] = df.apply(map_group, axis=1)

    weekly_counts_eventSize = df.groupby(['week_label', 'group']).size().reset_index(name='event_size')
    weekly_counts_groupSize = df.groupby(['week_label', 'group']).agg({'vehicleName': 'nunique'}).reset_index()
    weekly_counts_groupSize.rename(columns={'vehicleName': 'group_size'}, inplace=True)

    weekly_counts_combined = pd.merge(
        weekly_counts_eventSize,
        weekly_counts_groupSize,
        on=['week_label', 'group'],
        how='outer'
    )

    weekly_counts_combined['infractions_per_vehicle'] = (
        weekly_counts_combined['event_size'] / weekly_counts_combined['group_size']
    ).fillna(0)


    print(weekly_counts_combined)

    skip=1

# infractionFrequencyChart_data('2025-05-20')

def monthlyGroupPreformanceTable_data(ending_date_str):
    """
    This function generates the data for the monthly group performance table.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - relativedelta(months=3)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName'])

    df['recordDate'] = pd.to_datetime(df['recordDate'])
    # Calculate the previous Saturday for each date
    df['month_start'] = df['recordDate'] - pd.to_timedelta((df['recordDate'].dt.weekday + 2) % 7, unit='d')
    # Format as string for easier grouping/plotting
    df['month_label'] = df['month_start'].dt.strftime('%Y-%m')

    # map out group
    df['group'] = df.apply(map_group, axis=1)
    # Group by month and group, and count the number of events
    monthly_counts_eventSize = df.groupby(['month_label', 'group']).size().reset_index(name='event_size')
    monthly_counts_groupSize = df.groupby(['month_label', 'group']).agg({'vehicleName': 'nunique'}).reset_index()
    monthly_counts_groupSize.rename(columns={'vehicleName': 'group_size'}, inplace=True)
    monthly_counts_combined = pd.merge(
        monthly_counts_eventSize,
        monthly_counts_groupSize,
        on=['month_label', 'group'],
        how='outer'
    )
    monthly_counts_combined['infractions_per_vehicle'] = (
        monthly_counts_combined['event_size'] / monthly_counts_combined['group_size']
    ).fillna(0)
    
    print(monthly_counts_combined)


    skip=1

# monthlyGroupPreformanceTable_data('2025-05-20')

def infractionsTotalPerCategory(ending_date_str):
    """
    This function generates the data for the infractions total per category.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - dt.timedelta(days=168)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName', 'behaviorsName'])

    df['recordDate'] = pd.to_datetime(df['recordDate'])
    # Calculate the previous Saturday for each date
    df['week_start'] = df['recordDate'] - pd.to_timedelta((df['recordDate'].dt.weekday + 2) % 7, unit='d')
    # Format as string for easier grouping/plotting
    df['week_label'] = df['week_start'].dt.strftime('%Y-%m-%d')
        
    df['group'] = df.apply(map_group, axis=1)

    df = df[df['group'] != 'Trainer']

    weekly_counts_total = df.groupby(['week_label', 'group']).size().reset_index(name='event_size')
    print(weekly_counts_total)

    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    query = """
        SELECT *
        FROM lytxPriorityTwoCategories
    """
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    category_list = [row[1] for row in data]

    df = df[df['behaviorsName'].isin(category_list)]

    weekly_counts_eventSize = df.groupby(['week_label', 'group', 'behaviorsName']).size().reset_index(name='event_size')


# infractionsTotalPerCategory('2025-05-20')
