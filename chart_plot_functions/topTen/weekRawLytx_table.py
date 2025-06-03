import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.topTen.weekRawLytx_tableData import rawLytxData

def weekRawLytx_table(ending_date_str, behavior_list, return_fig, fig=None):
    """
    Create a table for the top ten Lytx raw data for the week ending on the specified date.
    
    Parameters:
    ending_date_str (str): The ending date in 'YYYY-MM-DD' format.
    
    Returns:
    fig: A Plotly figure containing the table.
    """

    data_dict = rawLytxData(ending_date_str, behavior_list)
    
    # Define a list of six light colors for table backgrounds
    light_colors = ["#FFEBEE", "#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5", "#E0F7FA"]

    if return_fig:

        for i, (k, v) in enumerate(data_dict.items()):
            row = i // 3 + 1  # Adjust row calculation for 3 columns
            col = i % 3 + 1  # Adjust column calculation for 3 columns
            vehicles = list(v.keys())  # Vehicle names
            drivers = [v[x]['driver'] for x in v.keys()]
            counts = [v[x]['count'] for x in v.keys()]
            
            # Rotate through the light colors for each table
            table_color = light_colors[i % len(light_colors)]
            
            fig.add_trace(
                go.Table(
                    header=dict(
                        values=["Vehicle".title(), "Driver".title(), "Count".title()],  # Title case for headers
                        align="center",  # Center-align header text
                        fill_color="lightgrey",  # Header background color
                        font=dict(color="black", size=20),  # Increase header font size
                        height=40,  # Increase header height
                        line=dict(color="black", width=1),  # Add border to header cells
                    ),
                    cells=dict(
                        values=[vehicles, drivers, counts],
                        align="center",  # Center-align cell text
                        fill_color=[
                            [table_color if j % 2 == 0 else "white" for j in range(len(vehicles))]
                        ],  # Striped rows
                        font=dict(color="black", size=16),  # Increase cell font size
                        height=30,  # Increase cell height for padding
                        line=dict(color="black", width=1),  # Add border to body cells
                    ),
                ),
                row=row,
                col=col,
            )
        return fig
    else:
        return data_dict
    
