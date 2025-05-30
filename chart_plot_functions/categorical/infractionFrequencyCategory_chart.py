import pandas as pd
import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.categorical.infractionFrequencyCategory_chartData import infractionFrequencyCategory_chartData

def infractionFrequencyCategory_chart(weekly_total_data, regionGroupPerformance_table, fig, row_num, col_num):

    weekly_total_data = infractionFrequencyCategory_chartData(weekly_total_data, regionGroupPerformance_table)

    groups_list = weekly_total_data['group'].unique().tolist()
    
    for group in groups_list:
        cat_df = weekly_total_data[weekly_total_data['group'] == group]
        fig.add_trace(go.Scatter(
            x= cat_df['week_label'],
            y= cat_df['infractions_per_vehicle'],
            mode= 'lines+markers',
            name= group,
            line=dict(color='green' if group == 'COV' else 'blue' if group == 'Contractor' else 'red'),  # Set the color of the line
            showlegend= True,
            ), row= row_num, col= col_num)
    fig.update_xaxes(
        nticks= 20,
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Frequency Per Vehicle",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    
    return fig





