import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_trend(cxt):
    trans = cxt.get_trans(calculate_delta=True)
    trans['abs_delta_p'] = trans.delta_price.abs()
    sigma_diff = trans.groupby(['code', 'time_flag']).abs_delta_p.sum().reset_index()
    sigma_diff = sigma_diff.rename(columns={'abs_delta_p': 'sigma_diff'})
    close = trans[['code', 'time_flag', 'price']].drop_duplicates(subset=['code', 'time_flag'], keep='last')
    close.reset_index(drop=True, inplace=True)
    preprice = close.groupby('code').price.shift(1).reset_index(drop=True)
    close['change'] = (close.price - preprice).fillna(0)
    trend = sigma_diff.merge(close, on=['code', 'time_flag'], how='outer')
    trend['trend'] = trend.change / trend.sigma_diff
    trans['amount'] = trans.volume * trans.price
    trans['amihud'] = trans['return'].abs() / trans.amount * 100
    amihud = trans.groupby(['code', 'time_flag']).amihud.sum().reset_index()
    res = trend.merge(amihud, on=['code', 'time_flag'], how='outer')
    return res


pipeline = HftPipeline('trans', include_trans=True)
pipeline.add_block_step(get_trend)
pipeline.gen_factors(["trend", "amihud"])
