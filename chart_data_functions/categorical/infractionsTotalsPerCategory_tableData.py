import sqlite3
import pandas as pd


def infractionsTotalsPerCategory_tableData(weekly_grouped_data):
    """
    This function generates the data for the infractions totals per category table.
    It aggregates the weekly grouped data to get the total infractions per category.
    """
    weekly_grouped_data = weekly_grouped_data.copy()
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['group'] != 'Training']  # Exclude Training group for the chart
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['behaviorsName'] != '']  # Exclude empty behavior names
    weekly_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-8:])]  # Get the last 3 weeks of data
    
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    query = """
        SELECT *
        FROM categoricalBehaviors_drop
    """
    cursor.execute(query)
    categoricalBehaviors_drop_data = cursor.fetchall()
    conn.close()
    categoricalBehaviors_drop_data = pd.DataFrame(categoricalBehaviors_drop_data, columns=['id', 'category'])
    categoricalBehaviors_drop_list = categoricalBehaviors_drop_data['category'].unique().tolist()

    weekly_grouped_data = weekly_grouped_data[~weekly_grouped_data['behaviorsName'].isin(categoricalBehaviors_drop_list)]  # Exclude non-priority behavior

    weekly_total_data = weekly_grouped_data.groupby(['week_label', 'behaviorsName']).agg({'event_size': 'sum'}).reset_index()

    return weekly_grouped_data, weekly_total_data

