import pandas as pd


from chart_plot_functions.functions.table_sequence_color import get_monthly_table_colors

def regionalGroupPerformanceWeekly_tableData(regionGroupPerformance_table, weekly_total_data):

    regionGroupPerformance_table = regionGroupPerformance_table.copy()
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['group'] != 'Training']  # Exclude Training group for the chart

    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['month_label'].isin(regionGroupPerformance_table['month_label'].unique()[-1:])]  # Get the last month of data
    regionGroupPerformance_table = regionGroupPerformance_table.reset_index(drop=True)

    weekly_total_data = weekly_total_data.copy()
    weekly_total_data = weekly_total_data[weekly_total_data['group'] != 'Training']  # Exclude Training group for the chart
    weekly_total_data = weekly_total_data[weekly_total_data['week_label'].isin(weekly_total_data['week_label'].unique()[-12:])]
    weekly_total_data = weekly_total_data.reset_index(drop=True)

    regionGroupPerformance_table['infractions_per_vehicle'] = 0

    for index, row in weekly_total_data.iterrows():
        weekly_total_data.at[index, 'infractions_per_vehicle'] = round(row['event_size'] / regionGroupPerformance_table[regionGroupPerformance_table['group'] == row['group']]['group_size'].values[0], 2)

    last_3_months = regionGroupPerformance_table['month_label'].unique()

    latest_month = last_3_months[-1]
    latest_group_size = regionGroupPerformance_table[regionGroupPerformance_table['month_label'] == latest_month][['group', 'group_size']]

    week_list = weekly_total_data['week_label'].unique().tolist()

    pivot = weekly_total_data.pivot(index='group', columns='week_label', values='infractions_per_vehicle').reset_index()

    result = pd.merge(pivot, latest_group_size, on='group', how='left')
    result.insert(1, 'group_size', result.pop('group_size'))  # Move group_size to the second column

    fill_colors = get_monthly_table_colors(result, week_list)

    return result, fill_colors