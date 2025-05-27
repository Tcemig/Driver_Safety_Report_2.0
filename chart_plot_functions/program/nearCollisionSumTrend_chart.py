import plotly.graph_objects as go
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.nearCollisionSumTrend_chartData import nearCollision_sumTrend_chartData

def nearCollision_sumTrend_chart(ending_date_str, fig, row_num, col_num):

    nearCollision_sumTrend_data = nearCollision_sumTrend_chartData(ending_date_str)

    fig.add_trace(go.Bar(
        x= nearCollision_sumTrend_data['week_label'],
        y= nearCollision_sumTrend_data['event_size'],
        name= '',
        ), row= row_num, col= col_num)
    fig.update_xaxes(
        title_text= "Weeks",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Behavior / Active ERs",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)


    # Calculate linear regression line
    slope, intercept = np.polyfit(nearCollision_sumTrend_data.index, nearCollision_sumTrend_data['event_size'], 1)
    line_of_best_fit = slope * np.array(nearCollision_sumTrend_data.index) + intercept
    fig.add_trace(go.Scatter(
        x= nearCollision_sumTrend_data['week_label'],
        y= line_of_best_fit,
        mode= 'lines',
        name= 'Line of Best Fit',
        line= dict(color='black'),
        ), row= row_num, col= col_num)

    fig.add_annotation(
        xref="x domain", yref="y",
        x=0.0, y=0.20,
        text= "Near Collisions frequency per vehicles has",
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

    line_of_best_fit_Diff = round(((list(line_of_best_fit)[-1] / list(line_of_best_fit)[0]) -1) *100, 2)
    if line_of_best_fit_Diff > 0:
        annotation_text = f"increased <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    else:
        annotation_text = f"decreased <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past 12 weeks."
    fig.add_annotation(
        xref="x domain", yref="y",
        x=0.0, y=0.05,
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