import plotly.graph_objects as go
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.individualBehaviorWeekly_chartData import individualBehaviorWeekly_chartData

def individualBehaviorWeekly_chart(weekly_grouped_data, behavior_name, fig, row_num, col_num):

    individualBehaviorWeekly_data = individualBehaviorWeekly_chartData(weekly_grouped_data, behavior_name)

    fig.add_trace(go.Bar(
        x= individualBehaviorWeekly_data['week_label'],
        y= individualBehaviorWeekly_data['event_size'],
        name= '',
        ), row= row_num, col= col_num)
    fig.update_xaxes(
        title_text= "",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Count",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    
    # Calculate linear regression line
    slope, intercept = np.polyfit(individualBehaviorWeekly_data.index, individualBehaviorWeekly_data['event_size'], 1)
    line_of_best_fit = slope * np.array(individualBehaviorWeekly_data.index) + intercept
    fig.add_trace(go.Scatter(
        x= individualBehaviorWeekly_data['week_label'],
        y= line_of_best_fit,
        mode= 'lines',
        name= 'Line of Best Fit',
        line= dict(color='black')
        ), row= row_num, col= col_num)
    
    # Add custom annotation to the bar chart
    line_of_best_fit_Diff = round(((list(abs(line_of_best_fit))[-1] / list(abs(line_of_best_fit))[0]) -1) *100, 2)
    if line_of_best_fit_Diff > 0:
        annotation_text = f"Behavior has increased by <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    else:
        annotation_text = f"Behavior has decreased by <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    fig.add_annotation(
        xref="x domain", yref="y",
        x=0.01, y=0.0,
        text= annotation_text,
        showarrow=False,
        font=dict(
            size=12,
            color="black"
        ),
        align="center",
        bordercolor="black",
        borderwidth=1,
        borderpad=2,
        bgcolor="white",
        opacity=0.9,
        row= row_num, col= col_num
    )
    
    return fig