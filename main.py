import csv
from collections import Counter
from itertools import groupby
from operator import itemgetter
import datetime
from functools import cmp_to_key

import seaborn as sns
import numpy as np
from numpy.random import randn
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy import stats

# csv.register_dialect('tab_dialect', delimiter='\t', quoting=csv.QUOTE_ALL)

data_dir = './data'
data_name_1 = 'microwave'
data_name_2 = 'hair_dryer'
data_name_3 = 'pacifier'
target_dir = './a'

data_names = [data_name_1, data_name_2, data_name_3]
lines = []

target_cols = [1, 2, 4, 7, 8, 9, 10, 12, 13, 14]
accept_threshold = 10


def select_col(data, cols):
    res = []
    for item in data:
        res.append([item[i] for i in cols])
    return res


def cmp_datetime(a, b):
    a_datetime = datetime.datetime.strptime(a[-1], '%m/%d/%Y')
    b_datetime = datetime.datetime.strptime(b[-1], '%m/%d/%Y')

    if a_datetime > b_datetime:
        return -1
    elif a_datetime < b_datetime:
        return 1
    else:
        return 0


if __name__ == '__main__':
    data_name = data_name_2
    with open(data_dir + '/' + data_name + '.csv', 'r', encoding='UTF-8') as f:
        file_list = csv.reader(f)
        headers = next(file_list)
        for line in file_list:
            lines.append(line)

    lines = list(filter(lambda x: x[11] == 'Y' or x[11] == 'y', lines))
    lines = select_col(lines, target_cols)
    # print(len(lines))
    count_kinds = Counter(list(map(lambda x: x[2], lines)))
    ct_dist = Counter(count_kinds.values())
    # with open(target_dir + '/' + data_name + '_ct.txt', 'w', encoding='UTF-8') as f:
    #     f.write(str(count_kinds.most_common()))

    plt.hist(list(filter(lambda x: x > 1, list(count_kinds.values()))), bins=800, histtype="stepfilled")
    # plt.show()
    # sns.distplot(list(count_kinds.values()), bins=200, rug=False)
    plt.show()
    # s = 0
    # for key in count_kinds.keys():
    #     if count_kinds[key] >= 10:
    #         s += count_kinds[key]
    # print(s)
    # tc = []
    # for key, value in count_kinds:
    #     tc.append(tuple((key, value)))
    # print(sorted(tc, key=lambda x: x[1], reverse=True))
    lines = list(filter(lambda x: count_kinds[x[2]] >= accept_threshold, lines))
    groups = groupby(sorted(lines, key=itemgetter(2)), key=lambda x: x[2])
    res = []
    for key, group in groups:
        res.extend(sorted(list(group), key=cmp_to_key(cmp_datetime)))
        # print(key, len(list(group)))
    # print(res)
    # print(count_kinds)
    #
    # with open(target_dir + '/' + data_name + '.csv', 'w', encoding='UTF-8', newline='') as f:
    #     writer = csv.writer(f)
    #     writer.writerow(*select_col([headers], target_cols))
    #     writer.writerows(res)

    # csv.unregister_dialect('tab_dialect')

    print('Done')
