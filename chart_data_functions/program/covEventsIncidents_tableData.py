import pandas as pd

def covEventsIncidents_tableData(covEI_data, smartSheet_data):
    """
    This function generates the data for the monthly group performance table.
    It pulls the last 5 months of data and excludes the Training group.
    """

    # still need to pull at/no/shared fault data from the database
    
    covEI_data['week_label'] = pd.to_datetime(covEI_data['week_label'], errors='coerce')


    covEI_weekly_data = covEI_data.copy()
    covEI_weekly_data['week_label'] = covEI_weekly_data['week_label'].dt.strftime('%Y-%m-%d')
    covEI_weekly_data = covEI_weekly_data[covEI_weekly_data['week_label'].isin(covEI_weekly_data['week_label'].unique()[-5:])]  # Get the last 5 weeks of data



    covEI_weekly_data['Total VI At Fault'], covEI_weekly_data['Total VI No Fault'], covEI_weekly_data['Total VI Shared Fault'] = 0, 0, 0

    for index, row in covEI_weekly_data.iterrows():
        start_date = pd.to_datetime(row['week_label'])
        end_date = start_date + pd.DateOffset(days=6)

        # Filter the smartSheet_data for the current week
        week_data = smartSheet_data[(smartSheet_data['Date of Incident'] >= start_date) & (smartSheet_data['Date of Incident'] <= end_date)]
        # Calculate the totals for each fault type
        at_fault_count = week_data[week_data['Fault'].str.contains('at', case=False, na=False)].shape[0]
        no_fault_count = week_data[week_data['Fault'].str.contains('no', case=False, na=False)].shape[0]
        shared_fault_count = week_data[week_data['Fault'].str.contains('shared', case=False, na=False)].shape[0]
        # Update the corresponding columns in covEI_weekly_data
        covEI_weekly_data.at[index, 'Total VI At Fault'] = at_fault_count
        covEI_weekly_data.at[index, 'Total VI No Fault'] = no_fault_count
        covEI_weekly_data.at[index, 'Total VI Shared Fault'] = shared_fault_count

    # Monthly Data
    covEI_monthly_data = covEI_data.copy()
    covEI_monthly_data['week_label'] = covEI_monthly_data['week_label'].dt.strftime('%Y-%m')
    covEI_monthly_data = covEI_monthly_data[covEI_monthly_data['week_label'].isin(covEI_monthly_data['week_label'].unique()[-5:])]  # Get the last 5 months of data

    covEI_monthly_data = covEI_monthly_data.groupby('week_label', as_index=False).agg({
        'group_size': 'mean',
        'event_size': 'sum',
    })
    covEI_monthly_data['group_size'] = covEI_monthly_data['group_size'].astype(int)
    covEI_monthly_data['event_size'] = covEI_monthly_data['event_size'].astype(int)

    covEI_monthly_data['Total VI At Fault'], covEI_monthly_data['Total VI No Fault'], covEI_monthly_data['Total VI Shared Fault'] = 0, 0, 0

    for index, row in covEI_monthly_data.iterrows():
        start_date = pd.to_datetime(row['week_label'])
        end_date = start_date + pd.DateOffset(months=1) - pd.DateOffset(days=1)

        # Filter the smartSheet_data for the current month
        month_data = smartSheet_data[(smartSheet_data['Date of Incident'] >= start_date) & (smartSheet_data['Date of Incident'] <= end_date)]
        # Calculate the totals for each fault type
        at_fault_count = month_data[month_data['Fault'].str.contains('at', case=False, na=False)].shape[0]
        no_fault_count = month_data[month_data['Fault'].str.contains('no', case=False, na=False)].shape[0]
        shared_fault_count = month_data[month_data['Fault'].str.contains('shared', case=False, na=False)].shape[0]
        # Update the corresponding columns in covEI_monthly_data
        covEI_monthly_data.at[index, 'Total VI At Fault'] = at_fault_count
        covEI_monthly_data.at[index, 'Total VI No Fault'] = no_fault_count
        covEI_monthly_data.at[index, 'Total VI Shared Fault'] = shared_fault_count


    return covEI_weekly_data, covEI_monthly_data




