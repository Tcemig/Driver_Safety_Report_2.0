import sqlite3
import pandas as pd
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from functions.chart_data_creation import weeklyInfractionsTotalPerCategory_data

def nearCollision_sumTrend_chartData(ending_date_str):
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


    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num=96)
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-12:])]  # Get the last 12 weeks of data
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'].isin(nearCollisionCategories_list)]
    weekly_grouped_data = weekly_grouped_data.groupby(['week_label'], as_index=False).agg({'event_size': 'sum'})
    
    
    return weekly_grouped_data


