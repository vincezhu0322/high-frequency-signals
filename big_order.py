import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_trander(cxt):
    trander = cxt.get_trans_with_order(time_flag_freq='1min')
    trander = trander[trander.trans_type == 1]
    trander['amount'] = trander.price * trander.volume
    trander['bid_volume'] = trander.bid_volume.fillna(0)
    trander['ask_volume'] = trander.ask_volume.fillna(0)
    trander['bid_price'] = trander.bid_price.fillna(trander.price)
    trander['ask_price'] = trander.ask_price.fillna(trander.price)
    bid_volume = (trander[(trander.bs_flag == 1) & ((trander.trans_type == 3) | (trander.trans_type == 4))].groupby(
        ['code', 'bid_id']).volume.sum() + trander.groupby(['code', 'bid_id']).bid_volume.max()).reset_index().rename(
        columns={0: 'real_bid_volume'})
    ask_volume = (trander[(trander.bs_flag == -1) & ((trander.trans_type == 3) | (trander.trans_type == 4))].groupby(
        ['code', 'ask_id']).volume.sum() + trander.groupby(['code', 'ask_id']).ask_volume.max()).reset_index().rename(
        columns={0: 'real_ask_volume'})
    trander = trander.merge(ask_volume, on=['code', 'ask_id'], how='outer')
    trander = trander.merge(bid_volume, on=['code', 'bid_id'], how='outer')
    trander['real_bid_volume'] = trander.real_bid_volume.fillna(trander.bid_volume)
    trander['real_ask_volume'] = trander.real_ask_volume.fillna(trander.ask_volume)
    trander['big_bid'] = 0
    trander['big_ask'] = 0
    import numpy as np
    trander['log_bid_amount'] = np.log(trander.bid_price * trander.real_bid_volume)
    trander['log_ask_amount'] = np.log(trander.ask_price * trander.real_ask_volume)
    trander = trander[(trander.log_bid_amount > -99999) & (trander.log_ask_amount > -99999)]
    benchmark = (trander.groupby('code').log_bid_amount.std() + trander.groupby(
        'code').log_bid_amount.mean()).reset_index().rename(columns={'log_bid_amount': 'threshold'})
    benchmark['threshold'] = benchmark.threshold.map(lambda x: max(x, 12))
    trander = trander.merge(benchmark, on='code', how='left')
    trander.loc[trander.log_bid_amount > trander.threshold, 'big_bid'] = 1
    trander.loc[trander.log_ask_amount > trander.threshold, 'big_ask'] = 1
    trander['big_bid_amount'] = trander.big_bid * trander.amount
    trander['big_ask_amount'] = trander.big_ask * trander.amount
    trander['net_big_amount'] = trander.big_bid_amount - trander.big_ask_amount
    big_bid_ratio = (trander[trander.big_bid == 1].groupby(['code', 'time_flag']).amount.sum() / trander.groupby(
        ['code', 'time_flag']).amount.sum()).reset_index().rename(columns={'amount': 'big_bid_ratio'}).fillna(0)
    big_bid_tensity = (trander.groupby(['code', 'time_flag']).big_bid_amount.mean() / trander.groupby(
        ['code', 'time_flag']).big_bid_amount.std()).reset_index().rename(columns={'big_bid_amount': 'big_bid_tensity'}).fillna(
        0)
    res = big_bid_ratio.merge(big_bid_tensity, on=['code', 'time_flag'], how='outer').fillna(0)
    net_ratio = (trander.groupby(['code', 'time_flag']).net_big_amount.sum() / trander.groupby(
        ['code', 'time_flag']).amount.sum()).reset_index().rename(columns={0: 'big_net_bid_ratio'})
    net_tensity = (trander.groupby(['code', 'time_flag']).net_big_amount.mean() / trander.groupby(
        ['code', 'time_flag']).net_big_amount.std()).reset_index().rename(
        columns={'net_big_amount': 'big_net_bid_tensity'})
    net = net_ratio.merge(net_tensity, on=['code', 'time_flag'], how='outer').fillna(0)
    res = res.merge(net, on=['code', 'time_flag'], how='outer')
    return res


pipeline = HftPipeline('big_order', include_trans_with_order=True)
pipeline.add_block_step(get_trander)
pipeline.gen_factors(['big_bid_ratio', 'big_bid_tensity', 'big_net_bid_ratio', 'big_net_bid_tensity'])

if __name__ == '__main__':
    res = pipeline.compute(start_ds='20210322', end_ds='20210322', universe=['603501.SH', '600268.SH', '002667.SZ'],
                           n_blocks=8).reset_index()
