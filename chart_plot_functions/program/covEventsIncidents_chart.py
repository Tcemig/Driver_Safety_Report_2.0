import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_plot_functions.functions.table_sequence_color import get_weekly_table_colors

from chart_data_functions.program.covEventsIncidents_tableData import covEventsIncidents_tableData

def covEventsIncidentsMonthly_chart(covEI_data, smartSheet_data, fig, row_num, col_num):

    weeklyCovEI, monthlyCovEI = covEventsIncidents_tableData(covEI_data, smartSheet_data)
    monthlyCovEI_Color = monthlyCovEI.copy()

    fill_colors = get_weekly_table_colors(monthlyCovEI_Color, ['Total VI At Fault', 'Total VI No Fault', 'Total VI Shared Fault'])
    

    cell_values_2 = []
    cell_headers_2 = []
    for cell_v in monthlyCovEI.columns:
        cell_values_2.append(monthlyCovEI[f"{cell_v}"])
        cell_headers_2.append(f"<b>{cell_v}</b>")
    fig.add_trace(go.Table(
        header= dict(
            values= cell_headers_2,
            fill_color= 'lightgray',
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black', size=10)
            ),
        cells= dict(
            values= cell_values_2, 
            fill_color= fill_colors,
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black'),
            ),
    ), row= row_num, col= col_num)
    fig.update_traces(domain_x=[0.31,0.66], domain_y=[0.76, 0.824], selector=dict(type='table'), row= row_num, col= col_num)

    return fig

def covEventsIncidentsWeekly_chart(covEI_data, smartSheet_data, fig, row_num, col_num):

    weeklyCovEI, monthlyCovEI = covEventsIncidents_tableData(covEI_data, smartSheet_data)
    weeklyCovEI_Color = weeklyCovEI.copy()

    cell_values_2 = []
    cell_headers_2 = []
    for cell_v in weeklyCovEI.columns:
        cell_values_2.append(weeklyCovEI[f"{cell_v}"])
        cell_headers_2.append(f"<b>{cell_v}</b>")

    fill_colors = get_weekly_table_colors(weeklyCovEI_Color, ['Total VI At Fault', 'Total VI No Fault', 'Total VI Shared Fault'])

    fig.add_trace(go.Table(
        header= dict(
            values= cell_headers_2,
            fill_color= 'lightgray',
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black', size=10)
            ),
        cells= dict(
            values= cell_values_2, 
            fill_color= fill_colors,
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black'),
            ),
        columnwidth= [120, 100, 100, 100, 100, 100, 100, 100],
    ), row= row_num, col= col_num)
    fig.update_traces(domain_x=[0.67,1.0], domain_y=[0.76, 0.824], selector=dict(type='table'), row= row_num, col= col_num)

    return fig