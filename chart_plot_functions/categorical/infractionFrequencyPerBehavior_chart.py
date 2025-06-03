import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.categorical.infractionFrequencyPerBehavior_chartData import infractionFrequencyPerBehavior_chartData

def infractionFrequencyPerBehavior_chart(weekly_grouped_data, fig, row_num, col_num):


    weekly_grouped_data, top_18_behaviors = infractionFrequencyPerBehavior_chartData(weekly_grouped_data)

    for col in top_18_behaviors:
        
        total_cov = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) & 
            (weekly_grouped_data['group'] == 'COV')
        ]['event_size'].sum()
        total_contractor = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) &
            (weekly_grouped_data['group'] == 'Contractor')
        ]['event_size'].sum()
        total_linehaul = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) &
            (weekly_grouped_data['group'] == 'Linehaul')
        ]['event_size'].sum()

        COV_Behaviors_df = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) &
            (weekly_grouped_data['group'] == 'COV')
        ].reset_index(drop=True)
        Contractor_Behaviors_df = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) &
            (weekly_grouped_data['group'] == 'Contractor')
        ].reset_index(drop=True)
        Linehaul_Behaviors_df = weekly_grouped_data[
            (weekly_grouped_data['behaviorsName'] == col) &
            (weekly_grouped_data['group'] == 'Linehaul')
        ].reset_index(drop=True)
        
        for cat_df, cat_text in zip([COV_Behaviors_df, Contractor_Behaviors_df, Linehaul_Behaviors_df], ['COV', 'Contractor', 'Linehaul']):

            fig.add_trace(go.Scatter(
                x= cat_df['week_label'],
                y= cat_df['event_size'],
                mode= 'lines+markers',
                name= f'{cat_text}',
                line=dict(color='green' if cat_text == 'COV' else 'blue' if cat_text == 'Contractor' else 'red'),  # Set the color of the line
                showlegend= False,
                ), row= row_num, col= col_num)
            
        fig.update_xaxes(
            showticklabels = False,
            nticks= 20,
            showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
            showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
            
            row= row_num, col= col_num)
        if col_num == 1:
            fig.update_yaxes(
                title_text= "Total Infractions",
                showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
                showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
                
                row= row_num, col= col_num)
        else:
            fig.update_yaxes(
                title_text= "",
                showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
                showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
                
                row= row_num, col= col_num)

        fig.add_annotation(
            xref="x domain", yref="y domain",
            x=0.0, y=1.0,
            text= f"{col}",
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
        
        fig.add_annotation(
            xref="x domain", yref="y domain",
            x=0.0, y=0.0,
            text= f"COV: {total_cov}<br>Contractor: {total_contractor}<br>Linehaul: {total_linehaul}",
            showarrow=False,
            font=dict(
                size=12,
                color="black"
            ),
            align="left",
            bordercolor="black",
            borderwidth=1,
            borderpad=2,
            bgcolor="white",
            opacity=0.9,
            row= row_num, col= col_num
        )
        
        col_num += 1
        
        if col_num == 4:
            row_num += 1
            col_num = 1

    return fig
