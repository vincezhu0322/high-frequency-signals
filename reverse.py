import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def reverse(cxt):
    snap = cxt.get_snap(time_flag_freq='1min')
    snap = snap[(snap.time >= 92500000) & (snap.time <= 150300000)]
    snap = snap.sort_values(['code', 'time']).reset_index(drop=True)
    close10 = snap[snap.time <= 100000000].groupby(['code']).last.nth(-1).reset_index()
    close10.columns = ['code', 'close10']
    snap = snap.merge(close10, on='code', how='left')
    snap['reverse'] = snap.last / snap.close10 - 1
    snap = snap.sort_values(['code', 'time']).reset_index(drop=True)
    res = snap[['code', 'time_flag', 'reverse']].drop_duplicates(subset=['code', 'time_flag'], keep='last')
    prelast = snap.groupby('code').last.shift(1).reset_index(drop=True)
    snap['return'] = ((snap.last - prelast) / snap.last).fillna(0)
    snap['indic'] = 0
    snap.loc[snap['return'] < 0, 'indic'] = 1
    snap['preamount'] = snap.groupby('code').cumamount.shift(1).reset_index(drop=True)
    snap['pretrade'] = snap.groupby('code').cumtrade.shift(1).reset_index(drop=True)
    snap['nega_amount'] = (snap['cumamount'] - snap['preamount']) * snap.indic
    snap['nega_trade'] = (snap['cumtrade'] - snap['pretrade']) * snap.indic
    snap['amount'] = snap['cumamount'] - snap['preamount']
    snap['trade'] = snap['cumtrade'] - snap['pretrade']
    bottom = ((snap.groupby(['code', 'time_flag']).nega_amount.sum() / snap.groupby
    (['code', 'time_flag']).nega_trade.sum()) / (snap.groupby(['code', 'time_flag']).amount.sum() / snap.groupby
    (['code', 'time_flag']).trade.sum())).fillna(0).reset_index().rename(columns={0: 'chaodi'})
    res = res.merge(bottom, on=['code', 'time_flag'], how='left')
    return res


pipeline = HftPipeline('snap', include_snap=True)
pipeline.add_block_step(reverse)
pipeline.gen_factors(["reverse", "chaodi"])
