import csv
from collections import Counter
from itertools import groupby
from operator import itemgetter
import datetime
from functools import cmp_to_key

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


with open(data_dir + '/' + data_name_3 + '.csv', 'r', encoding='UTF-8') as f:
    file_list = csv.reader(f)
    headers = next(file_list)
    for line in file_list:
        lines.append(line)

lines = list(filter(lambda x: x[11] == 'N', lines))
lines = select_col(lines, target_cols)
count_kinds = Counter(list(map(lambda x: x[2], lines)))
lines = list(filter(lambda x: count_kinds[x[2]] >= accept_threshold, lines))
groups = groupby(sorted(lines, key=itemgetter(2)), key=lambda x: x[2])
res = []
for key, group in groups:
    res.extend(sorted(list(group), key=cmp_to_key(cmp_datetime)))
    # print(key, len(list(group)))
# print(res)
# print(count_kinds)
#
with open(target_dir + '/' + data_name_3 + '.csv', 'w', encoding='UTF-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(*select_col([headers], target_cols))
    writer.writerows(res)

# csv.unregister_dialect('tab_dialect')

print('Done')
