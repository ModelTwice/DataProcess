from main import data_name_1
from main import data_name_2
from main import data_name_3
from main import get_data
from main import cmp_datetime
import datetime
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from functools import cmp_to_key

data_name = data_name_1
lines = get_data(data_name)


def date_range(beginDate, endDate):
    beginDate = datetime.datetime.strptime(beginDate, '%m/%d/%Y').date()
    endDate = datetime.datetime.strptime(endDate, '%m/%d/%Y').date()
    dates = []
    dt = beginDate
    date = beginDate
    while date <= endDate:
        dates.append(date.strftime("%m/%d/%Y"))
        dt = dt + datetime.timedelta(1)
        date = dt
    return dates


def stand_date(date):
    date = datetime.datetime.strptime(date, '%m/%d/%Y').date()
    return date.strftime("%m/%d/%Y")


dates = sorted(list(map(lambda x: x[-1], lines)), key=cmp_to_key(cmp_datetime))
dates = list(map(stand_date, dates))
dr = date_range(dates[-1], dates[0])
date_counter = Counter(dates)
y = []
for d in dr:
    if d in date_counter.keys():
        # if d == '08/05/2010':
        #     y.append(20)
        # else:
        y.append(date_counter[d])
    else:
        y.append(0)
x = [datetime.datetime.strptime(d, '%m/%d/%Y').date() for d in dr]

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d/%Y'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())
# Plot
plt.plot(x, y)
plt.gcf().autofmt_xdate()
plt.title(data_name)
plt.show()
