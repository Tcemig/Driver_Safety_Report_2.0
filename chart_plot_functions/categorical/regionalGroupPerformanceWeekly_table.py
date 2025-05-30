import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.categorical.regionalGroupPerformanceWeekly_tableData import regionalGroupPerformanceWeekly_tableData

def regionalGroupPerformanceWeekly_table(regionGroupPerformance_table, weekly_total_data, fig, row_num, col_num):

    regionGroupPerformance_table, fill_color = regionalGroupPerformanceWeekly_tableData(regionGroupPerformance_table, weekly_total_data)

    cell_values = []
    cell_headers = []
    for cell_v in regionGroupPerformance_table.columns:
        cell_values.append(regionGroupPerformance_table[f"{cell_v}"])
        cell_headers.append(f"<b>{cell_v}</b>")
    fig.add_trace(go.Table(
        header= dict(
            values= cell_headers,
            fill_color= 'lightgray',
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black')
            ),
        cells= dict(
            values= cell_values, #[finalRGPreformance_df[col] for col in finalRGPreformance_df.columns],
            fill_color= fill_color,
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black'),
            ),
    ), row= row_num, col= col_num)
    fig.update_traces(domain_x=[0.34, 1.00], domain_y=[0.75,0.865], selector=dict(type='table'), row= row_num, col= col_num)

    fig.add_annotation(
        x=0.78,
        y=0.875,
        xref="paper",
        yref="paper",
        text="<span style='text-decoration: underline; font-weight: bold; '>Weekly Region and Group Performance</span>",
        showarrow=False,
        font=dict(size=16, color='black'),
        textangle= 0
    )

    return fig