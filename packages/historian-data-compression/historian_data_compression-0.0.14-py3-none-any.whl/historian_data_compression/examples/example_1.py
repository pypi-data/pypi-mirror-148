# -*- coding: utf-8 -*-

"""
Avoid timestamp issues!

    1. sort the dateframe by timestamp
    2. convert negative timestamps in Windows (dates before 1970-01-01)
    
"""

import pandas as pd
from datetime import datetime, timedelta
from historian_data_compression import point_generator, dead_band_compression, swinging_door_compression

df = pd.read_csv(r"https://datahub.io/core/natural-gas/r/daily.csv")
df["Date"] = pd.to_datetime(df["Date"], format="%Y-%m-%d %H:%M:%S")

df = df.sort_values("Date")
days = (datetime(1970, 1, 1) - df.loc[0, "Date"]).total_seconds() / (60 * 60 * 24)
if days > 0:
    days =  int(days) + 100
else:
    days = 0
df["Date"] = df["Date"] + pd.Timedelta(days=days)

max = df["Price"].max()
min = df["Price"].min()
dbc_deadband_perc = 0.5 / 100                                                                       # typically 0.5 %
dbc_deviation = dbc_deadband_perc * (max - min) / 2                                                 # deviation = deadband / 2
dbc_timeout = 0                                                                                     # seconds, but 0 eauals 'no timeout'
swdc_deadband_perc = 1 / 100                                                                        # typically 1.0 %
swdc_deviation = swdc_deadband_perc * (max - min) / 2     
swdc_timeout = 0                                                                                    # seconds, but 0 eauals 'no timeout'

df_dbc = pd.DataFrame(
    tuple(
        {
            "Date": datetime.fromtimestamp(ts),
            "Price": value
        }
        for ts, value in dead_band_compression(
            point_generator(df[["Date", "Price"]]), deviation=dbc_deviation, timeout=dbc_timeout
        )
    )
)
df_dbc_swdc = pd.DataFrame(
    tuple(
        {
            "Date": datetime.fromtimestamp(ts),
            "Price": value
        }
        for ts, value in swinging_door_compression(
            point_generator(df_dbc), deviation=swdc_deviation, timeout=swdc_timeout
        )
    )
)
if days > 0:
    df_dbc["Date"] = df_dbc["Date"] - pd.Timedelta(days=days)
    df_dbc_swdc["Date"] = df_dbc_swdc["Date"] - pd.Timedelta(days=days)
print(
      "Size after 1st stage compression (deadband only):           "
      f"{len(df_dbc) / len(df):>10.1%}"
)
print(
      "Size after 2nd stage compression (deadband + swinging door):"
      f"{len(df_dbc_swdc) / len(df):>10.1%}"
)

