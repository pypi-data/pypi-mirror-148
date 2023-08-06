#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : minidata.
# @File         : demo
# @Time         : 2022/4/22 下午4:34
# @Author       : yuanjie
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  :


from meutils.pipe import *

df = pd.read_csv('../../words.txt', '\t', header=None)

print(df[0].to_frame('words'))
df[0].to_frame('w').to_feather('词库/敏感词.ft')
# df.to_feather('情感分析/携程酒店评论.ft')

# df = pd.read_csv('~/Desktop/task3_train.txt', '\t', names=['s1', 's2', 'label'])
#
# df = df.sort_values(['s1', 's2'], ignore_index=True)[['label', 's1', 's2']]
# print(df.head(20))
#
# df.s2 = df.s2.str.strip()
# df.s1 = df.s1.str.strip()
#
# NAME = '微众银行智能客服相似问'
# joblib.dump(df, NAME + '.pkl')
#
# print(joblib.load(NAME + '.pkl'))
#
#
# for p in Path('senteval_cn').glob('*'):
#     df: pd.DataFrame = joblib.load(p.name)
#
#     df.to_feather(p.stem+'.ft')

# pd.read_feather()
