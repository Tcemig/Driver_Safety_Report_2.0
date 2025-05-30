import pandas as pd

from chart_plot_functions.functions.table_sequence_color import get_monthly_table_colors

def regionalGroupPerformance_tableData(regionGroupPerformance_table):
    """
    This function generates the data for the regional group performance table.
    It pulls the last 3 months of data and excludes the Training group.
    """
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['group'] != 'Training']  # Exclude Training group for the chart
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['month_label'].isin(regionGroupPerformance_table['month_label'].unique()[-3:])]  # Get the last 3 months of data
    regionGroupPerformance_table['infractions_per_vehicle'] = round(regionGroupPerformance_table['infractions_per_vehicle'], 2)

    last_3_months = regionGroupPerformance_table['month_label'].unique()

    latest_month = last_3_months[-1]
    latest_group_size = regionGroupPerformance_table[regionGroupPerformance_table['month_label'] == latest_month][['group', 'group_size']]

    pivot = regionGroupPerformance_table.pivot(index='group', columns='month_label', values='infractions_per_vehicle').reset_index()

    result = pd.merge(pivot, latest_group_size, on='group', how='left')
    result.insert(1, 'group_size', result.pop('group_size'))  # Move group_size to the second column

    fill_colors = get_monthly_table_colors(result, last_3_months)

    return result, fill_colors
    
