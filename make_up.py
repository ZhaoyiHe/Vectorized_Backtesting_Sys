import pandas as pd


def make_up_suspended_dates(trading_days,return_position_df):
    updated_df = pd.merge(trading_days,return_position_df)
    updated_df['returns'] = updated_df['returns'].fillna(method="ffill")
    updated_df['position'] = updated_df['position'].fillna(0)
    return updated_df