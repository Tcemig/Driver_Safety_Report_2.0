import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from plotly.colors import n_colors
import datetime as dt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.chart_data_creation import overviewProgramPerformance_data, weeklyInfractionsTotalPerCategory_data

from chart_plot_functions.program.overviewPrographPerformance_chart import overviewProgramPerformance_chart
from chart_plot_functions.program.regionalGroupPerformance_chart import regionalGroupPerformance_chart

def programResults_chart(ending_date_str):

    overview_data = overviewProgramPerformance_data(ending_date_str)

    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str)


    def pulling_week_label(backwards_week):
        """
        Pulls the week label from the DataFrame based on the number of weeks to go backwards. overview_data is the DataFrame containing the week labels.
        """
        if backwards_week < 0 or backwards_week >= len(overview_data):
            raise ValueError("Invalid number of weeks to go backwards.")
        return overview_data.iloc[-(backwards_week + 1)]['week_label']


    # Pulls the 6 highest trending behaviors from the weekly grouped data
    group_trending_list = weekly_grouped_data[weekly_grouped_data['behaviorsName'] != '']['behaviorsName'].value_counts().nlargest(6).index.tolist()



    fig = make_subplots(
        rows=12, 
        cols=3, 
        start_cell="top-left",
        vertical_spacing= 0.04,
        horizontal_spacing= 0.06,
        column_widths= [1, 1, 1],

        specs=[
            [{"colspan": 3, "rowspan": 2}, None, None],
            [None, None, None],
            [{"colspan": 1, 'type': 'table', "rowspan": 1}, {"colspan": 1, "type": 'table', "rowspan": 1}, {"colspan": 1, "type": 'table', "rowspan": 1}],
            [{"colspan": 1}, {"colspan": 2}, None],
            [{"rowspan": 3, "colspan": 1}, {"colspan": 2}, None],
            [None, {"colspan": 2}, None],
            [None, {"colspan": 2}, None],
            [{}, {}, {}],
            [{}, {}, {}],
            [{"rowspan": 3, "colspan": 1}, {"colspan": 2}, None],
            [None, {"colspan": 2}, None],
            [None, {"colspan": 2}, None],
        ],

        subplot_titles=(
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Overview of Program Performance - Frequency</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Region and Group Performance</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>COV Events & Incidents Monthly</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>COV Events & Incidents Weekly</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Near Collisions - Trend</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Near Collisions - Behaviors - Past 12 Weeks</span>",
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Behavior Profile: Sum 12 Weeks</span>",         
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[0]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[1]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[2]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[3]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[4]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[5]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>Non-Priority Behavior Profile: Sum 12 Weeks</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Non-Priority Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Non-Priority Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Non-Priority Behavior Profile</span>",
        
        )
    )

    # Chart: ROW 1, COL 1
    fig = overviewProgramPerformance_chart(overview_data, fig, row_num=1, col_num=1)

    # Table: ROW 3, COL 1
    fig = regionalGroupPerformance_chart(ending_date_str, fig, row_num=3, col_num=1)







    fig.update_layout(
        showlegend=False,
        height= 3200,
        width=1850,
        title_text=f"<span style='font-size: 24px; font-weight: bold; color: black;'>LYTX Program Results Week: {pulling_week_label(0)} {(dt.datetime.strptime(pulling_week_label(0), '%Y-%m-%d') + dt.timedelta(days=7)).strftime('%Y-%m-%d')}</span>",        
        # Overview of Program Performance - Frequency
        xaxis= dict(domain= [0.0, 1.0]),
        yaxis= dict(domain= [0.85, 0.998]),
        
        # Near Collisions - Trend
        yaxis3= dict(domain= [0.76, 0.82]),
        
        # Near Collisions - Behaviors - Past 12 Weeks
        xaxis4= dict(domain= [0.47, 1.0]),
        yaxis4= dict(domain= [0.62, 0.679]),

        # Behavior Profile: Sum 12 Weeks
        yaxis5= dict(domain= [0.44, 0.599]),

        # Current Week Behavior Profile
        xaxis6= dict(domain= [0.47, 1.00]),
        yaxis6= dict(domain= [0.54, 0.599]),

        # Past Week Behavior Profile
        xaxis7= dict(domain= [0.47, 1.00]),
        yaxis7= dict(domain= [0.458, 0.518]),

        # Past 2 Week Behavior Profile
        xaxis8= dict(domain= [0.47, 1.00]),
        yaxis8= dict(domain= [0.39, 0.439]),
        
        # First row of dynamic updating charts
        yaxis9= dict(domain=[0.32, 0.358]),
        yaxis10= dict(domain=[0.32, 0.358]),
        yaxis11= dict(domain=[0.32, 0.358]),
        
        # Second row of dynamic updating charts
        yaxis12= dict(domain=[0.24, 0.278]),
        yaxis13= dict(domain=[0.24, 0.278]),
        yaxis14= dict(domain=[0.24, 0.278]),
        
        # Non-Priority Behavior Profile: Sum 12 Weeks
        yaxis15= dict(domain=[0.0, 0.198]),
        
        # Current Week Non-Priority Behavior Profile
        xaxis16= dict(domain= [0.47, 1.00]),
        yaxis16= dict(domain= [0.14, 0.198]),

        # Past Week Non-Priority Behavior Profile
        xaxis17= dict(domain= [0.47, 1.00]),
        yaxis17= dict(domain= [0.06, 0.118]),

        # Past 2 Week Non-Priority Behavior Profile
        xaxis18= dict(domain= [0.47, 1.00]),
        yaxis18= dict(domain= [0.0, 0.038]),
        )
    fig.show()



programResults_chart(ending_date_str='2025-05-20')

