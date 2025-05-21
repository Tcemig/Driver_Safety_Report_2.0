import pandas as pd
from suds.client import Client


from LYTX_API.restAPI import pull_LYTX_eventsWithMetadata


def pulling_data():

    date_str = '2025-05-20'
    keys_to_include = [
        'id',  # Direct key
        'customerEventId',
        'eventTriggerId',
        'eventTriggerSubTypeId',
        'score',
        'vehicleId',
        'groupId',
        'driverId',
        'driverFirstName',
        'driverLastName',
        
        ('behaviors', 'id'),  # Nested key path
        ('behaviors', 'name',),
    ]
    events_data = pull_LYTX_eventsWithMetadata(date_str, keys_to_include)

