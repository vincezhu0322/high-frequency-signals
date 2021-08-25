import cudf
import sys
sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_op_buy_will(cxt):
    order = cxt.get_order(time_flag_freq='30min')
    order = order[order.time_flag == 100000]
    trander = cxt.get_trans_with_order(time_flag_freq='30min')
    trander = trander[trander.time_flag == 100000]
    trander['bid_volume'] = trander.bid_volume.fillna(0)
    trander['ask_volume'] = trander.ask_volume.fillna(0)
    bid_volume = (trander[(trander.bs_flag == 1) & ((trander.ask_type == 3) | (trander.ask_type == 4))].groupby(
        ['code', 'bid_id']).volume.sum() + trander.groupby(['code', 'bid_id']).bid_volume.max()).reset_index().rename(
        columns={0: 'real_bid_volume'})
    ask_volume = (trander[(trander.bs_flag == -1) & ((trander.bid_type == 3) | (trander.bid_type == 4))].groupby(
        ['code', 'ask_id']).volume.sum() + trander.groupby(['code', 'ask_id']).ask_volume.max()).reset_index().rename(
        columns={0: 'real_ask_volume'})
    trander = trander.merge(ask_volume, on=['code', 'ask_id'], how='outer')
    trander = trander.merge(bid_volume, on=['code', 'bid_id'], how='outer')
    trander['real_bid_volume'] = trander.real_bid_volume.fillna(trander.bid_volume)
    trander['real_ask_volume'] = trander.real_ask_volume.fillna(trander.ask_volume)
    bid_order = trander[['code', 'bid_id', 'real_bid_volume']].rename(
        columns={'bid_id': 'order_id', 'real_bid_volume': 'volume'})
    bid_order['bs_flag'] = 1
    ask_order = trander[['code', 'ask_id', 'real_ask_volume']].rename(
        columns={'ask_id': 'order_id', 'real_ask_volume': 'volume'})
    ask_order['bs_flag'] = -1
    order = cudf.concat([order[['code', 'order_id', 'bs_flag', 'volume']], bid_order, ask_order])
    order = order.sort_values(['code', 'order_id', 'volume'])
    order = order[order.volume != 0].drop_duplicates(subset=['code', 'order_id'], keep='last')
    bid_order = order[order.bs_flag == 1].groupby('code').volume.sum()
    ask_order = order[order.bs_flag == -1].groupby('code').volume.sum()
    order_temp = (bid_order - ask_order).fillna(0)
    trander = trander[trander.trans_type == 1]
    bid_trans = trander[trander.bs_flag == 1].groupby('code').volume.sum().sort_index()
    ask_trans = trander[trander.bs_flag == -1].groupby('code').volume.sum().sort_index()
    trans_temp = (bid_trans - ask_trans).fillna(0)
    vol_temp = trander.groupby('code').volume.sum().sort_index()
    res = ((trans_temp + order_temp)/vol_temp).fillna(0).reset_index().rename(columns={'index':'code','volume': 'op_buy_will'})
    res['time_flag'] = 100000
    return res


pipeline = HftPipeline('op_buy_will', include_order=True, include_trans_with_order=True)
pipeline.add_block_step(get_op_buy_will)
pipeline.gen_factors(['op_buy_will'])

if __name__ == '__main__':
    res = pipeline.compute(start_ds='20210322', end_ds='20210322', universe=['603501.SH','600268.SH','002667.SZ'], n_blocks=1)
    print(res)
