import pandas as pd
import os
import sqlite3

def creating_sql_tables(creating_table, columns):

    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns])

    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {creating_table} (
            {columns_def}
        )
    ''')
    conn.commit()
    conn.close()

columns = [
    ("id", "INTEGER PRIMARY KEY UNIQUE"), # AUTOINCREMENT
    ('eventId', 'STRING NOT NULL UNIQUE'),
    ('customerEventId', 'STRING'),
    ('eventTriggerId', 'STRING'),
    ('eventTriggerSubTypeId', 'STRING'),
    ('score', 'INTEGER'),
    ('vehicleId', 'STRING'),
    ('groupId', 'STRING'),
    ('latitude', 'REAL'),
    ('longitude', 'REAL'),
    ('driverId', 'STRING'),
    ('driverFirstName', 'STRING'),
    ('driverLastName', 'STRING'),
    ('recordDate', 'DATETIME'),
    ('recordDateTZ', 'STRING'),
    ('recordDateUTCOffset', 'STRING'),
    ('vehicleName', 'STRING'),
    ('groupName', 'STRING'),
    ('driverName', 'STRING'),
    ('behaviorsId', 'STRING'),
    ('behaviorsName', 'STRING'),
    ('behaviorsCreationDate', 'DATETIME')
]
creating_sql_tables("lytxRawEventsData", columns)
print("Table created successfully.")

def deleting_sql_table(table_name):
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
    conn.commit()
    conn.close()
# answer = input("Do you want to delete the table? (yes/no): ")
# if answer.strip().lower() == 'yes':
#     deleting_sql_table("lytxAllBehaviors")
#     print("Table deleted successfully.")

def remove_all_data_from_table(table_name):
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM {table_name}')
    conn.commit()
    conn.close()
# answer = input("Do you want to remove all data from the table? (yes/no): ")
# if answer.strip().lower() == 'yes':
#     remove_all_data_from_table("lytxRawEventsData")
#     print("All data removed successfully.")

def change_column_name(table_name, old_column_name, new_column_name):
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    cursor.execute(f'ALTER TABLE {table_name} RENAME COLUMN {old_column_name} TO {new_column_name}')
    conn.commit()
    conn.close()
# change_column_name("lytxRawEventsData", "behaviors_name", "behaviorsName")


def convert_csv_to_sql(file):
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file)

    # Convert the DataFrame to SQL
    df.to_sql('my_table', conn, if_exists='append', index=False)

    conn.commit()
    conn.close()