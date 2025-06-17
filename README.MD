# LYTX Weekly Report 2.0

This project generates weekly reports and interactive charts from LYTX data, including top 10 behaviors, categorical results, and program results. The reports are visualized using Plotly and exported as HTML files.

## Directory Structure

.
├── .env                         # Environment variables
├── .gitignore                   # Git ignore file
├── cleaning_data.py             # Script for cleaning raw data
├── converting_csv_to_sql.py     # Script for converting CSV data to SQL database
├── data_dict.json               # Data dictionary for reference
├── lytx_weekly_reports.db       # SQLite database with LYTX data
├── main.py                      # Main entry point for generating reports
├── chart_data_functions/        # Functions for preparing chart data
│   ├── categorical/
│   ├── program/
│   └── topTen/
├── chart_plot_functions/        # Functions for plotting charts
│   ├── categorical/
│   ├── functions/
│   ├── program/
│   └── topTen/
├── charts/                      # Chart generation scripts
│   ├── categoricalResults_chart.py
│   ├── programResults_chart.py
│   ├── topTenResults_chart.py
│   └── __pycache__/
├── created_charts/              # Output HTML charts
│   ├── categoricalLytx.html
│   ├── programLytx.html
│   └── topTenLytx.html
├── functions/                   # Utility and helper functions
├── LYTX_API/                    # LYTX API integration (if applicable)
└── temp_json_files/             # Temporary JSON files

## Usage

1. **Set up your environment**  
   Add necessary environment variables to `.env`.

2. **Prepare the data**  
   - On `main.py` uncomment the running data lines 12-14 to run the new data

3. **Generate Charts**  
   - Run `main.py` to generate all reports and charts.
   - Individual chart scripts are in the `charts/` directory.

4. **View Results**  
   - Open the HTML files in `created_charts/` to view interactive charts.

## Requirements

- Python 3.11+
- [Plotly](https://plotly.com/python/)
- Other dependencies as specified in your environment

## Notes

- Chart data and plotting logic are modularized in `chart_data_functions/` and `chart_plot_functions/`.
- Output charts are saved as standalone HTML files for easy sharing.
- `converting_csv_to_sql.py` used to convert already existing data to format in sqlite3 file.

---

For more details, see the individual scripts and modules.