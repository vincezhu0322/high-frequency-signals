# 高频因子列表

| 序号 | 因子名称 | 计算公式 | 出处 | 背后逻辑 | 因子频次 | 使用数据 |
|-- | ------------------ | -------------------------------- | -- | ------------- | ---- | ----|
|1.| 改进ROE |不会| ①| 消除ROE的滞后性| 日频 |
|2.| 大单买入占比 | $`{\sum_{j=1}^N大买单成交额_{i,t-j}}\over{\sum_{j=1}^N成交额_{i,t-j}}`$ | ②| 捕捉大资金买入 | 1min |
|3.| 大单买入强度 | $`mean(大买单成交额_{i,t-j})\over{std(大买单成交额_{i,t-j})}`$ | ②| 捕捉大资金的买入强度 | 1min |
|4.| 大单净买入占比 | $`{\sum_{j=1}^N(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}\over{\sum_{j=1}^N成交额_{i,t-j}}`$ | ②| 捕捉大资金净买入 | 1min |
|5.| 大单净买入强度 | $`{mean(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}\over{std(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}`$ | ②| 捕捉大资金的净买入强度 | 1min |
|6.| 开盘大单买入占比 | $`{\sum_{j=1}^N大买单成交额_{i,t-j,9:30-10:00}}\over{\sum_{j=1}^N成交额_{i,t-j,9:30-10:00}}`$ | ②| 捕捉开盘半小时大资金的买入 | 日频 |
|7.| 开盘大单买入强度 | $`{mean(大买单成交额_{i,t-j,9:30-10:00})}\over{std(成交额_{i,t-j,9:30-10:00}})`$ | ②| 捕捉开盘半小时大资金的买入强度 | 日频 |
|8.| 开盘大单净买入占比 | $`{\sum_{j=1}^N(大买单成交额_{i,t-j,9:30-10:00}-大卖单成交额_{i,t-j,9:30-10:00})}\over{\sum_{j=1}^N成交额_{i,t-j,9:30~10:00}}`$ | ②| 捕捉开盘半小时大资金的净买入 | 日频 |
|9.| 开盘大单净买入强度 | $`{mean(大买单成交额_{i,t-j,9:30-10:00}-大卖单成交额_{i,t-j,9:30-10:00})}\over{std(成交额_{i,t-j,9:30-10:00}})`$ | ②| 捕捉开盘半小时大资金的净买入强度 | 日频 |
|10.| 高频方差 | $`\sqrt{{1\over{T}}\sum_{n=t}^{t-T+1}(\sum_{j=1}^Nr_{i,j,n}^2))}`$, T=选股周期, N=观测数, i,j,n代表第i只股票, 第j分钟和第n个交易日 | ③| 高阶矩和风险溢价的相关性 | 1min | trans|
|11.| 高频偏度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{{\sqrt{N}\sum_{j=1}^Nr_{i,j,n}^3}\over{(\sum_{j=1}^{N}r_{i,j,n}^2})^{1.5}}`$, 参数意义与前一个因子相同 | ③| 刻画日内快速拉升/下跌 | 1min | trans|
|12.| 高频峰度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{N\sum_{j=1}^Nr_{i,j,n}^4\over{{(\sum_{j=1}^{N}r_{i,j,n}^2})^2}}`$, 参数意义与前一个因子相同| ③| 刻画日内快速拉升/下跌 | 1min | trans|
|13.| 下行波动占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sqrt{N}\sum_{j=1}^Nr_{i,j,n}^2\cdot{I_{r<0}}\over{\sum_{j=1}^Nr_{i,j,n}^2}}`$, 参数意义与前一个因子相同 |④| 下行风险大的股票具有更高的风险溢价 | 1min| trans|
|14.| 尾盘成交占比 |$`{1\over{T}}\sum_{n=t}^{t-T+1}{Vol_{i,14:30-15:00,j}\over{Vol_{i,j,n}}}`$|④| 尾盘散户和游资多 |日频| snap|
|15.| 开盘净委买增额占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}委买增加量_{i,j,n}-委卖增加量_{i,j,n}\over{成交量_{i,\cdot,n}}}`$ |④|开盘信息交易者多|日频| snap|
|16.| 高频量价相关性 | $`{1\over{T}}\sum_{n=t}^{t-T+1}corr(Last_{i,j,n}, {Vol_{i,j,n}\over\sum_jVol_{i,j,n}})`$ |④| 量价背离 | 1min| trans |
|17.| 改进反转 | $`\prod_{n=t}^{t-T+1}{Last_{i,j,n}\over{Last_{i,10:00,n}}}-1`$ |④| 剔除隔夜跳空影响的反转因子 | 1min| snap|
|18.| 平均单笔流出占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j=1}^NAmt_{i,j,n}\cdot{I_{r<0}}/\sum_{j=1}^NTrdNum_{i,j,n}\cdot{I_{r<0}}\over\sum_{j=1}^NAmt_{i,j,n}/\sum_{j=1}^NTrdNum_{i,j,n}}`$ |④| 捕捉大资金抄底行为 | 1min | snap|
|19.| 大单推动涨幅 | $`\prod_{n=t}^{t-T+1}\prod(1+r_{i,j,n}\cdot{I_{j\in{IdxSet}}})-1`$, IdxSet=当日平均单笔成交金额最大的30%的K线的序号 |④| 多空博弈激烈，未来反转加强 | 日频|
|20.| 开盘净主买占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n}\over\sum_{j\in{9:30-10:00}}成交额_{i,j,n}}`$ |④|刻画开盘主动买入|日频| trans|
|21.| 开盘净主买强度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{mean_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n})\over{std_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n})}}`$|④|刻画开盘主动买入强度|日频| trans|
|22.| 开盘买入意愿 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}+委买增加量_{i,j,n}-主动卖出成交额_{i,j,n}-委卖增加量_{i,j,n})\over\sum_{j\in{9:30-10:00}}成交额_{i,j,n}}`$|④|刻画开盘主动买入意愿|日频|

① 海通证券选股因子系列研究（七十三）    
② 海通证券选股因子系列研究（七十二）    
③ Does Realized Skewness and Kurtosis Predict the
Cross-Section of Equity Returns?    
④ 海通证券选股因子系列研究（六十九）