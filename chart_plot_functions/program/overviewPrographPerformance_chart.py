import plotly.graph_objects as go
import numpy as np
import datetime as dt

def overviewProgramPerformance_chart(overview_data, fig, row_num, col_num):
    row_num, col_num = 1, 1
    fig.add_trace(go.Scatter(
        x= overview_data['week_label'],
        y= overview_data['avg_event_size'],
        mode= 'lines+markers',
        name= 'Frequency Scored Events',
        ), row= row_num, col= col_num)
    fig.update_xaxes(
        # showticklabels = True,
        nticks= 20,
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    fig.update_yaxes(
        title_text= "Frequency Per Vehicle",
        showline=True, linewidth=2, linecolor='black', mirror=True, # Adds Lines around border of chart
        showgrid=True, gridwidth=1, gridcolor='lightgray', # Adds custom grid in chart
        
        row= row_num, col= col_num)
    
    slope, intercept = np.polyfit(overview_data.index, overview_data['avg_event_size'], 1)
    line_of_best_fit = slope * np.array(overview_data.index) + intercept
    fig.add_trace(go.Scatter(
        x= overview_data['week_label'],
        y= line_of_best_fit,
        mode= 'lines',
        name= 'Line of Best Fit',
        line= dict(color='black'),
        ), row= row_num, col= col_num)

    start_date = dt.datetime.strptime(overview_data.loc[0, 'week_label'], "%Y-%m-%d")
    end_date = dt.datetime.strptime(overview_data.loc[len(overview_data)-1, 'week_label'][:10], "%Y-%m-%d")
    month_Diff = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
    line_of_best_fit_Diff = round(((list(line_of_best_fit)[-1] / list(line_of_best_fit)[0]) -1) *100, 2)
    if line_of_best_fit_Diff > 0:
        annotation_text = f"Behavior frequency per vehicles has increased <span style='color: red;'>{line_of_best_fit_Diff}%</span> on average over the past {month_Diff} months."
    else:
        annotation_text = f"Behavior frequency per vehicles has decreased <span style='color: green;'>{line_of_best_fit_Diff}%</span> on average over the past {month_Diff} months."

    fig.add_annotation(
        xref="x domain", yref="y",
        x=0.0, y= (min(overview_data['avg_event_size']) - 0.35),
        text= annotation_text,
        showarrow=False,
        font=dict(
            size=16,
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

    return fig