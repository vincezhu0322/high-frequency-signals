import sys
sys.path.append('/mnt/lustre/app/qllib')


import cudf
from hft_signal_maker.hft_pipeline import HftPipeline


def open_bid(cxt):
    trans = cxt.get_trans()
    trans = trans[(trans.time >= 93000000) & (trans.time <= 100000000) & (trans.trans_type == 1)]
    trans['amount'] = trans.price * trans.volume
    amount = trans.groupby(['code', 'bs_flag', 'time_flag']).amount.sum()
    amount = amount.reset_index()
    bsflag = cudf.DataFrame({'bs_flag': amount.bs_flag.unique(), 'anchor': 1})
    codes = cudf.DataFrame({'code': amount.code.unique(), 'anchor': 1})
    timeflag = cudf.DataFrame({'time_flag': amount.time_flag.unique(), 'anchor': 1})
    temp = codes.merge(timeflag, on=['anchor'], how='outer').sort_values(
        ['code', 'time_flag']).reset_index(drop=True)
    frame = temp.merge(bsflag, on=['anchor'], how='outer').drop(columns=['anchor']).sort_values(
        ['code', 'time_flag', 'bs_flag']).reset_index(drop=True)
    amount = frame.merge(amount, on=['code', 'time_flag', 'bs_flag'], how='left').sort_values(
        ['code', 'time_flag', 'bs_flag']).reset_index(
        drop=True)
    amount.fillna(0, inplace=True)
    amount.set_index(['code', 'time_flag'], inplace=True)
    diff = (amount[amount.bs_flag == 1].amount - amount[amount.bs_flag == -1].amount).reset_index()
    agg = (amount[amount.bs_flag == 1].amount + amount[amount.bs_flag == -1].amount).reset_index()
    ratio = (diff.groupby('code').amount.sum() / agg.groupby('code').amount.sum()).reset_index()
    ratio.columns = ['code', 'open_bid_ratio']
    tensity = (diff.groupby('code').amount.mean() / diff.groupby('code').amount.std()).reset_index()
    tensity.columns = ['code', 'open_bid_tensity']
    res = ratio.merge(tensity, on='code', how='left')
    res['time_flag'] = 100000
    return res.set_index(['code', 'time_flag'])


pipeline = HftPipeline('ti6_open_bid', include_trans=True)
pipeline.add_block_step(open_bid)
pipeline.gen_factors(["open_bid_ratio", "open_bid_tensity"])


if __name__ == '__main__':
    import cupy
    res = pipeline.compute('20210101', '20210104', universe='ALL', n_blocks=8)
    print(res)
    # pipeline.run('20210101', '20210301', universe='ALL', n_blocks=8, target_dir='/mnt/lustre/home/lgj/data')

