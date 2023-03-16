import pandas as pd
import numpy as np

def scale_normalize(x, y):
    return x/(np.nanmax(y)-np.nanmin(y))

def normalize(x):
    x = (x-np.nanmin(x))/(np.nanmax(x)-np.nanmin(x)) # normalize x between 0 and 1
    return x
              
def normalize_between_minus_one_and_one(x):
    x = 2*(normalize(x) - 0.5)
    return x

def roll_signal(df, field, only_mean=False, twice=False, normalize=False, user_col='user_id'):
    cols = list(df.columns)
    df['rolled_' + field] = df.groupby(user_col)[field].transform(lambda x: x.rolling(8, min_periods=1).mean().shift(-4))
    df[field + '_std'] = df.groupby(user_col)[field].transform(lambda x: x.rolling(8, min_periods=1).std().shift(-4))
    if twice:
        df['rolled_' + field] = df.groupby(user_col)['rolled_' + field].transform(lambda x: x.rolling(8, min_periods=1).mean().shift(-4))
    
    if normalize:
        df['scale'] = df.groupby(user_col)['rolled_' + field].transform(lambda x: x.max() - x.min())
        df[field + '_std'] = df[field + '_std']/df.scale
        df['rolled_' + field] = df.groupby(user_col)['rolled_' + field].transform(normalize)
    
    df['rolled_' + field + '_minus'] = df['rolled_' + field] - df[field + '_std']/2
    df['rolled_' + field + '_plus'] = df['rolled_' + field] + df[field + '_std']/2
    if only_mean:
        df = df[cols + ['rolled_' + field]]
    return df