import pandas as pd

def individualBehaviorWeekly_chartData(weekly_grouped_data, behavior_name):
    """
    This function generates the data for the individual behavior weekly chart.
    It pulls the last 12 weeks of data and excludes the Training group.
    """
    
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['group'] != 'Training']  # Exclude Training group
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'] == behavior_name]  # Filter by specific behavior
    weekly_grouped_data = weekly_grouped_data.groupby(['week_label'], as_index=False).agg({'event_size': 'sum'})

    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-12:])] # Get the last 12 weeks of data
    weekly_grouped_data = weekly_grouped_data.reset_index(drop=True)


    return weekly_grouped_data








