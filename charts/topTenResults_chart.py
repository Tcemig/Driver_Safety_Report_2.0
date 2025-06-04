from plotly.subplots import make_subplots
import datetime as dt
import plotly.graph_objects as go

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_plot_functions.topTen.weekRawLytx_table import weekRawLytx_table



def topTen_Tables(ending_date_str):

    behavior_list = [
        'aggressive',
        'failed to Stop',
        'posted speed violation',
        'speed policy violation',
        'near collision',
        'near collision - unavoidable',
        'following distance',
        'curb strike',
        'lens obstruction',
        'no seat belt',
        'drowsy',
        'handheld device',
        'inattentive',
        'red light',
        'passenger(s) in vehicle',
        'mirror use',
        'smoking',
        'too fast for conditions',
        'intersection awareness',
        'backing on a roadway',
    ]
    data_dict = weekRawLytx_table(ending_date_str, behavior_list, return_fig=False)

    fig = make_subplots(
        rows=(len(data_dict) + 2) // 3,  # Calculate rows needed for 3 columns
        cols=3,  # Set the number of columns to 3
        subplot_titles=[k.title() for k in data_dict.keys()],  # Convert behavior names to title case
        vertical_spacing=0.01,
        horizontal_spacing=0.01,
        specs=[[{'type': 'domain'} for _ in range(3)] for _ in range((len(data_dict) + 2) // 3)],  # Set all subplots to 'domain'
    )

    fig = weekRawLytx_table(ending_date_str, behavior_list, return_fig=True, fig=fig)

    fig.update_layout(
        height=1900,
        width=1800,
        title=dict(
            text=f"Top 10 Behaviors by Vehicle From LYTX: {(dt.datetime.strptime(ending_date_str, '%Y-%m-%d') - dt.timedelta(days=6)).strftime('%Y-%m-%d')} - {ending_date_str}",
            font=dict(size=24)  # Adjust the font size here
        ),
        showlegend=False,
    )
    fig.show()

    fig.write_html(f"created_charts/topTenLytx.html", include_plotlyjs="cdn")




