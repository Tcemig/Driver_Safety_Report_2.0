import sqlite3
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from functions.chart_data_creation import weeklyInfractionsTotalPerCategory_data

def nearCollision_behaviorsTrend_chartData(ending_date_str):
    """
    This function generates the data for the near collision sum trend chart.
    It pulls the last 12 weeks of data and excludes the Training group.
    """
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    query = """
        SELECT *
        FROM nearCollisionCategories
    """
    cursor.execute(query)
    nearCollisionCategories_data = cursor.fetchall()
    conn.close()
    nearCollisionCategories_data = pd.DataFrame(nearCollisionCategories_data, columns=['id', 'category'])
    nearCollisionCategories_list = nearCollisionCategories_data['category'].unique().tolist()


    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num=200)
    Past12Week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-12:])]  # Get the last 12 weeks of data
    Past12Week_grouped_data = Past12Week_grouped_data[Past12Week_grouped_data['behaviorsName'].isin(nearCollisionCategories_list)]
    Past12Week_grouped_data = Past12Week_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    NearCollision_Totals_df = Past12Week_grouped_data.set_index('behaviorsName')['event_size'].to_dict()
    NearCollision_Totals_df = pd.DataFrame.from_dict(NearCollision_Totals_df, orient='index', columns=['Frequency'])
    Past12Week_grouped_data = Past12Week_grouped_data.sort_values(by='event_size', ascending=True)

    Past24Week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-24:-12])]  # Get the last 24 weeks of data
    Past24Week_grouped_data = Past24Week_grouped_data[Past24Week_grouped_data['behaviorsName'].isin(nearCollisionCategories_list)]
    Past24Week_grouped_data = Past24Week_grouped_data.groupby(['behaviorsName'], as_index=False).agg({'event_size': 'sum'})
    PastNearCollision_Totals_df = Past24Week_grouped_data.set_index('behaviorsName')['event_size'].to_dict()
    PastNearCollision_Totals_df = pd.DataFrame.from_dict(PastNearCollision_Totals_df, orient='index', columns=['Frequency'])

    # Making Percentage Difference 12 Week Near Collision Behavior Sum
    NearCollision_Totals_df['Percentage Diff'] = 'N/A'
    NearCollision_Totals_df_textColors = []
    NearCollision_Totals_df_text = []
    for index, row in NearCollision_Totals_df.iterrows():
        current_Behavior = index
        current_Behavior_Num = int(NearCollision_Totals_df.loc[index, 'Frequency'])
        past_Behavior_Num = PastNearCollision_Totals_df.loc[current_Behavior, 'Frequency']
        percent_diff_num = 'N/A'
        try:
            past_Behavior_Num = int(past_Behavior_Num)
            percent_diff_num = round(((current_Behavior_Num/past_Behavior_Num)-1)*100, 2)
            NearCollision_Totals_df.loc[index, 'Percentage Diff'] = percent_diff_num
            NearCollision_Totals_df_text.append(f"{percent_diff_num}%")
            if percent_diff_num > 0:
                NearCollision_Totals_df_textColors.append('red')
            elif percent_diff_num < 0:
                NearCollision_Totals_df_textColors.append('green')
            else:
                NearCollision_Totals_df_textColors.append('black')
        except TypeError:
            NearCollision_Totals_df_textColors.append('black')
            NearCollision_Totals_df_text.append("N/A")  

    return Past12Week_grouped_data, NearCollision_Totals_df_textColors, NearCollision_Totals_df_text

nearCollision_behaviorsTrend_chartData("2025-05-20")