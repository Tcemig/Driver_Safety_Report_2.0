from plotly.colors import n_colors
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.chart_data_creation import monthlyGroupPreformanceTable_data

def regionalGroupPerformance_tableData(ending_date_str, months_num):
    """
    This function generates the data for the regional group performance table.
    It pulls the last 3 months of data and excludes the Training group.
    """
    regionGroupPerformance_table = monthlyGroupPreformanceTable_data(ending_date_str, months_num)
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['group'] != 'Training']  # Exclude Training group for the chart
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['month_label'].isin(regionGroupPerformance_table['month_label'].unique()[-3:])]  # Get the last 3 months of data
    regionGroupPerformance_table['infractions_per_vehicle'] = round(regionGroupPerformance_table['infractions_per_vehicle'], 2)

    last_3_months = regionGroupPerformance_table['month_label'].unique()

    latest_month = last_3_months[-1]
    latest_group_size = regionGroupPerformance_table[regionGroupPerformance_table['month_label'] == latest_month][['group', 'group_size']]

    pivot = regionGroupPerformance_table.pivot(index='group', columns='month_label', values='infractions_per_vehicle').reset_index()

    result = pd.merge(pivot, latest_group_size, on='group', how='left')

    cols = ['group', 'group_size'] + list(last_3_months)
    regionGroupPerformance_table = result[cols]
    regionGroupPerformance_table_colors = n_colors('rgb(211,211,211)', 'rgb(47,79,79)', len(regionGroupPerformance_table.columns), colortype='rgb')

    return regionGroupPerformance_table, regionGroupPerformance_table_colors
    
