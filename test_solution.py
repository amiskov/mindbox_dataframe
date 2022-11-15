import pandas as pd
from datetime import timedelta, datetime
from solution import add_session_id
from random import randint, shuffle
from typing import Optional


def test_data():
    data = {}

    # The earliest timestamp is `15 Nov 2022 12:00:00`.
    start = datetime(year=2022, month=11, day=15, hour=12, minute=00)

    # There are 3 customers. Problem: `customer_id=1` has no timestamps.
    sorted_customer_ids = [3, 3, 3, 3, 2, 3, 2, 2, 1, 1]
    sorted_visits: list[Optional[datetime]] = [
        # session_id = 1, customer_id = 3
        start,
        (start + timedelta(minutes=1)),
        (start + timedelta(minutes=2)),
        (start + timedelta(minutes=3)),

        # session_id = 2, customer_id = 2
        (start + timedelta(minutes=10)),

        # session_id = 3, customer_id = 3
        (start + timedelta(minutes=11)),

        # session_id = 4, customer_id = 2
        (start + timedelta(minutes=12)),
        (start + timedelta(minutes=13)),

        # session_id = -1, customer_id = 1
        None,
        None,
    ]

    # Shuffle customer_is and timestamps at once (with the same order)
    customer_time = list(zip(sorted_customer_ids, sorted_visits))
    shuffle(customer_time)
    shuffled_customer_ids, shuffled_visits = zip(*customer_time)

    # Create DataFrame
    data['customer_id'] = pd.array(shuffled_customer_ids)
    data['time'] = pd.array(
        [t.strftime('%H:%M:%S') if t else None for t in shuffled_visits])
    data['timestamp'] = pd.array(
        [int(t.timestamp()) if t else pd.NA for t in shuffled_visits])
    data['product_id'] = [randint(111, 222) for _ in range(10)]
    df = pd.DataFrame(data=data)

    # Add `session_id` column
    add_session_id(df)

    # 1st session, 3rd customer
    s1 = df.iloc[0].session_id
    assert df.iloc[0].customer_id == 3
    assert s1 == df.iloc[0].customer_id + df.iloc[0].timestamp
    assert s1 == df.iloc[1].session_id
    assert s1 == df.iloc[2].session_id
    assert s1 == df.iloc[3].session_id

    # 2nd session, 2nd customer
    s2 = df.iloc[4].session_id
    assert df.iloc[4].customer_id == 2
    assert s2 not in df.iloc[0:4].session_id.unique()
    assert s2 not in df.iloc[5:].session_id.unique()

    # 3rd session, 3rd customer
    s3 = df.iloc[5].session_id
    assert df.iloc[5].customer_id == 3
    assert s3 not in df.iloc[0:5].session_id.unique()
    assert s3 not in df.iloc[6:].session_id.unique()

    # 4th session, 2nd customer
    s4 = df.iloc[6].session_id
    assert df.iloc[6].customer_id == 2
    assert df.iloc[7].customer_id == 2
    assert s4 == df.iloc[7].session_id

    # -1st session, 1st customer
    assert df.iloc[8].session_id == -1 and df.iloc[8].customer_id == 1
    assert df.iloc[9].session_id == -1 and df.iloc[9].customer_id == 1
