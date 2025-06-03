


def infractionFrequencyPerBehavior_chartData(weekly_grouped_data):

    weekly_grouped_data = weekly_grouped_data.copy()
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['group'] != 'Training']  # Exclude Training group for the chart
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'] != '']  # Exclude empty behavior names
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-18:])]  # Get the last 18 weeks of data

    behavior_totals = weekly_grouped_data.groupby(['behaviorsName']).agg({'event_size': 'sum'}).reset_index()
    behavior_totals = behavior_totals.sort_values(by='event_size', ascending=False).reset_index(drop=True)

    top_18_behaviors = behavior_totals['behaviorsName'].unique().tolist()[:18]
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'].isin(top_18_behaviors)]

    return weekly_grouped_data, top_18_behaviors

