import pandas as pd
import numpy as np
from datetime import timedelta, datetime
from solution import add_session_id


def bench(df_size=10 ** 4):
    start = datetime(year=2022, month=11, day=15, hour=12, minute=00)
    end = start + timedelta(minutes=10)
    s = int(start.timestamp())
    e = int(end.timestamp())

    df = pd.DataFrame(data={
        'customer_id': np.random.randint(1, 8, df_size),
        'timestamp': np.random.randint(s, e, df_size),
        'product_id': np.random.randint(111, 888, df_size),
    })

    test_started = datetime.now()
    df.sort_values(by='timestamp', na_position='last', inplace=True)
    add_session_id(df)
    delta = datetime.now() - test_started

    print('\nFinished in', delta.seconds, 'seconds')


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='ProgramName',
        description='What the program does',
        epilog='Text at the bottom of help')
    parser.add_argument('-s', '--ds-size', default=10**4, type=int)
    args = parser.parse_args()
    bench(args.ds_size)
