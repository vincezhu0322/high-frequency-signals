import sys

sys.path.append('/mnt/lustre/app/qllib')

from hft_signal_maker.hft_pipeline import HftPipeline


def get_pareto(cxt):
    order = cxt.get_order()
    pareto = order.groupby('code').volume.quantile(0.25) / order.groupby('code').volume.quantile(0.75)
    res = pareto.reset_index().rename(columns={'volume': 'pareto'})
    res['time_flag'] = '150000'
    return res


pipeline = HftPipeline('pareto', include_order=True)
pipeline.add_block_step(get_pareto)
pipeline.gen_factors(["pareto"])

if __name__ == '__main__':
    res = pipeline.compute(start_ds='20210630', end_ds='20210630', universe='ALL', n_blocks=1).reset_index()
    print(res)
