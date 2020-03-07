from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.vader import SentiText
from main import target_dir
from main import data_name_1
from main import data_name_2
from main import data_name_3
import csv

corpus = []

def nltk_sentiment(sentences):
    sid = SentimentIntensityAnalyzer()
    for sen in sentences:
        print(sen)
        senti = sid.polarity_scores(sen)
        for k in senti:
            print('{0}:{1},'.format(k, senti[k]), end='\n')



with open(target_dir + '/' + data_name_1 + '.csv', 'r', encoding='UTF-8') as f:
    file_list = csv.reader(f)
    headers = next(file_list)
    for line in file_list:
        corpus.append(line[-2])

vectorizer = CountVectorizer()  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
X = vectorizer.fit_transform(corpus)  # 将文本转为词频矩阵
tf_idf = transformer.fit_transform(X)  # 计算tf-idf，
word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
weight = tf_idf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

nltk_sentiment(corpus)

# with open(target_dir + '/' + data_name_1 + '.txt', 'w', encoding='UTF-8') as f:
#     for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重
#         # print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
#         # for j in range(len(word)):
#         f.write(' '.join(list(map(lambda x: str(x), filter(lambda x: x[1] > 0.1, list(
#             zip(word, list(map(lambda x: round(x, 3), weight[i])))))))))
#         f.write('\n')

print('Done')
