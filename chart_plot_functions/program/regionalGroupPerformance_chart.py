import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.program.regionalGroupPerformance_tableData import regionalGroupPerformance_tableData

def regionalGroupPerformance_chart(regionGroupPerformance_table, fig, domain_y_low, domain_y_high, row_num, col_num):

    regionGroupPerformance_table, regionGroupPerformance_table_colors = regionalGroupPerformance_tableData(regionGroupPerformance_table)

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
            fill_color= regionGroupPerformance_table_colors,
            align= 'center',
            line_color='darkslategray',
            font= dict(color='black'),
            ),
    ), row= row_num, col= col_num)
    fig.update_traces(domain_x=[0,0.30], domain_y=[domain_y_low, domain_y_high], selector=dict(type='table'), row= row_num, col= col_num)

    return fig