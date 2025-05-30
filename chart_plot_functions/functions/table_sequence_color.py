import matplotlib.colors as mcolors

def get_weekly_table_colors(df, highlight_cols):
    row_colors = ['white', 'lightgray']
    
    fill_colors = []

    for col in df.columns:
        col_colors = []
        for i, val in enumerate(df[col]):
            # Alternate row background
            base_color = row_colors[i % 2]
            # Highlight logic for specific columns
            if col in highlight_cols and i > 0:
                prev_val = df[col].iloc[i-1]
                if val < prev_val:
                    col_colors.append('lightgreen')
                elif val > prev_val:
                    col_colors.append('lightcoral')
                else:
                    col_colors.append(base_color)
            else:
                col_colors.append(base_color)
        fill_colors.append(col_colors)
    return fill_colors

def get_monthly_table_colors(df, highlight_cols):
    row_colors = ['white', 'lightgray']
    fill_colors = []

    # Define a colormap from red to green
    cmap = mcolors.LinearSegmentedColormap.from_list("red_green", ["red", "green"])

    for col in df.columns:
        col_colors = []
        if col in highlight_cols:
            # Normalize the column values between 0 and 1
            col_vals = df[col].astype(float)
            norm = (col_vals - col_vals.min()) / (col_vals.max() - col_vals.min() + 1e-9)
            # Invert so 0 is green (lowest), 1 is red (highest)
            norm = 1 - norm
        for i, val in enumerate(df[col]):
            base_color = row_colors[i % 2]
            if col in highlight_cols:
                # Get the color from the colormap
                color = mcolors.to_hex(cmap(norm.iloc[i]))
                col_colors.append(color)
            else:
                col_colors.append(base_color)
        fill_colors.append(col_colors)
    return fill_colors