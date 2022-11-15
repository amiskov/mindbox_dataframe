import pandas as pd
from datetime import timedelta
from pandarallel import pandarallel

pandarallel.initialize(progress_bar=True)


def add_session_id(df):
    """
    `df` will be modified in-place.
    """
    df.sort_values(by='timestamp', na_position='last', inplace=True)

    SESS_TIME = timedelta(minutes=3).seconds

    first_row = df.iloc[0]
    cust_id = first_row.customer_id
    sess_start = first_row.timestamp
    sess_id = cust_id + sess_start

    def f(row):
        nonlocal cust_id
        nonlocal sess_id
        nonlocal sess_start

        if pd.isna(row.timestamp):
            return -1

        if (row.customer_id != cust_id) or (row.timestamp - sess_start > SESS_TIME):
            cust_id = row.customer_id
            sess_start = row.timestamp
            sess_id = cust_id + sess_start

        return sess_id

    df['session_id'] = df.parallel_apply(f, axis=1)
