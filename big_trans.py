import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def big_trans(cxt):
    trans = cxt.get_trans(time_flag_freq='5min').reset_index()
    preprice = trans.groupby('code').price.shift(1).reset_index(drop=True)
    trans['return'] = ((trans.price - preprice) / trans.price).fillna(0)
    trans['amount'] = trans.price * trans.volume
    thres = trans.groupby('code').amount.quantile(q=0.7).reset_index()
    thres.columns = ['code', 'threshold']
    trans = trans.merge(thres, on='code', how='left')
    trans['anchor'] = trans.amount - trans.threshold
    big = trans[trans.anchor >= 0].drop(columns=['anchor'])
    big['return'] += 1
    big['indic'] = 0
    big.loc[big['return'] < 1, 'indic'] = -1
    big.loc[big['return'] > 1, 'indic'] = 1
    big['net_amount'] = big.amount * big.indic
    res = big.groupby('code')['return'].prod().reset_index()
    res.columns = ['code', 'big_pull']
    net = (big.groupby('code').net_amount.sum() / trans.groupby('code').amount.sum()).reset_index()
    net.columns = ['code', 'big_net']
    res = res.merge(net, on='code', how='outer')
    res['time_flag'] = 'daily'
    return res


pipeline = HftPipeline('big_trans', include_trans=True)
pipeline.add_block_step(big_trans)
pipeline.gen_factors(["big_pull", "big_net"])

if __name__ == '__main__':
    res = pipeline.compute(start_ds='20210322', end_ds='20210322', universe='ALL', n_blocks=1)
    print(res)
