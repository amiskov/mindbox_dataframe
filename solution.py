import pandas as pd
from datetime import timedelta
from pandarallel import pandarallel
from uuid import uuid4


pandarallel.initialize(progress_bar=True)


def add_session_id(df):
    """
    `df` will be modified in-place.
    """
    df.sort_values(by='timestamp', na_position='last', inplace=True)

    SESS_TIME = timedelta(minutes=3).seconds

    cust_id = df.iloc[0].customer_id
    sess_id = uuid4()
    sess_start = df.iloc[0].timestamp

    def f(row):
        nonlocal cust_id
        nonlocal sess_id
        nonlocal sess_start

        if pd.isna(row.timestamp):
            return -1

        if (row.customer_id != cust_id) or (row.timestamp - sess_start > SESS_TIME):
            sess_id = uuid4()
            sess_start = row.timestamp
            cust_id = row.customer_id
        return sess_id
    
    df['session_id'] = df.parallel_apply(f, axis=1)


