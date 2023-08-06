import json
import os
import numpy as np

def make_dirs(path):
    '''
    创建文件夹，
    :param path:
    :return:
    '''
    if os.path.isdir(path) and os.path.exists(path) is False:
        os.makedirs(path)

def compute_cv(data:[])->int:
    # 计算变异系数 = =标准差/均值
    print(data)
    data2 = np.array(data)
    print(f"max:{np.max(data2)},min:{np.min(data2)}")
    return round(np.std(data2)/np.average(data2),4)

def compute_ratio_cv(results):
    '''

    :param results:[{"lhRatio":0.1},{}]
    :return:
    '''
    data = []
    for i in results:
        data.append(i['lhRatio'])
    return compute_cv(data)