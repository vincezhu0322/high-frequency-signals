import cudf
from hft_signal_maker.hft_pipeline import HftPipeline


def op_ed_ratio(cxt):
    snap = cxt.get_snap(time_flag_freq='1min')
    ed = snap[(snap.time >= 143000000) & (snap.time <= 150000000)].groupby('code').cumvol
    ed_vol_ratio = (ed.max() - ed.min()) / snap.groupby('code').cumvol.max()
    op = snap[(snap.time >= 93000000) & (snap.time <= 100000000)].groupby('code')
    op_vol_ratio = (op.cumvol.max() - op.cumvol.min()) / snap.groupby('code').cumvol.max()
    op_net_bid_ratio = (op.totbid.nth(-1) - op.totbid.nth(0) + op.totoff.nth(0) - op.totoff.nth(-1)) / snap.groupby(
        'code').cumvol.max()
    res = cudf.DataFrame({'ed_vol_ratio': ed_vol_ratio, 'op_vol_ratio': op_vol_ratio,
                          'op_net_bid_ratio': op_net_bid_ratio}).reset_index()
    res['time_flag'] = '09:30-10:00, 14:30-15:00'
    return res


pipeline = HftPipeline('snap', include_snap=True)
pipeline.add_block_step(op_ed_ratio)
pipeline.gen_factors(["op_vol_ratio", "op_net_bid_ratio", "ed_vol_ratio"])
