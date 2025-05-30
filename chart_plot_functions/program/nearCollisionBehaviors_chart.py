import plotly.graph_objects as go
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.nearCollisionBehaviors_chartData import nearCollision_behaviorsTrend_chartData

def nearCollision_behaviorsTrend_chart(weekly_grouped_data, fig, row_num, col_num):

    nearCollision_behaviorsTrend_data, NearCollision_Totals_df_textColors, NearCollision_Totals_df_text = nearCollision_behaviorsTrend_chartData(weekly_grouped_data)

    fig.add_trace(go.Bar(
        x= nearCollision_behaviorsTrend_data['event_size'],
        y= nearCollision_behaviorsTrend_data['behaviorsName'],
        name= '',
        orientation='h',
        text= NearCollision_Totals_df_text,
        textfont= dict(color=NearCollision_Totals_df_textColors),
        ), row= row_num, col= col_num)
    fig.update_traces(
        textposition= 'outside',
        row= row_num, col= col_num)
    fig.update_xaxes(
        # title_text= "",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)

    fig.add_annotation(
        x=1.015,
        y=0.73,
        xref="paper",
        yref="paper",
        text="Coachable Behaviors",
        showarrow=False,
        font=dict(size=14, color='black'),
        textangle= -90
    )

    return fig