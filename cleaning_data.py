import pandas as pd
from suds.client import Client
import sqlite3
import datetime as dt

from LYTX_API.restAPI import pull_LYTX_eventsWithMetadata, pull_LYTX_vehicles, pull_LYTX_groups
from LYTX_API.soupAPI import LYTX_Login_SOAPUI, LYTX_GetUsers_SOUPUI, LYTX_GetUsers_fromGroup_SOUPUI


def cleaning_events_data(date_str):

    keys_to_include = [
        'id',  # Direct key
        'customerEventId',
        'eventTriggerId',
        'eventTriggerSubTypeId',
        'score',
        'vehicleId',
        'groupId',
        'latitude',
        'longitude',
        'driverId',
        'driverFirstName',
        'driverLastName',

        ('behaviors', 'creationDate'),
        'recordDateUTC',
        'recordDateTZ',
        'recordDateUTCOffset',
        
        ('behaviors', 'id'),  # Nested key path
        ('behaviors', 'name',),
    ]
    events_data = pull_LYTX_eventsWithMetadata(date_str, keys_to_include)

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(events_data)

    # Mapping vehicldeId to vehicleName - REST API
    lytx_vehicle_dict = pull_LYTX_vehicles()
    id_to_name = {v['id']: v['name'] for v in lytx_vehicle_dict}
    df['vehicleName'] = df['vehicleId'].map(id_to_name)

    # Mapping groupId to groupName - REST API
    lytx_group_dict = pull_LYTX_groups()
    id_to_name = {v['id']: v['name'] for v in lytx_group_dict}
    df['groupName'] = df['groupId'].map(id_to_name)

    # Mapping driverId to driverName - SOUPUI
    login_response = LYTX_Login_SOAPUI()
    lytx_user_dict = LYTX_GetUsers_SOUPUI(login_response)
    id_to_name = {v['UserId']: f"{v['FirstName'].strip()} {v['LastName'].strip()}" for v in lytx_user_dict}
    df['driverName'] = df['driverId'].map(id_to_name)

    # Convert the 'recordDateUTC' column from UTC to PST
    df['recordDateUTC'] = pd.to_datetime(df['recordDateUTC'], utc=True)
    df['recordDateUTC'] = df['recordDateUTC'].dt.tz_convert('America/Los_Angeles')
    df['recordDateUTC'] = df['recordDateUTC'].dt.strftime('%Y-%m-%d %H:%M:%S%z')

    # Change column names
    df = df.rename(columns={
        'id': 'eventId',
        'recordDateUTC': 'recordDate'
        })


    # save the df to sqlite
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()

    # Prepare columns and values
    columns = list(df.columns)
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?'] * len(columns))

    # Insert each row with INSERT OR IGNORE
    # if a primary key or unique constraint violation occurs, the row will be ignored
    for row in df.itertuples(index=False, name=None):
        cursor.execute(
            f'INSERT OR IGNORE INTO lytxRawEventsData ({columns_str}) VALUES ({placeholders})',
            row
        )

    conn.commit()
    conn.close()

for date in pd.date_range(start='2025-05-01', end='2025-05-20'):
    cleaning_events_data(date.strftime('%Y-%m-%d'))
    print(f"Data for {date.strftime('%Y-%m-%d')} cleaned and inserted into the database.")

    

