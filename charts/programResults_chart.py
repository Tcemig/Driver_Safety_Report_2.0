from plotly.subplots import make_subplots
import datetime as dt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.chart_data_creation import overviewProgramPerformance_data, weeklyInfractionsTotalPerCategory_data, monthlyGroupPreformanceTable_data, covEventsAndIncidents_data, Pulling_SmartSheet_data

from chart_plot_functions.program.overviewPrographPerformance_chart import overviewProgramPerformance_chart
from chart_plot_functions.program.regionalGroupPerformance_chart import regionalGroupPerformance_chart
from chart_plot_functions.program.covEventsIncidents_chart import covEventsIncidentsMonthly_chart, covEventsIncidentsWeekly_chart
from chart_plot_functions.program.nearCollisionSumTrend_chart import nearCollision_sumTrend_chart
from chart_plot_functions.program.nearCollisionBehaviors_chart import nearCollision_behaviorsTrend_chart
from chart_plot_functions.program.behavior_sumTrend_chart import behavior_sumTrend_chart
from chart_plot_functions.program.weekBehavior_chart import oneWeekBehavior_chart
from chart_plot_functions.program.individualBehaviorWeekly_chart import individualBehaviorWeekly_chart

from chart_plot_functions.functions.add_annotation import add_annotation

def programResults_chart(ending_date_str):

    overview_data = overviewProgramPerformance_data(ending_date_str)

    regionGroupPerformance_table = monthlyGroupPreformanceTable_data(ending_date_str, months_num=3)

    covEI_data = covEventsAndIncidents_data(ending_date_str)

    smartSheet_data = Pulling_SmartSheet_data()

    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num=200)
    last_week_grouped_data = weekly_grouped_data[weekly_grouped_data['week_label'].isin(weekly_grouped_data['week_label'].unique()[-1:])]  # Get the last 12 weeks of data
    # Pulls the 6 highest trending behaviors from the weekly grouped data
    group_trending_list = last_week_grouped_data[last_week_grouped_data['behaviorsName'] != '']['behaviorsName'].value_counts().nlargest(6).index.tolist()

    def pulling_week_label(backwards_week):
        """
        Pulls the week label from the DataFrame based on the number of weeks to go backwards. overview_data is the DataFrame containing the week labels.
        """
        if backwards_week < 0 or backwards_week >= len(overview_data):
            raise ValueError("Invalid number of weeks to go backwards.")
        return overview_data.iloc[-(backwards_week + 1)]['week_label']





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
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(1)} Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(2)} Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[0]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[1]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[2]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[3]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[4]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{group_trending_list[5]} Trend</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>Non-Priority Behavior Profile: Sum 12 Weeks</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(0)} Non-Priority Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(1)} Non-Priority Behavior Profile</span>",
            f"<span style='text-decoration: underline; font-weight: bold; color: black;'>{pulling_week_label(2)} Non-Priority Behavior Profile</span>",
        
        )
    )

    # Chart: ROW 1, COL 1
    fig = overviewProgramPerformance_chart(overview_data, fig, row_num=1, col_num=1)

    # Table: ROW 3, COL 1
    # domain_y=[0.76, 0.824]
    fig = regionalGroupPerformance_chart(regionGroupPerformance_table, fig, domain_y_low=0.76, domain_y_high=0.824, row_num=3, col_num=1)

    # Table: ROW 3, COL 2
    fig = covEventsIncidentsMonthly_chart(covEI_data, smartSheet_data, fig, row_num=3, col_num=2)

    # Table: ROW 3, COL 3
    fig = covEventsIncidentsWeekly_chart(covEI_data, smartSheet_data, fig, row_num=3, col_num=3)

    # Chart: ROW 4, COL 1
    fig = nearCollision_sumTrend_chart(weekly_grouped_data, fig, row_num=4, col_num=1)

    # Chart: ROW 4, COL 2
    fig = nearCollision_behaviorsTrend_chart(weekly_grouped_data, fig, row_num=4, col_num=2)

    # Chart: ROW 5, COL 1
    fig = behavior_sumTrend_chart(weekly_grouped_data, fig, nonPriority=True, row_num=5, col_num=1)


    # Chart: ROW 5, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=True, row_num=5, col_num=2, weekDate_str=pulling_week_label(0))
    # Add custom annotation to the bar chart
    fig.add_annotation(
        xref="x domain", yref="y",
        x=1.0, y=0.25,
        text="% = previous weeks behavior / current weeks behavior",
        showarrow=False,
        font=dict(
            size=14,
            color="black"
        ),
        align="center",
        bordercolor="black",
        borderwidth=1,
        borderpad=2,
        bgcolor="white",
        opacity=0.9,
        row= 5, col= 2
    )
    # Chart: ROW 6, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=True, row_num=6, col_num=2, weekDate_str=pulling_week_label(1))
    # Chart: ROW 7, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=True, row_num=7, col_num=2, weekDate_str=pulling_week_label(2))


    # Annotation Titles the 6 dynamic charts below
    fig.add_annotation(
        x=0.5,
        y=0.408,
        xref="paper",
        yref="paper",
        text="<span style='text-decoration: underline; font-weight: bold;'>Charts below represent the 6 highest behaviors for last week</span>",
        showarrow=False,
        font=dict(size=22, color='black'),
    )
    # Chart: ROW 8, COL 1
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[0], fig, row_num=8, col_num=1)
    # Chart: ROW 8, COL 2
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[1], fig, row_num=8, col_num=2)
    # Chart: ROW 8, COL 3
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[2], fig, row_num=8, col_num=3)
    # Chart: ROW 9, COL 1
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[3], fig, row_num=9, col_num=1)      
    # Chart: ROW 9, COL 2
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[4], fig, row_num=9, col_num=2)
    # Chart: ROW 9, COL 3
    fig = individualBehaviorWeekly_chart(weekly_grouped_data, group_trending_list[5], fig, row_num=9, col_num=3)

    # Chart: ROW 10, COL 1
    fig = behavior_sumTrend_chart(weekly_grouped_data, fig, nonPriority=False, row_num=10, col_num=1)

    # Chart: ROW 10, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=False, row_num=10, col_num=2, weekDate_str=pulling_week_label(0))
    # Chart: ROW 11, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=False, row_num=11, col_num=2, weekDate_str=pulling_week_label(1))
    # Chart: ROW 12, COL 2
    fig = oneWeekBehavior_chart(weekly_grouped_data, fig, nonPriority=False, row_num=12, col_num=2, weekDate_str=pulling_week_label(2))



    # Add annotations to the charts
    fig = add_annotation(fig, x=1.015, y=0.622, text="Coachable Behaviors", textangle=-90)
    fig = add_annotation(fig, x=1.015, y=0.531, text="Coachable Behaviors", textangle=-90)
    fig = add_annotation(fig, x=1.015, y=0.452, text="Coachable Behaviors", textangle=-90)

    fig = add_annotation(fig, x=1.015, y=0.157, text="Coachable Behaviors", textangle=-90)
    fig = add_annotation(fig, x=1.015, y=0.072, text="Coachable Behaviors", textangle=-90)
    fig = add_annotation(fig, x=1.015, y=0.00, text="Coachable Behaviors", textangle=-90)



    fig.update_layout(
        showlegend=False,
        height= 3200,
        width=1850,
        title_text=f"<span style='font-size: 24px; font-weight: bold; color: black;'>LYTX Program Results Week: {pulling_week_label(0)} {(dt.datetime.strptime(pulling_week_label(0), '%Y-%m-%d') + dt.timedelta(days=7)).strftime('%Y-%m-%d')}</span>",        
        # Overview of Program Performance - Frequency
        xaxis= dict(domain= [0.0, 1.0]),
        yaxis= dict(domain= [0.85, 0.998]),
        
        # Near Collisions - Trend
        yaxis2= dict(domain= [0.683, 0.739]),
        
        # Near Collisions - Behaviors - Past 12 Weeks
        xaxis3= dict(domain= [0.47, 1.0]),
        yaxis3= dict(domain= [0.67, 0.739]),

        # Behavior Profile: Sum 12 Weeks
        yaxis4= dict(domain= [0.495, 0.65]),

        # Current Week Behavior Profile
        xaxis5= dict(domain= [0.47, 1.00]),
        yaxis5= dict(domain= [0.585, 0.652]),

        # Past Week Behavior Profile
        xaxis6= dict(domain= [0.47, 1.00]),
        yaxis6= dict(domain= [0.495, 0.565]),

        # Past 2 Week Behavior Profile
        xaxis7= dict(domain= [0.47, 1.00]),
        yaxis7= dict(domain= [0.425, 0.478]),
        
        # First row of dynamic updating charts
        yaxis8= dict(domain=[0.33, 0.392]),
        yaxis9= dict(domain=[0.33, 0.392]),
        yaxis10= dict(domain=[0.33, 0.392]),
        
        # Second row of dynamic updating charts
        yaxis11= dict(domain=[0.245, 0.305]),
        yaxis12= dict(domain=[0.245, 0.305]),
        yaxis13= dict(domain=[0.245, 0.305]),
        
        # Non-Priority Behavior Profile: Sum 12 Weeks
        yaxis14= dict(domain=[0.0, 0.218]),
        
        # Current Week Non-Priority Behavior Profile
        xaxis15= dict(domain= [0.47, 1.00]),
        yaxis15= dict(domain= [0.15, 0.218]),

        # Past Week Non-Priority Behavior Profile
        xaxis16= dict(domain= [0.47, 1.00]),
        yaxis16= dict(domain= [0.063, 0.131]),

        # Past 2 Week Non-Priority Behavior Profile
        xaxis17= dict(domain= [0.47, 1.00]),
        yaxis17= dict(domain= [0.0, 0.045]),
        )
    fig.show()



programResults_chart(ending_date_str='2025-05-30')

