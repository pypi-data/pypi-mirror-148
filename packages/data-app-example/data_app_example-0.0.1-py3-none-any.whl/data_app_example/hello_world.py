"""
分段表计算函数
    seq_segtabl: 计算序列分段表
    df_segtable: 计算DataFrame分段表
    db_segtable: 计算数据库汇总表的分段表
    ...
"""

from collections import Counter
from itertools import accumulate
import numpy as np
import pandas as pd


def seq_segtable(data, max_=None, min_=None, seg: int = 1):
    """
    计算序列data中各个数值在max_-1和min_之间的分段计数，以及大于max_计数和小于min_计数
    分段表由分段区间统计元组组成，每个元组的结构为：
        (区间最大值，区间最小值，区间计数，区间累计计数，区间累计比例）
    分段表的分段区间为：
        [max_-1, max_-seg], ..., [max_-n*segs, min_]
        [max_, max_]， [min_-1, min-1]
    每个分段区间统计数据为：
        segcount: 本区间计数
        segaccum: 至本区间的计数累计
        segratio: 至本区间的比例累计（seg_accum与分段区间计数总和之比，计数总和不包括[max_-1, min_]范围之外的数据）
    区间[max_, max_]的统计数据为：
        segcount: 大于等于max_的计数
        segaccum: -1
        segratio: -1
    区间[min_, min_]的统计数据为：
        segcount: 小于min_的计数
        segaccum: -1
        segratio: -1

    :param data: collections.abc.Sequence：输入数据序列，可以为元组、列表、一维数组等。
    :param max_: int：限定分段最大值.如果设置为None（缺省），取实际数据的最大值+1.
    :param min_: int：限定分段最小值。如果设置为None（缺省），取实际数据的最小值。
    :param seg: int： 分段长度

    :return: tuple(tuple((区间最大值: int, 区间最小值：int, 本区间人数: int, 累计人数: int, 累计比例: float),...),
                   最大值以上人数：int, 最小值以下人数：int)
            输出结果为：
            (分段表，最大值以上计数，最小值以下计数）：
            (
                (
                (seg1max，seg1min, seg1count, seg1accumulate, seg1ratio),
                ...
                (segnmax，segnmin, segncount, segnaccumulate, segnratio)
                ),
                seg_above_include_max_count,
                seg_below_not_include_min_count
            )

    >>> seq_segtable([1, 2, 2, 1, 3, 8], 5, 2, 1)
    ((4, 4, 0, 0, 0.0), (3, 3, 1, 1, 0.3333333333333333), (2, 2, 2, 3, 1.0), (5, 5, 1, -1, -1), (1, 1, 2, -1, -1))
    >>> seq_segtable(data=[1, 5, 3, 2, 6], max_=5, min_=2, seg=2)
    ((4, 3, 1, 1, 0.5), (2, 2, 1, 2, 1.0), (5, 5, 2, -1, -1), (1, 1, 1, -1, -1))
    """

    # 如果没有设置最大最小分段值，使用数据中的最大最小值
    max_ = max(data)+1 if max_ is None else max_
    min_ = min(data) if min_ is None else min_

    # 计算1值段人数，超出最大值(包括max_)和最小值之外单独保存为max_sum和min_sum
    counter = Counter(data)
    table_one = [(each_seg, counter.get(each_seg, 0)) for each_seg in range(max_, min_-1, -1)]
    max_lg_sum = sum([counter.get(_seg, 0) for _seg in counter.keys() if _seg >= max_] + [0])
    min_ls_sum = sum([counter.get(_seg, 0) for _seg in counter.keys() if _seg < min_] + [0])

    # 从高到低计算各个分段区间，最大值max_不作为第一个区间
    # segs = [(segmax, segmin if segmin >= min_ else min_)
    #         for segmax, segmin in zip(range(max_-1, min_, -seg), range(max_-seg, min_-seg-1, -seg))
    #         if segmax >= min_]
    seg_sections = []
    for segmax, segmin in zip(range(max_-1, min_-seg-1, -seg),
                              range(max_-seg, min_-seg-1, -seg)):
        if segmax <= min_ or segmin <= min_:
            seg_sections += [(segmax if segmax > min_ else min_,
                      segmin if segmin > min_ else min_)]
            break
        seg_sections += [(segmax, segmin)]

    # 计算各分段区间内人数
    count_list = [sum(x for _seg, x in table_one if segmin <= _seg <= segmax)
                 for segmax, segmin in seg_sections]

    # 计算累计人数和累计比例
    _sum = sum(count_list)
    accum_list = list(accumulate(count_list))
    ratio_list = [x/_sum for x in accum_list]
    segmax_list = [x[0] for x in seg_sections]
    segmin_list = [x[1] for x in seg_sections]
    table_out = tuple(zip(segmax_list, segmin_list, count_list, accum_list, ratio_list))

    # 加入区间[max_, max_]与[min_-1, min_-1]的统计数据：
    table_out += ((np.PINF, max_, max_lg_sum, -1, -1), (min_-1, np.NINF, min_ls_sum, -1, -1))

    return table_out


def df_segtable(df, cols, max_=None, min_=None, seg=1):
    """
    计算DataFrame中指定列的分段表

    Args:
        df: DataFrame: input data
        cols: list of columns name: columns to calculate segtable
        max_: int: max score value
        min_: int: min score value
        seg: length of a score segment
    Return:
        DataFrame: segtable
            seg
            <column1>_count
            <column1>_accum
            <column1>_ratio
            ...

    >>> df1 = pd.DataFrame({'score': [1, 5, 3, 2, 1]})
    >>> df_segtable(df1, cols=['score'], max_=5, min_=2, seg=1)
       segmax  segmin  score_count  score_accum  score_ratio
    0     4.0     4.0            0            0          0.0
    1     3.0     3.0            1            1          0.5
    2     2.0     2.0            1            2          1.0
    3     inf     5.0            1           -1         -1.0
    4     1.0    -inf            2           -1         -1.0

    >>> df2 = pd.DataFrame({'score': [1, 5, 3, 2, 1], 'score2': [1, 5, 4, 1, 7]})
    >>> df_segtable(df2, cols=['score', 'score2'])
       segmax  segmin  score_count  ...  score2_count  score2_accum  score2_ratio
    0     5.0     5.0            1  ...             1             1          0.25
    1     4.0     4.0            0  ...             1             2          0.50
    2     3.0     3.0            1  ...             0             2          0.50
    3     2.0     2.0            1  ...             0             2          0.50
    4     1.0     1.0            2  ...             2             4          1.00
    5     inf     6.0            0  ...             1            -1         -1.00
    6     0.0    -inf            0  ...             0            -1         -1.00
    <BLANKLINE>
    [7 rows x 8 columns]

    >>> df_segtable(df2, cols=['score', 'score2'], max_=6, min_=2, seg=2)
       segmax  segmin  score_count  ...  score2_count  score2_accum  score2_ratio
    0     5.0     4.0            1  ...             2             2           1.0
    1     3.0     2.0            2  ...             0             2           1.0
    2     inf     6.0            0  ...             1            -1          -1.0
    3     1.0    -inf            2  ...             2            -1          -1.0
    <BLANKLINE>
    [4 rows x 8 columns]
    """

    # 使用max_/min_缺省值时，各列使用以第一个列的分段区间为基准
    if max_ is None:
        max_ = max(df[cols[0]]) + 1
    if min_ is None:
        min_ = min(df[cols[0]])

    dfout = None
    for col in cols:
        # 逐列计算分段表，转换为DataFrame
        seq_segtable_result = seq_segtable(df[col].values, max_, min_, seg)
        dfcol = pd.DataFrame(
            data=seq_segtable_result,
            columns=['segmax', 'segmin', col+'_count', col+'_accum', col+'_ratio']
        )
        # 合并多个列分段计算结果
        if dfout is None:
            dfout = dfcol
        else:
            concat_cols = [col+'_count', col+'_accum', col+'_ratio']
            dfout = pd.concat([dfout, dfcol[concat_cols]], axis=1)

    return dfout


def db_segtable(conn, table, cols, max_, min_, seg):
    """
    calculate segtable from a table in database

    :param conn: connection to database
    :param table: table in database
    :param cols:
    :param max_:
    :param min_:
    :param seg:
    :return:
    """


def demo():
    data = [1, 2, 3, 6, 7]
    print(data)
    print("seq_segtable(data, 5, 2, 1)")
    print(seq_segtable(data, 5, 2, 1))
    print("db_segtable(pd.DataFrame(data, columns=['score']), cols=['score'], 5, 2, 2)")
    dfseg = df_segtable(pd.DataFrame(data, columns=['score']), cols=['score'], max_=5, min_=2, seg=2)
    print(dfseg)
    return dfseg
if __name__ == '__main__':  
    demo()  
