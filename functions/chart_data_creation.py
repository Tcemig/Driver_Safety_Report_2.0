import pandas as pd
import datetime as dt
from dateutil.relativedelta import relativedelta
import smartsheet
from fuzzywuzzy import fuzz
import os
from dotenv import load_dotenv

load_dotenv()

SMARTSHEETS_ACCESS_TOKEN = os.getenv('SMARTSHEETS_ACCESS_TOKEN')


import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.query import sqlite3_query

# map out group
custom_groups_dict = {
    0: 'COV',
    1: 'Linehaul',
    2: 'Contractor',
    3: 'Training',
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
    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)
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

    return weekly_counts_combined


def monthlyGroupPreformanceTable_data(ending_date_str, months_num):
    """
    This function generates the data for the monthly group performance table.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - relativedelta(months=months_num)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName'])

    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)
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
    
    return monthly_counts_combined


def weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num):
    """
    This function generates the data for the infractions total per category.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - dt.timedelta(days=days_num)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName', 'behaviorsName'])

    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)
    # Calculate the previous Saturday for each date
    df['week_start'] = df['recordDate'] - pd.to_timedelta((df['recordDate'].dt.weekday + 2) % 7, unit='d')
    # Format as string for easier grouping/plotting
    df['week_label'] = df['week_start'].dt.strftime('%Y-%m-%d')
        
    df['group'] = df.apply(map_group, axis=1)

    df = df[df['group'] != 'Trainer']

    weekly_counts_total = df.groupby(['week_label', 'group']).size().reset_index(name='event_size')

    weekly_counts_eventSize = df.groupby(['week_label', 'group', 'behaviorsName']).size().reset_index(name='event_size')

    return weekly_counts_total, weekly_counts_eventSize


def overviewProgramPerformance_data(ending_date_str):
    """
    This function generates the data for the overview program performance chart.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - dt.timedelta(days=168)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName'])

    # Map week by week backwards a week is saturaty to friday and create a new column labeling the week
    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)
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

    merged_df = merged_df.iloc[1:, :] # Remove first row as it can contain not a full week of data
    merged_df = merged_df.reset_index(drop=True)

    return merged_df


def covEventsAndIncidents_data(ending_date_str):
    """
    This function generates the data for the COV events and incidents chart.
    """
    # calculate the ending date
    starting_date = dt.datetime.strptime(ending_date_str, "%Y-%m-%d") - relativedelta(months=5)
    starting_date_str = starting_date.strftime("%Y-%m-%d")

    df = sqlite3_query(ending_date_str, starting_date_str, ['score', 'recordDate', 'vehicleName', 'groupName', 'driverName', 'behaviorsName'])

    # Map week by week backwards a week is saturaty to friday and create a new column labeling the week
    df['recordDate'] = pd.to_datetime(df['recordDate'], errors='coerce', utc=True)
    if isinstance(df['recordDate'].dtype, pd.DatetimeTZDtype):
        df['recordDate'] = df['recordDate'].dt.tz_localize(None)
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

    return weekly_counts_combined


def Pulling_SmartSheet_data():

    smart = smartsheet.Smartsheet(access_token=SMARTSHEETS_ACCESS_TOKEN)


    def simple_sheet_to_dataframe(sheet):
        col_names = [col.title for col in sheet.columns]
        rows = []
        for row in sheet.rows:
            cells = []
            for cell in row.cells:
                cells.append(cell.value)
            rows.append(cells)
        data_frame = pd.DataFrame(rows, columns=col_names)
        return(data_frame)

    def sheet_to_dataframe(sheet_name):

        response = smart.Sheets.list_sheets()       # Call the list_sheets() function and store the response object
        for s in response.data:
            if s.name == sheet_name:
                sheetId = s.id
                break
        sheet = smart.Sheets.get_sheet(sheetId)     # Load the sheet by using its ID

        df = simple_sheet_to_dataframe(sheet)

        # df = df[(df['Date of Incident'] >= Start_Week) & (df['Date of Incident'] <= End_Week)]

        return df

    df = pd.DataFrame()

    for sheet_name in ['Incident Tracker 2025', 'Incident Tracker 2024']:

        try:
            individual_sheet_df = sheet_to_dataframe(sheet_name)
            df = pd.concat([df, individual_sheet_df], ignore_index=True)
        except Exception as e:
            print(f"Error processing sheet {sheet_name}: {e}")
            continue

    # Convert 'Date of Incident' to datetime
    if 'Date of Incident' in df.columns:
        df['Date of Incident'] = pd.to_datetime(df['Date of Incident'], errors='coerce')

    df = df.sort_values(by='Date of Incident', ascending=False)

    df = df[df['Fault'].notna()]
    df = df[df['Fault'].str.contains('Fault', na=False)]
    df = df[df['Vehicle Type'].str.contains('COV', na=False)]

    return df
