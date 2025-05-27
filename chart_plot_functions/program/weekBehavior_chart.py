import plotly.graph_objects as go
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.weekBehavior_chartData import oneWeekBehavior_chartData

def oneWeekBehavior_chart(ending_date_str, fig, row_num, col_num, weekDate_str, days_num=60):
    """
    This function generates the one week behavior chart.
    It pulls the last 1 week of data and excludes the Training group.
    """

    Behaviors_Totals_df, text_labels, text_colors = oneWeekBehavior_chartData(ending_date_str, days_num, weekDate_str)

    Behaviors_Totals_df = Behaviors_Totals_df.iloc[:8]
    text_labels = text_labels[:8]
    text_colors = text_colors[:8]


    fig.add_trace(go.Bar(
        x= Behaviors_Totals_df['event_size'],
        y= Behaviors_Totals_df['behaviorsName'],
        name= '',
        orientation='h',
        text= text_labels,
        textfont= dict(color=text_colors),
        ), row= row_num, col= col_num)
    fig.update_traces(
        textposition= 'outside',
        row= row_num, col= col_num)
    fig.update_xaxes(
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        tickfont=dict(size=9),  # Change the size of the x-axis labels
        
        row= row_num, col= col_num)

    fig.add_annotation(
        x=1.015,
        y=0.57,
        xref="paper",
        yref="paper",
        text="Coachable Behaviors",
        showarrow=False,
        font=dict(size=14, color='black'),
        textangle= -90
    )

    return fig