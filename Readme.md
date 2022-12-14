# 高频因子列表

| 序号 | 因子名称 | 计算公式 | 出处 | 背后逻辑 | 因子频次 | 使用数据 | pipeline|factor|
|-- | ------------------ | -------------------------------- | -- | ------------- | ---- | ----| -----|----|
|1.| 改进ROE |不会| ①| 消除ROE的滞后性| 日频 |
|2.| 大单买入占比 | $`{\sum_{j=1}^N大买单成交额_{i,t-j}}\over{\sum_{j=1}^N成交额_{i,t-j}}`$ | ②| 捕捉大资金买入 | 1min | trans_with_order | big_order | big_bid_ratio|
|3.| 大单买入强度 | $`mean(大买单成交额_{i,t-j})\over{std(大买单成交额_{i,t-j})}`$ | ②| 捕捉大资金的买入强度 | 1min | trans_with_order | big_order | big_bid_tensity|
|4.| 大单净买入占比 | $`{\sum_{j=1}^N(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}\over{\sum_{j=1}^N成交额_{i,t-j}}`$ | ②| 捕捉大资金净买入 | 1min | trans_with_order | big_order | big_net_bid_rario|
|5.| 大单净买入强度 | $`{mean(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}\over{std(大买单成交额_{i,t-j}-大卖单成交额_{i,t-j})}`$ | ②| 捕捉大资金的净买入强度 | 1min | trans_with_order | big_order | big_net_bid_tensity|
|6.| 开盘大单买入占比 | $`{\sum_{j=1}^N大买单成交额_{i,t-j,9:30-10:00}}\over{\sum_{j=1}^N成交额_{i,t-j,9:30-10:00}}`$ | ②| 捕捉开盘半小时大资金的买入 | 日频 | trans_with_order|op_big_order|op_big_bid_ratio|
|7.| 开盘大单买入强度 | $`{mean(大买单成交额_{i,t-j,9:30-10:00})}\over{std(成交额_{i,t-j,9:30-10:00}})`$ | ②| 捕捉开盘半小时大资金的买入强度 | 日频 |trans_with_order|op_big_order|op_big_bid_tensity|
|8.| 开盘大单净买入占比 | $`{\sum_{j=1}^N(大买单成交额_{i,t-j,9:30-10:00}-大卖单成交额_{i,t-j,9:30-10:00})}\over{\sum_{j=1}^N成交额_{i,t-j,9:30~10:00}}`$ | ②| 捕捉开盘半小时大资金的净买入 | 日频 |trans_with_order|op_big_order|op_big_net_bid_ratio|
|9.| 开盘大单净买入强度 | $`{mean(大买单成交额_{i,t-j,9:30-10:00}-大卖单成交额_{i,t-j,9:30-10:00})}\over{std(成交额_{i,t-j,9:30-10:00}})`$ | ②| 捕捉开盘半小时大资金的净买入强度 | 日频 |trans_with_order|op_big_order|op_big_net_bid_tensity|
|10.| 高频方差 | $`\sqrt{{1\over{T}}\sum_{n=t}^{t-T+1}(\sum_{j=1}^Nr_{i,j,n}^2))}`$, T=选股周期, N=观测数, i,j,n代表第i只股票, 第j分钟和第n个交易日 | ③| 高阶矩和风险溢价的相关性 | 1min | trans| hft_descrip | vola|
|11.| 高频偏度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{{\sqrt{N}\sum_{j=1}^Nr_{i,j,n}^3}\over{(\sum_{j=1}^{N}r_{i,j,n}^2})^{1.5}}`$, 参数意义与前一个因子相同 | ③| 刻画日内快速拉升/下跌 | 1min | trans| hft_descrip|skew|
|12.| 高频峰度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{N\sum_{j=1}^Nr_{i,j,n}^4\over{{(\sum_{j=1}^{N}r_{i,j,n}^2})^2}}`$, 参数意义与前一个因子相同| ③| 刻画日内快速拉升/下跌 | 1min | trans|hft_descrip|kurt|
|13.| 上行波动 | $`\sum_{j=1}^Nr_{i,j,n}^2\cdot{I_{r>0}}`$ |⑦|上升的波动|1min|trans|
|14.| 下行波动 | $`\sum_{j=1}^Nr_{i,j,n}^2\cdot{I_{r<0}}`$ |⑦|下降的波动|1min|trans|
|15.| 下行波动占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sqrt{N}\sum_{j=1}^Nr_{i,j,n}^2\cdot{I_{r<0}}\over{\sum_{j=1}^Nr_{i,j,n}^2}}`$, 参数意义与前一个因子相同 |④| 下行风险大的股票具有更高的风险溢价 | 1min| trans|hft_descrip|downward_ratio|
|16.| 开盘成交占比 |$`{1\over{T}}\sum_{n=t}^{t-T+1}{Vol_{i,9:30-10:00,j}\over{Vol_{i,j,n}}}`$|④| 开盘知情交易者多 |日频| snap|op_ed_ratio|op_vol_ratio|
|17.| 尾盘成交占比 |$`{1\over{T}}\sum_{n=t}^{t-T+1}{Vol_{i,14:30-15:00,j}\over{Vol_{i,j,n}}}`$|④| 尾盘散户和游资多 |日频| snap|op_ed_ratio|ed_vol_ratio|
|18.| 开盘净委买增额占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}委买增加量_{i,j,n}-委卖增加量_{i,j,n}\over{成交量_{i,\cdot,n}}}`$ |④|开盘信息交易者多|日频| snap|op_ed_ratio|op_net_bid_ratio|
|19.|高频量价相关性|$`corr(v_{i,j,n},p_{i,j,n})`$|⑦|基本统计量|1min|trans|hft_descrip|hft_corr|
|20.| 改进量价 | $`{1\over{T}}\sum_{n=t}^{t-T+1}corr(Last_{i,j,n}, {Vol_{i,j,n}\over\sum_jVol_{i,j,n}})`$ |④| 量价背离 | 1min| trans |hft_descrip|adj_corr|
|21.| 改进反转 | $`\prod_{n=t}^{t-T+1}{Last_{i,j,n}\over{Last_{i,10:00,n}}}-1`$ |④| 剔除隔夜跳空影响的反转因子 | 1min| snap|reverse|reverse|
|22.| 平均单笔流出占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j=1}^NAmt_{i,j,n}\cdot{I_{r<0}}/\sum_{j=1}^NTrdNum_{i,j,n}\cdot{I_{r<0}}\over\sum_{j=1}^NAmt_{i,j,n}/\sum_{j=1}^NTrdNum_{i,j,n}}`$ |④| 捕捉大资金抄底行为 | 1min | snap|reverse|chaodi|
|23.| 大单推动涨幅 | $`\prod_{n=t}^{t-T+1}\prod(1+r_{i,j,n}\cdot{I_{j\in{IdxSet}}})-1`$, IdxSet=当日平均单笔成交金额最大的30%的K线的序号 |④| 多空博弈激烈，未来反转加强 | 日频| trans|big_trans|big_pull|
|24.| 开盘净主买占比 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n}\over\sum_{j\in{9:30-10:00}}成交额_{i,j,n}}`$ |④|刻画开盘主动买入|日频| trans|ti6_open_bid|op_bid_ratio|
|25.| 开盘净主买强度 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{mean_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n})\over{std_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}-主动卖出成交额_{i,j,n})}}`$|④|刻画开盘主动买入强度|日频| trans|ti6_open_bid|op_bid_tensity|
|26.|买入意愿|$`{\sum_{j\in{t}}(主动买入成交额_{i,j,n}+委买增加量_{i,j,n}-主动卖出成交额_{i,j,n}-委卖增加量_{i,j,n})\over\sum_{j\in{t}}成交额_{i,j,n}}`$|④|刻画买入意愿|1min|order, trans_with_order|buy_will|buy_will|
|27.| 开盘买入意愿 | $`{1\over{T}}\sum_{n=t}^{t-T+1}{\sum_{j\in{9:30-10:00}}(主动买入成交额_{i,j,n}+委买增加量_{i,j,n}-主动卖出成交额_{i,j,n}-委卖增加量_{i,j,n})\over\sum_{j\in{9:30-10:00}}成交额_{i,j,n}}`$|④|刻画开盘主动买入意愿|日频|order, trans_with_order|op_buy_will|op_buy_will|
|28.| 大单资金净流入率 | $`(\sum_{i=1}^{N}Amt_i\cdot{I_{r_i>0,i\in{IdxSet}}}-\sum_{i=1}^{N}Amt_i\cdot{I_{r_i<0,i\in{IdxSet}}})\over\sum_{i=1}^{N}Amt_i`$ |⑤| 同18|日频|trans|big_trans|big_net|
|29.| 买盘集中度 | $`\sum_{k=1}^{N_{i,t}}买单成交金额_{i,t,k}^2\over总成交金额_{i,t}^2`$ |⑥|刻画买盘强度|1min|trans|hft_descrip|bid_concentration|
|30.| 趋势 | $`close_t-close_{t-1}\over\sum_{j\in{t}}\vert{p_j-p_{j-1}}\vert`$|⑦|刻画股价的趋势强度|1min|trans|trend|trend|
|31.| Amihud非流动性 |$`\sum_{j\in{t}}{\vert{r_j}\vert\over{Amt_j}}`$|⑦|刻画流动性，流动性越低，股价越容易被交易行为影响|1min|trans|trend|amihud|
|32.|帕累托|$`V_{1\over4}\over{V_{3\over4}}`$|⑧|刻画委托量衰减速度|日频|order, trans_with_order|pareto|pareto|
|33.|信息分布均匀度|$`std(\sum_{j=1}^Nr_{i,j,n}^2)\over{mean(\sum_{j=1}^Nr_{i,j,n}^2)}`$|⑨|在EMH中，股价的波动完全等于信息流的波动|日频|trans|uid|uid|

① 海通证券选股因子系列研究（七十三）    
② 海通证券选股因子系列研究（七十二）    
③ Does Realized Skewness and Kurtosis Predict the
Cross-Section of Equity Returns?    
④ 海通证券选股因子系列研究（六十九）    
⑤ 海通证券选股因子系列研究（六十六）     
⑥ 海通证券选股因子系列研究（五十九）     
⑦ 20210712-多因子Alpha系列报告之（四十一）：高频价量数据的因子化方法-广发证券  
⑧ 20190426-“订单簿的温度”系列研究（二）：逐笔成交中的帕累托因子-东吴证券  
⑨ 20200901-“波动率选股因子”系列研究（二）：信息分布均匀度，基于高频波动率的选股因子-东吴证券