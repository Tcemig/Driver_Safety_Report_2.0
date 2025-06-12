def infractionFrequencyCategory_chartData(weekly_total_data, regionGroupPerformance_table):

    regionGroupPerformance_table = regionGroupPerformance_table.copy()
    regionGroupPerformance_table = regionGroupPerformance_table.iloc[-4:, :] 
    regionGroupPerformance_table = regionGroupPerformance_table[regionGroupPerformance_table['group'] != 'Training']

    weekly_total_data = weekly_total_data.copy()
    weekly_total_data = weekly_total_data[weekly_total_data['group'] != 'Training']

    weekly_total_data['infractions_per_vehicle']  = 0

    for index, row in weekly_total_data.iterrows():
        try:
            weekly_total_data.at[index, 'infractions_per_vehicle'] = round(row['event_size'] / regionGroupPerformance_table[regionGroupPerformance_table['group'] == row['group']]['group_size'].values[0], 2)
        except IndexError:
            weekly_total_data.at[index, 'infractions_per_vehicle'] = 0

    return weekly_total_data

    



