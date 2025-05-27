import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from functions.chart_data_creation import covEventsAndIncidents_data


def covEventsIncidents_tableData(ending_date_str):
    """
    This function generates the data for the monthly group performance table.
    It pulls the last 5 months of data and excludes the Training group.
    """

    # still need to pull at/no/shared fault data from the database
    
    covEI_data = covEventsAndIncidents_data(ending_date_str)
    covEI_data['week_label'] = pd.to_datetime(covEI_data['week_label'], errors='coerce')


    covEI_weekly_data = covEI_data.copy()
    covEI_weekly_data['week_label'] = covEI_weekly_data['week_label'].dt.strftime('%Y-%m-%d')
    covEI_weekly_data = covEI_weekly_data[covEI_weekly_data['week_label'].isin(covEI_weekly_data['week_label'].unique()[-5:])]  # Get the last 5 weeks of data
    covEI_weekly_data['Total VI At Fault'], covEI_weekly_data['Total VI No Fault'], covEI_weekly_data['Total VI Shared Fault'] = 0, 0, 0


    # Monthly Data
    covEI_monthly_data = covEI_data.copy()
    covEI_monthly_data['week_label'] = covEI_monthly_data['week_label'].dt.strftime('%Y-%m')
    covEI_monthly_data = covEI_monthly_data[covEI_monthly_data['week_label'].isin(covEI_monthly_data['week_label'].unique()[-5:])]  # Get the last 5 months of data

    covEI_monthly_data = covEI_monthly_data.groupby('week_label', as_index=False).agg({
        'group_size': 'mean',
        'event_size': 'sum',
    })
    covEI_monthly_data['group_size'] = covEI_monthly_data['group_size'].astype(int)
    covEI_monthly_data['event_size'] = covEI_monthly_data['event_size'].astype(int)

    covEI_monthly_data['Total VI At Fault'], covEI_monthly_data['Total VI No Fault'], covEI_monthly_data['Total VI Shared Fault'] = 0, 0, 0


    return covEI_weekly_data, covEI_monthly_data




