import sys
import cudf

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_pareto(cxt):
    order = cxt.get_order()
    trander = cxt.get_trans_with_order()
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
    order = cudf.concat([order[['code', 'order_id', 'volume']], trander[['code', 'bid_id', 'real_bid_volume']].rename(
        columns={'bid_id': 'order_id', 'real_bid_volume': 'volume'}),
                         trander[['code', 'ask_id', 'real_ask_volume']].rename(
                             columns={'ask_id': 'order_id', 'real_ask_volume': 'volume'})])
    order = order.sort_values(['code', 'order_id', 'volume'])
    order = order[order.volume != 0].drop_duplicates(subset=['code', 'order_id'], keep='last')
    pareto = order.groupby('code').volume.quantile(0.25) / order.groupby('code').volume.quantile(0.75)
    res = pareto.reset_index().rename(columns={'volume': 'pareto'})
    res['time_flag'] = 150000
    return res


pipeline = HftPipeline('pareto', include_order=True, include_trans_with_order=True)
pipeline.add_block_step(get_pareto)
pipeline.gen_factors(["pareto"])


if __name__ == '__main__':
    res = pipeline.compute(start_ds='20210630', end_ds='20210630', universe=['603501.SH', '600268.SH', '002667.SZ'], n_blocks=1).reset_index()
    print(res)
