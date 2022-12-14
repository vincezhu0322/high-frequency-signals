import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def high_frequency_description(cxt):
    trans = cxt.get_trans(time_flag_freq='5min').reset_index()
    r = trans['return']
    trans['rsqr'] = r ** 2
    trans['rcube'] = r ** 3
    trans['rquar'] = r ** 4
    trans['indic'] = 0
    trans.loc[trans['return'] < 0, 'indic'] = 1
    trans['rsqr_nega'] = trans.rsqr * trans.indic
    res = trans.groupby(['ds', 'code', 'time_flag']).rsqr.sum().sort_index().reset_index()
    res.columns = ['ds', 'code', 'time_flag', 'vola']
    N = trans.groupby(['ds', 'code', 'time_flag']).rsqr.count().sort_index().reset_index(drop=True)
    r2 = trans.groupby(['ds', 'code', 'time_flag']).rsqr.sum().sort_index().reset_index(drop=True)
    r3 = trans.groupby(['ds', 'code', 'time_flag']).rcube.sum().sort_index().reset_index(drop=True)
    r4 = trans.groupby(['ds', 'code', 'time_flag']).rquar.sum().sort_index().reset_index(drop=True)
    ri = trans.groupby(['ds', 'code', 'time_flag']).rsqr_nega.sum().sort_index().reset_index(drop=True)
    skew = (r3 * (N ** 0.5) / r2 ** 1.5).fillna(0)
    kurt = (r4 * (N) / r2 ** 2).fillna(0)
    downward_ratio = (ri * (N ** 0.5) / r2).fillna(0)
    res['skew'] = skew
    res['kurt'] = kurt
    res['downward_ratio'] = downward_ratio
    volsum = trans.groupby(['code', 'time_flag']).volume.sum().reset_index().rename(columns={'volume': 'vol_sum'})
    trans = trans.merge(volsum, on=['code', 'time_flag'], how='left').sort_values(['ds', 'code', 'time_flag'])
    trans['vol_ratio'] = trans.volume / trans.vol_sum
    v1 = trans.groupby(['code', 'time_flag']).price.var().sort_index()
    v2 = trans.groupby(['code', 'time_flag']).vol_ratio.var().sort_index()
    v3 = trans.groupby(['code', 'time_flag']).volume.var().sort_index()
    n = trans.groupby(['code', 'time_flag']).vol_ratio.count().sort_index()
    m1 = trans.groupby(['code', 'time_flag']).price.mean().sort_index()
    m2 = trans.groupby(['code', 'time_flag']).vol_ratio.mean().sort_index()
    m4 = trans.groupby(['code', 'time_flag']).volume.mean().sort_index()
    trans['pxvr'] = trans.price * trans.vol_ratio
    trans['pxv'] = trans.price * trans.volume
    m3 = trans.groupby(['code', 'time_flag']).pxvr.mean().sort_index()
    m5 = trans.groupby(['code', 'time_flag']).pxv.mean().sort_index()
    cor = ((n / (n - 1)) * (m3 - m1 * m2) / (v1 * v2) ** 0.5).fillna(0).sort_index()
    cor = cor.reset_index().rename(columns={0: 'adj_corr'})
    cor[(cor.adj_corr > 1) | (cor.adj_corr < -1)] = 0
    cor2 = ((n / (n - 1)) * (m5 - m1 * m4) / (v1 * v3) ** 0.5).fillna(0).sort_index()
    cor2 = cor2.reset_index().rename(columns={0: 'hft_corr'})
    cor2[(cor2.hft_corr > 1) | (cor2.hft_corr < -1)] = 0
    res = res.merge(cor, on=['code', 'time_flag'], how='left')
    res = res.merge(cor2, on=['code', 'time_flag'], how='left')
    trans['anchor'] = 0
    trans.loc[trans['bs_flag'] == 1, 'anchor'] = 1
    trans['amount'] = trans.price * trans.volume
    trans['bid_sqr'] = (trans.amount * trans.anchor) ** 2
    trans['amount_sqr'] = trans.amount ** 2
    bid = (trans.groupby(['code', 'time_flag']).bid_sqr.sum() / trans.groupby(
        ['code', 'time_flag']).amount_sqr.sum()).reset_index()
    bid.columns = ['code', 'time_flag', 'bid_concentration']
    res = res.merge(bid, on=['code', 'time_flag'], how='left')
    return res


pipeline = HftPipeline('hft_descrip', include_trans=True)
pipeline.add_block_step(high_frequency_description)
pipeline.gen_factors(["vola", "skew", "kurt", "hft_corr", "adj_corr", "downward_ratio", "bid_concentration"])

if __name__ == '__main__':
    import cupy

    cupy.cuda.Device(5).use()
    res = pipeline.compute('20210322', '20210322', universe='ALL', n_blocks=8)
    print(res)
