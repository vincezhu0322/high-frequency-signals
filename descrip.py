from hft_signal_maker.hft_pipeline import HftPipeline


def high_frequency_description(cxt):
    trans = cxt.get_trans().reset_index()
    preprice = trans.groupby('code').price.shift(1).reset_index(drop=True)
    r = ((trans.price - preprice) / trans.price).fillna(0) * 100
    trans['return'] = r
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
    kurt = (r4 * N / r2 ** 2).fillna(0)
    downward_ratio = (ri * (N ** 0.5) / r2).fillna(0)
    res['skew'] = skew
    res['kurt'] = kurt
    res['downward_ratio'] = downward_ratio
    return res


pipeline = HftPipeline('trans', include_trans=True)
pipeline.add_block_step(high_frequency_description)
pipeline.gen_factors(["vola", "skew", "kurt", "downward_ratio"])
