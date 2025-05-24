import sqlite3
import pandas as pd

def sqlite3_query(ending_date_str, starting_date_str, columns_list):
# Connect to the SQLite database
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()

    columns_str = ', '.join(columns_list)

    # Query to get the count of events by date
    query = f"""
        SELECT {columns_str}
        FROM lytxRawEventsData
        WHERE recordDate BETWEEN ? AND ?
    """

    cursor.execute(query, (starting_date_str, ending_date_str))
    data = cursor.fetchall()

    conn.close()

    # Convert the data to a DataFrame
    df = pd.DataFrame(data, columns=columns_list)

    return df