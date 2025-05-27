import plotly.graph_objects as go
import numpy as np

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.behavior_sumTrend_chartData import behavior_sumTrend_chartData

def behavior_sumTrend_chart(ending_date_str, fig, row_num, col_num):

    Behaviors_Totals_df, text_labels, text_colors = behavior_sumTrend_chartData(ending_date_str)

    Behaviors_Totals_df = Behaviors_Totals_df.iloc[:20]
    text_labels = text_labels[:20]
    text_colors = text_colors[:20]
    
    fig.add_trace(go.Bar(
        x= Behaviors_Totals_df['behaviorsName'],
        y= Behaviors_Totals_df['event_size'],
        name= '',
        
        # marker_color=Behaviors_Totals_df_textColors
        # text= Behaviors_Totals_df_text,
        # textfont= dict(color=Behaviors_Totals_df_textColors, size=140),
        ), row= row_num, col= col_num)
    fig.update_traces(
        textposition= 'auto',
        textangle= 270,
        row= row_num, col= col_num)
    fig.update_xaxes(
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        tickangle= 270,
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Count",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)

    for i, txt in enumerate(text_labels):
        fig.add_annotation(
            x=Behaviors_Totals_df.index[i],
            y=Behaviors_Totals_df['event_size'][i] + 135,
            text=txt,
            showarrow=False,
            textangle= 270,
            font=dict(
                size=11,
                color=text_colors[i]
            ), row= row_num, col= col_num
        )

    return fig