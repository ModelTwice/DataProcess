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
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentiText
import seaborn as sns

lines = get_data(data_name_1)
for i in range(len(lines)):
    if len(lines[i][-2].split()) > 1000:
        print(i)
        print(len(lines[i][-2].split()))

corpus = list(map(lambda x: x[-2], lines))
word_count = list(map(lambda x: len(x.split()), corpus))
word_count = list(filter(lambda x: x > 40, word_count))
# print(sorted(list(zip(range(1, len(word_count) + 1), word_count)), key=lambda x: x[1], reverse=True))
# print(sorted(word_count, reverse=True))
# plt.hist(word_count, bins=800, histtype="stepfilled")
# plt.show()
# sns.distplot(word_count, bins=200)
# plt.show()
