import sqlite3
import pandas as pd

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from LYTX_API.restAPI import pull_LYTX_events_behaviors


def updating_allBehaviors():
    """
    This function updates all the behaviors in the system.
    """
    # Get all behaviors
    all_behaviors_dict = pull_LYTX_events_behaviors()
    all_behaviors_df = pd.DataFrame(all_behaviors_dict)
    all_behaviors_df = all_behaviors_df[['id', 'name']]

    # Connect to the database
    conn = sqlite3.connect('lytx_weekly_reports.db')
    cursor = conn.cursor()
    # Prepare columns and values
    columns = list(all_behaviors_df.columns)
    columns_str = ', '.join(columns)
    placeholders = ', '.join(['?'] * len(columns))

    # Insert each row with INSERT OR IGNORE
    # if a primary key or unique constraint violation occurs, the row will be ignored
    for row in all_behaviors_df.itertuples(index=False, name=None):
        cursor.execute(
            f'INSERT OR IGNORE INTO lytxAllBehaviors ({columns_str}) VALUES ({placeholders})',
            row
        )

    conn.commit()
    conn.close()

updating_allBehaviors()

    