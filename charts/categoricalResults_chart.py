from plotly.subplots import make_subplots
import datetime as dt

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from functions.chart_data_creation import weeklyInfractionsTotalPerCategory_data, monthlyGroupPreformanceTable_data

from chart_plot_functions.categorical.infractionFrequencyCategory_chart import infractionFrequencyCategory_chart
from chart_plot_functions.categorical.regionalGroupPerformanceWeekly_table import regionalGroupPerformanceWeekly_table
from chart_plot_functions.categorical.infractionsTotalsPerCategory_Table import infractionsTotalsPerCategory_Table
from chart_plot_functions.categorical.infractionFrequencyPerBehavior_chart import infractionFrequencyPerBehavior_chart


from chart_plot_functions.program.regionalGroupPerformance_chart import regionalGroupPerformance_chart


from chart_plot_functions.functions.add_annotation import add_annotation


def categoricalResults_chart(ending_date_str):

    weekly_total_data, weekly_grouped_data = weeklyInfractionsTotalPerCategory_data(ending_date_str, days_num=200)

    regionGroupPerformance_table = monthlyGroupPreformanceTable_data(ending_date_str, months_num=3)


    # start chart construction
    fig = make_subplots(
        rows=16, 
        cols=3, 
        start_cell="top-left",
        vertical_spacing= 0.01,
        horizontal_spacing= 0.03,
        row_heights=[3, 1.5, 4, 4, 0.15, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # Adjust these values as needed

        column_widths= [1, 1, 1],
        
        specs=[
            [{"colspan": 3, "rowspan": 1}, None, None],
            [{"colspan": 1, "rowspan": 1, 'type': 'table'}, {"colspan": 2, "rowspan": 1, 'type': 'table'}, None],
            [{"colspan": 3, "rowspan": 1, 'type': 'table'}, None, None],
            [{"colspan": 3, "rowspan": 1, 'type': 'table'}, None, None],
            [{}, {}, {}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
            [{"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}, {"colspan": 1, "rowspan": 1}],
        ],
        subplot_titles=(
            "<span style='text-decoration: underline; font-weight: bold; color: black;'>Infraction Frequency per Category</span>",
            # "<span style='text-decoration: underline; font-weight: bold; color: black; '>Monthly Region and Group Performance</span>",
            # "<span style='text-decoration: underline; font-weight: bold; color: black; '>Weekly Region and Group Performance</span>",
        )
    )

    # Chart: ROW 1, COL 1
    fig = infractionFrequencyCategory_chart(weekly_total_data, regionGroupPerformance_table, fig, row_num=1, col_num=1)

    # Chart: ROW 2, COL 1
    fig = regionalGroupPerformance_chart(regionGroupPerformance_table, fig, domain_y_low=0.75, domain_y_high=0.865, row_num=2, col_num=1)
    # Chart: ROW 2, COL 2
    fig = regionalGroupPerformanceWeekly_table(regionGroupPerformance_table, weekly_total_data, fig, row_num=2, col_num=2)

    fig = add_annotation(fig, x=0.50, y=0.82, text="<span style='text-decoration: underline; font-weight: bold; '>Infractions Totals and per Category</span>", textangle=0)

    fig = infractionsTotalsPerCategory_Table(weekly_grouped_data, fig, row_num=3, col_num=1)

    fig = add_annotation(fig, x=0.50, y=0.501, text="Infraction Frequency per Behavior", textangle=0) # font=dict(size=30, color='black'),
    fig = add_annotation(fig, x=1.00, y=0.818, text="Legend: COV | Contractor | Linehaul", textangle=0) # font=dict(size=15, color='black'),

    fig = infractionFrequencyPerBehavior_chart(weekly_grouped_data, fig, row_num=6, col_num=1)


    fig.update_layout(
        # showlegend=False,
        height= 3200,
        width=1850,
        title_text=f"<span style='font-size: 24px; font-weight: bold; color: black;'>LYTX Categorical Results Week: {(dt.datetime.strptime(ending_date_str, '%Y-%m-%d') - dt.timedelta(days=6)).strftime('%Y-%m-%d')} - {ending_date_str}</span>",

    )

    fig.show()

    fig.write_html(f"created_charts/categoricalLytx.html", include_plotlyjs="cdn")

