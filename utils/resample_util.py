import tushare as ts
import pandas as pd
from utils.time_util import get_first_date

def resampe_data_from_tick(tickers, date, freq):
    df_result = None
    for ticker in tickers:
        df_tick = ts.get_tick_data(ticker, date)
        df_tick = df_tick.set_index(['datetime'])
        df_temp = df_tick['price'].resample(freq).ohlc()
        df_temp['vol'] = df_tick['volume'].resample(freq).sum()
        df_temp['amount'] = df_tick['amount'].resample(freq).sum()
        df_temp['code'] = ticker
        if df_result is None:
            df_result = df_temp
        else:
            df_result = pd.concat([df_result, df_temp])
    df_result = df_result.reset_index()
    return df_result

ohlc_dict = {'open':'first','high':'max','low':'min','close':'last','vol':'sum','amount':'sum'}
def resample_freq(df_buffer, freq):
    df_freq = None
    for ticker, group in df_buffer.groupby(['code']):
        group = group.set_index(['datetime']).astype(float)
        df_temp = group.resample(freq, how=ohlc_dict, closed='right', label='right')
        df_temp['code'] = ticker
        if df_freq is None:
            df_freq = df_temp
        else:
            df_freq = pd.concat([df_freq, df_temp])
    df_freq = df_freq.dropna().reset_index()
    return df_freq[['code','datetime','open','high','low','close','vol','amount']]

def resample_live_data(raw_data_d, tickers, freq='w'):
    df_result = pd.DataFrame()
    raw_data_d = raw_data_d.set_index(['code', 'datetime'])
    if freq == 'w':
        first_date = get_first_date(freq='w')
    else:
        first_date = get_first_date(freq='m')
        
    for ticker in tickers:
        data = raw_data_d.loc[ticker]
        pre_close = data['close'].iloc[-len(data.loc[first_date:])-1]
        data = data.loc[first_date:]
        item_dict = {}
        item_dict['code'] = ticker
        item_dict['datetime'] = data.index[-1]
        item_dict['open'] = data['open'].iloc[0]
        item_dict['close'] = data['close'].iloc[-1]
        item_dict['high'] = data['high'].max()
        item_dict['low'] = data['low'].min()
        item_dict['vol'] = data['vol'].sum()
        item_dict['amount'] = data['amount'].sum()
        item_dict['p_change'] = item_dict['close']/pre_close*100-100
        df_result = df_result.append(pd.Series(item_dict), ignore_index=True)
    return df_result[['code', 'datetime','open','close','high','low','vol','amount','p_change']]