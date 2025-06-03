import plotly.graph_objects as go
import math
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chart_data_functions.categorical.infractionsTotalsPerCategory_tableData import infractionsTotalsPerCategory_tableData

def safe_int_str(x):
    try:
        return f"{int(float(x))} "
    except (ValueError, TypeError):
        return "0 "

def build_table_section(df_list, columns, weekly_grouped_data):
    cell_values = []
    cell_headers = []
    for cell_v in columns:
        if cell_v == 'week_label':
            # Convert to datetime if not already
            week_series = pd.to_datetime(df_list[0][f'{cell_v}'])
            # Build a list of date ranges for each row
            date_text = [
                f"{dt.month:02d}-{dt.day:02d} to {(dt + pd.Timedelta(days=6)).month:02d}-{(dt + pd.Timedelta(days=6)).day:02d}"
                for dt in week_series
            ]
            cell_values.append(date_text)
            cell_headers.append(f"<b>Week</b>")
        elif cell_v == 'Total':

            temp_cov_total = weekly_grouped_data[weekly_grouped_data['group'] == 'COV'][f'{cell_v}'].sum()
            temp_contractor_total = weekly_grouped_data[weekly_grouped_data['group'] == 'Contractor'][f'{cell_v}'].sum()
            temp_linehaul_total = weekly_grouped_data[weekly_grouped_data['group'] == 'Linehaul'][f'{cell_v}'].sum()
            
            temp_total = temp_cov_total + temp_contractor_total + temp_linehaul_total
            
            interal_temp_all = f"       {temp_total}<br>{temp_cov_total} | {temp_contractor_total} | {temp_linehaul_total}"
            temp_all.append(interal_temp_all)

            cell_values.append(temp_all)
            cell_headers.append(f"<b>{cell_v}</b>")
        else:
            temp_cov = df_list[0][f'{cell_v}'].values if cell_v in df_list[0].columns else ['0 ' for _ in range(len(df_list[0]))]
            temp_cov = [safe_int_str(x) for x in temp_cov]
            # temp_cov = ['0 ' if str(x).strip().lower() == 'nan' or (isinstance(x, float) and math.isnan(x)) else x for x in temp_cov]

            temp_contractor = df_list[1][f'{cell_v}'].values if cell_v in df_list[1].columns else ['0 ' for _ in range(len(df_list[0]))]
            temp_contractor = [safe_int_str(x) for x in temp_contractor]
            # temp_contractor = ['0 ' if str(x).strip().lower() == 'nan' or (isinstance(x, float) and math.isnan(x)) else x for x in temp_contractor]

            temp_linehaul = df_list[2][f'{cell_v}'].values if cell_v in df_list[2].columns else ['0 ' for _ in range(len(df_list[0]))]
            temp_linehaul = [safe_int_str(x) for x in temp_linehaul]
            # temp_linehaul = ['0 ' if str(x).strip().lower() == 'nan' or (isinstance(x, float) and math.isnan(x)) else x for x in temp_linehaul]

            temp_all = []
            for i in range(len(temp_cov)):
                cov_val = int(str(temp_cov[i]).strip())
                contractor_val = int(str(temp_contractor[i]).strip())
                linehaul_val = int(str(temp_linehaul[i]).strip())
                temp_total = cov_val + contractor_val + linehaul_val
                past_total = int(str(temp_cov[i-1]).strip()) + int(str(temp_contractor[i-1]).strip()) + int(str(temp_linehaul[i-1]).strip())

                try:
                    if (past_total == 0) and (temp_total == 0):
                        total_diff = 0
                    else:
                        total_diff = ((temp_total / past_total) - 1) * 100
                except ZeroDivisionError:
                    total_diff = 100
                try:
                    if (int(temp_cov[i-1]) == 0) and (int(temp_cov[i]) == 0):
                        cov_diff = 0
                    else:
                        cov_diff = ((int(temp_cov[i]) / int(temp_cov[i-1])) - 1) * 100
                except ZeroDivisionError:
                    cov_diff = 100
                except ValueError:
                    cov_diff = 0
                try:
                    if (int(temp_contractor[i-1]) == 0) and (int(temp_contractor[i]) == 0):
                        contractor_diff = 0
                    else:
                        contractor_diff = ((int(temp_contractor[i]) / int(temp_contractor[i-1])) - 1) * 100
                except ZeroDivisionError:
                    contractor_diff = 100
                except ValueError:
                    contractor_diff = 0
                try:
                    if (int(temp_linehaul[i-1]) == 0) and (int(temp_linehaul[i]) == 0):
                        linehaul_diff = 0
                    else:
                        linehaul_diff = ((int(temp_linehaul[i]) / int(temp_linehaul[i-1])) - 1) * 100
                except ZeroDivisionError:
                    linehaul_diff = 100
                except ValueError:
                    linehaul_diff = 0

                diff_dict = {}
                for key, key_text, temp_int in zip([total_diff, cov_diff, contractor_diff, linehaul_diff], ['Total', 'COV', 'Contractor', 'Linehaul'], [temp_total, temp_cov[i], temp_contractor[i], temp_linehaul[i]]):
                    if key < -40.00:
                        diff_text = f"<span style='color: darkgreen; font-weight: bold;'>{temp_int}</span>"
                    elif key < -20.00:
                        diff_text = f"<span style='color: green; font-weight: bold;'>{temp_int}</span>"
                    elif key < -10.00:
                        diff_text = f"<span style='color: lightgreen; font-weight: bold;'>{temp_int}</span>"
                    elif key > 40.00:
                        diff_text = f"<span style='color: darkred; font-weight: bold;'>{temp_int}</span>"
                    elif key > 20.00:
                        diff_text = f"<span style='color: red; font-weight: bold;'>{temp_int}</span>"
                    elif key > 10.00:
                        diff_text = f"<span style='color: lightcoral; font-weight: bold;'>{temp_int}</span>"
                    else:
                        diff_text = f"{temp_int}"

                    diff_dict[key_text] = diff_text

                interal_temp_all = f"       {diff_dict['Total']}<br>{diff_dict['COV']} | {diff_dict['Contractor']} | {diff_dict['Linehaul']}"
                temp_all.append(interal_temp_all)

            cell_values.append(temp_all)
            cell_headers.append(f"<b>{cell_v}</b>")
    return cell_headers, cell_values

def infractionsTotalsPerCategory_Table(weekly_grouped_data, fig, row_num, col_num):
    weekly_grouped_data, weekly_total_data = infractionsTotalsPerCategory_tableData(weekly_grouped_data)

    week_list = weekly_grouped_data['week_label'].unique().tolist()
    all_behaviors = weekly_grouped_data['behaviorsName'].unique().tolist()
    first_half = ['week_label'] + all_behaviors[:len(all_behaviors)//2]
    second_half = ['week_label'] + all_behaviors[len(all_behaviors)//2:] + ['Total']

    cov_df = weekly_grouped_data[weekly_grouped_data['group'] == 'COV'].reset_index(drop=True).pivot(index='week_label', columns='behaviorsName', values='event_size').reset_index()
    contractor_df = weekly_grouped_data[weekly_grouped_data['group'] == 'Contractor'].reset_index(drop=True).pivot(index='week_label', columns='behaviorsName', values='event_size').reset_index()
    linehaul_df = weekly_grouped_data[weekly_grouped_data['group'] == 'Linehaul'].reset_index(drop=True).pivot(index='week_label', columns='behaviorsName', values='event_size').reset_index()

    # First half
    headers1, values1 = build_table_section([cov_df, contractor_df, linehaul_df], first_half, weekly_grouped_data)
    fig.add_trace(go.Table(
        header=dict(values=headers1, fill_color='lightgray', align='center', line_color='darkslategray', font=dict(color='black')),
        cells=dict(values=values1, fill_color='white', align='center', line_color='darkslategray', font=dict(color='black')),
    ), row=row_num, col=col_num)

    # Second half
    headers2, values2 = build_table_section([cov_df, contractor_df, linehaul_df], second_half, weekly_grouped_data)
    fig.add_trace(go.Table(
        header=dict(values=headers2, fill_color='lightgray', align='center', line_color='darkslategray', font=dict(color='black')),
        cells=dict(values=values2, fill_color='white', align='center', line_color='darkslategray', font=dict(color='black')),
    ), row=row_num+1, col=col_num)

    fig.update_traces(domain_x=[0.0, 1.00], domain_y=[0.65,0.81], selector=dict(type='table'), row= row_num, col= col_num)
    fig.update_traces(domain_x=[0.0, 1.00], domain_y=[0.40,0.65], selector=dict(type='table'), row= row_num+1, col= col_num)

    return fig


    