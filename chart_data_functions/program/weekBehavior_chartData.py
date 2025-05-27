import pandas as pd
import datetime as dt
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from functions.chart_data_creation import weeklyInfractionsTotalPerCategory_data


def get_7_days_prior(date_str):
    date_obj = dt.datetime.strptime(date_str, "%Y-%m-%d")
    prior_date = date_obj - dt.timedelta(days=7)
    return prior_date.strftime("%Y-%m-%d")

def oneWeekBehavior_chartData(ending_date_str, days_num, weekDate_str):
    """
    This function generates the data for the one week behavior chart.
    It pulls the last 1 week of data and excludes the Training group.
    """
    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num)
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['group'] != 'Training']  # Exclude Training group
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'] != '']  # Exclude empty behaviors

    display_weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'] == weekDate_str]  # Get the last 1 week of data
    display_weekly_grouped_data = display_weekly_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    display_weekly_grouped_data = display_weekly_grouped_data.sort_values(by='event_size', ascending=False)
    display_weekly_grouped_data = display_weekly_grouped_data.reset_index(drop=True)

    past_week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'] == get_7_days_prior(weekDate_str)]
    past_week_grouped_data = past_week_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    past_week_grouped_data = past_week_grouped_data.sort_values(by='event_size', ascending=False)
    past_week_grouped_data = past_week_grouped_data.reset_index(drop=True)

    # Create DataFrames indexed by behavior name
    recent_df = display_weekly_grouped_data.set_index('behaviorsName')[['event_size']].rename(columns={'event_size': 'Frequency'})
    previous_df = past_week_grouped_data.set_index('behaviorsName')[['event_size']].rename(columns={'event_size': 'Frequency'})

    # Add Percentage Diff column
    recent_df['Percentage Diff'] = 'N/A'
    text_colors = []
    text_labels = []

    for behavior in recent_df.index:
        current = recent_df.at[behavior, 'Frequency']
        past = previous_df['Frequency'].get(behavior, None)
        try:
            if past is not None and past != 0:
                percent_diff = round(((current / past) - 1) * 100, 2)
                recent_df.at[behavior, 'Percentage Diff'] = percent_diff
                text_labels.append(f"{percent_diff}%")
                if percent_diff > 0:
                    text_colors.append('red')
                elif percent_diff < 0:
                    text_colors.append('green')
                else:
                    text_colors.append('black')
            else:
                text_colors.append('black')
                text_labels.append("N/A")
        except Exception:
            text_colors.append('black')
            text_labels.append("N/A")

    return display_weekly_grouped_data, text_labels, text_colors

