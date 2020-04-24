import tushare as ts
import pandas as pd
from data.market import history_data

def get_num_per_day(freq='d'):
    if freq == 'd':
        num_per_day = 1
    elif freq == '15min':
        num_per_day = 16
    elif freq == '30min':
        num_per_day = 8
    elif freq == '60min':
        num_per_day = 4
    elif freq == '120min':
        num_per_day = 2
    return num_per_day

def get_hs300_last_date_online(freq='d'):
    conn = ts.get_apis()
    benchmark = ts.bar('000300', conn=conn, asset='INDEX', freq=freq)
    ts.close_apis(conn)
    if benchmark is None:
        return None, None
    last_date0 = benchmark.index[0].strftime('%Y-%m-%d')
    last_date1 = benchmark.index[1].strftime('%Y-%m-%d')
    return last_date0, last_date1

def get_hs300_last_date_offline(freq='d'):
    data = history_data(['000300'], freq=freq)
    if data is None or data.empty:
        return None
    return data['datetime'].max().strftime('%Y-%m-%d')

def append_live_data(raw_data, live_data):
    if 'code' not in raw_data.columns:
        raw_data = raw_data.reset_index()
    cur_date = live_data['datetime'].iloc[-1].strftime('%Y-%m-%d')
    raw_data = raw_data[raw_data['datetime']<cur_date]
    raw_data = raw_data.append(live_data, ignore_index=True)
    return raw_data[['code', 'datetime','open','close','high','low','vol','amount','p_change']]

def get_raise_up_times(raw_data, threshold=9.5, seq_len=120, times=1):
    if 'code' in raw_data.columns:
        raw_data = raw_data.set_index(['code', 'datetime'])
    times_list = []
    ticker_list = []
    for ticker in raw_data.index.levels[0]:
        data = raw_data.loc[ticker].iloc[-seq_len:]
        ticker_list.append(ticker)
        times_list.append(sum(data['p_change']>threshold))
    df_result = pd.DataFrame(times_list, index=ticker_list, columns=['times'])
    df_result = df_result[df_result['times']>=times].sort_values(by=['times'], ascending=False)
    return df_result

def get_inverse_points(raw_data, n, m, a, b):
    if 'code' in raw_data.columns:
        raw_data = raw_data.set_index(['code'])
    times_list = []
    ticker_list = []
    for ticker in raw_data.index.levels[0]:
        data = raw_data.loc[ticker]
        close_t = data['cose']
        close_tn = data['cose'].shift(-n)
        close_tm = data['cose'].shift(m)
        part1 = (close_tn - close_t)/close_t*100
        part2 = (close_tm - close_t)/close_t*100
        points = data[part1>=a & part1>=b]['datetime']
        
