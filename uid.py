import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_uid(cxt):
    trans = cxt.get_trans(calculate_delta=True)
    trans['rsqr'] = (trans['return'] * 100) ** 2
    r2 = trans.groupby(['ds', 'code', 'time_flag']).rsqr.sum().reset_index()
    res = (r2.groupby(['code']).rsqr.std() / r2.groupby(['code']).rsqr.mean()).reset_index()
    res.columns = ['code', 'uid']
    res['time_flag'] = 'daily'
    return res


pipeline = HftPipeline('trans', include_trans=True)
pipeline.add_block_step(get_uid)
pipeline.gen_factors(["uid"])
