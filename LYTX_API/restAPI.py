import http.client
import json
import os
import math
from dotenv import load_dotenv

load_dotenv()

LYTX_API_KEY = os.getenv('LYTX_API_KEY')
LYTX_HTTP_CONNECTION = os.getenv('LYTX_HTTP_CONNECTION')

def pull_LYTX_eventsWithMetadata(date_str, keys_to_include):

    conn = http.client.HTTPSConnection(LYTX_HTTP_CONNECTION)
    headers = {
        'accept': "application/json",
        'x-apikey': LYTX_API_KEY
        }
    return_limit = 1000
    conn.request(
        "GET",
        f"""/video/safety/eventsWithMetadata?limit={return_limit}&includeSubgroups=true&sortBy=lastUpdatedDate&sortDirection=desc&dateOption=lastUpdatedDate&to={date_str}T23%3A59%3A59.00Z&from={date_str}T00%3A00%3A00.00Z""",
        headers=headers
    )
    res = conn.getresponse()
    data = res.read()
    # data = data.decode("utf-8")
    data = json.loads(data.decode("utf-8"))

    # Process the data
    processed_data = []
    for item in data:
        new_item = {}
        for key in keys_to_include:
            if isinstance(key, tuple):  # Nested key
                temp_list = item[key[0]]
                if len(temp_list) == 1:
                    new_item[f"{key[0]}{key[-1].title()}"] = temp_list[0][key[-1]]
                else:
                    new_item[f"{key[0]}{key[-1].title()}"] = ""
            else:  # Direct key
                new_item[key] = item[key]
        processed_data.append(new_item)

    return processed_data

date_str = '2025-05-20'
keys_to_include = [
    'id',  # Direct key
    'customerEventId',
    'eventTriggerId',
    'eventTriggerSubTypeId',
    'score',
    'vehicleId',
    'groupId',
    'speed',
    'latitude',
    'longitude',
    'driverId',
    # 'coachId',
    'driverFirstName',
    'driverLastName',
    
    ('behaviors', 'id'),  # Nested key path
    ('behaviors', 'name',),
    ('behaviors', 'creationDate'),
]
return_data = pull_LYTX_eventsWithMetadata(date_str, keys_to_include)
with open('temp_json_files/lytx_events.json', 'w') as f:
    json.dump(return_data, f, indent=4)
skip=1

def pull_LYTX_vehicles():

    conn = http.client.HTTPSConnection(LYTX_HTTP_CONNECTION)
    headers = {
        'accept': "application/json",
        'x-apikey': LYTX_API_KEY
        }
    return_limit = 1000
    conn.request("GET", f"/vehicles/all?limit={return_limit}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    # data = data.decode("utf-8")
    data = json.loads(data.decode("utf-8"))

    return data
# return_data = pull_LYTX_vehicles()

def pull_LYTX_drivers(date_str):

    all_trips = []
    page = 1
    total_pages = 1

    while page <= total_pages:

        conn = http.client.HTTPSConnection(LYTX_HTTP_CONNECTION)
        headers = {
            'accept': "application/json",
            'x-apikey': LYTX_API_KEY,
            'Content-Type': 'application/json'
            }
        params = {
            f"startTime": f"{date_str}T00:00:00.000Z",
            f"endTime": f"{date_str}T23:59:59.999Z",
            "pageNumber": page,
            "pageSize": 1000
        }
        body = json.dumps(params)
        conn.request("POST", f"/driverId/trips", body=body, headers=headers)
        res = conn.getresponse()
        data = res.read()
        data = json.loads(data.decode("utf-8"))

        # Assuming the trips are in a key called 'items' or similar
        trips = data.get('results', [])
        all_trips.extend(trips)

        if page == 1: # calculate total pages on first iteration
            total_pages = math.ceil(data.get('totalCount')/1000)

        page += 1

    return all_trips
# return_data = pull_LYTX_drivers('2025-05-16')

def pull_LYTX_groups():

    conn = http.client.HTTPSConnection(LYTX_HTTP_CONNECTION)
    headers = {
        'accept': "application/json",
        'x-apikey': LYTX_API_KEY
        }
    return_limit = 100
    conn.request("GET", f"/groups?limit={return_limit}", headers=headers)
    res = conn.getresponse()
    data = res.read()
    # data = data.decode("utf-8")
    data = json.loads(data.decode("utf-8"))
    data = data['groups']

    return data
return_data = pull_LYTX_groups()
with open('temp_json_files/lytx_groups.json', 'w') as f:
    json.dump(return_data, f, indent=4)
skip=1
