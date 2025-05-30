import pandas as pd
import sqlite3

def behavior_sumTrend_chartData(weekly_grouped_data, nonPriority):
    """
    This function generates the data for the behavior sum trend chart.
    It pulls the last 12 weeks of data and excludes the Training group.
    """
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['group'] != 'Training']  # Exclude Training group
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'] != '']  # Exclude empty behaviors

    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    query = """
        SELECT *
        FROM nonPriority_behaviors
    """
    cursor.execute(query)
    nonPriorityBehaviors_data = cursor.fetchall()
    conn.close()
    nonPriorityBehaviors_data = pd.DataFrame(nonPriorityBehaviors_data, columns=['id', 'category'])
    nonPriorityBehaviors_list = nonPriorityBehaviors_data['category'].unique().tolist()

    if nonPriority: # if True then exclude non-priority behaviors
        weekly_grouped_data = weekly_grouped_data.drop(weekly_grouped_data[weekly_grouped_data['behaviorsName'].isin(nonPriorityBehaviors_list)].index)
    else:  # if False then only include priority behaviors
        weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'].isin(nonPriorityBehaviors_list)]

    Past12Week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-12:])]  # Get the last 12 weeks of data
    Past12Week_grouped_data = Past12Week_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    Past12Week_grouped_data = Past12Week_grouped_data.sort_values(by='event_size', ascending=False)
    Past12Week_grouped_data = Past12Week_grouped_data.reset_index(drop=True)

    Past24Week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-24:-12])]  # Get the last 24 weeks of data
    Past24Week_grouped_data = Past24Week_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    Past24Week_grouped_data = Past24Week_grouped_data.sort_values(by='event_size', ascending=False)



    # Create DataFrames indexed by behavior name
    recent_df = Past12Week_grouped_data.set_index('behaviorsName')[['event_size']].rename(columns={'event_size': 'Frequency'})
    previous_df = Past24Week_grouped_data.set_index('behaviorsName')[['event_size']].rename(columns={'event_size': 'Frequency'})

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

    return Past12Week_grouped_data, text_labels, text_colors


