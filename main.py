import pandas as pd

from cleaning_data import cleaning_events_data

from charts.categoricalResults_chart import categoricalResults_chart
from charts.topTenResults_chart import topTen_Tables
from charts.programResults_chart import programResults_chart

def main(starting_date_str, ending_date_str):

    # Creates the new data for the given date range
    # for date in pd.date_range(start=starting_date_str, end=ending_date_str, freq='D'):
    #     cleaning_events_data(date.strftime('%Y-%m-%d'))
    #     print(f"Data for {date.strftime('%Y-%m-%d')} cleaned and inserted into the database.")

    # Generate categorical results chart
    categoricalResults_chart(ending_date_str)

    # Generate top ten tables
    topTen_Tables(ending_date_str)

    # Generate program results chart
    programResults_chart(ending_date_str)

if __name__ == "__main__":
    main("2025-05-24", "2025-05-30")