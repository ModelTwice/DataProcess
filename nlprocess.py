from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.corpus import stopwords
from nltk.sentiment.vader import SentiText
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from nltk import word_tokenize, pos_tag
from nltk.stem import WordNetLemmatizer
import nltk
from main import get_data
from main import target_dir
from main import data_name_1
from main import data_name_2
from main import data_name_3
import csv

corpus = list(map(lambda x: x[-2], get_data(data_name_2)))


def has_digit(text):
    return any(map(lambda x: '0' <= x <= '9', list(text)))


def get_wordnet_pos(tree_bank_tag):
    if tree_bank_tag.startswith('J'):
        return wordnet.ADJ
    elif tree_bank_tag.startswith('V'):
        return wordnet.VERB
    elif tree_bank_tag.startswith('N'):
        return wordnet.NOUN
    elif tree_bank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return None


def lemmatize_sentence(sentence):
    res = []
    lemmatizer = WordNetLemmatizer()
    for word, pos in pos_tag(word_tokenize(sentence)):
        if pos in ['JJ', 'JJR', 'JJS']:
            wordnet_pos = get_wordnet_pos(pos) or wordnet.NOUN
            res.append(lemmatizer.lemmatize(word, pos=wordnet_pos))
    return res


def nltk_sentiment(sentences):
    sid = SentimentIntensityAnalyzer()
    for sen in sentences:
        print(sen)
        senti = sid.polarity_scores(sen)
        for k in senti:
            print('{0}:{1},'.format(k, senti[k]), end='\n')


def nltk_tokenize(sentences):
    res = []
    for sen in sentences:
        token_list = nltk.word_tokenize(sen)
        token_list = list(filter(lambda x: x not in stopwords.words('english'), token_list))
        token_list = list(filter(lambda x: not has_digit(x), token_list))
        tt = nltk.pos_tag(token_list)
        # ftt = list(filter(lambda x: x[1] in ['JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS'], tt))
        ftt = list(filter(lambda x: x[1] in ['JJ'], tt))
        res.append(ftt)
    return res


def all_words(sentences):
    res = set()
    for sen in sentences:
        res.update(lemmatize_sentence(sen))
    return res


vectorizer = CountVectorizer(stop_words=stopwords.words('english'))  # 该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer = TfidfTransformer()  # 该类会统计每个词语的tf-idf权值
X = vectorizer.fit_transform(corpus)  # 将文本转为词频矩阵
tf_idf = transformer.fit_transform(X)  # 计算tf-idf，
word = vectorizer.get_feature_names()  # 获取词袋模型中的所有词语
weight = tf_idf.toarray()  # 将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

# ftt_list = nltk_tokenize(corpus)

all_j = set()
for sen in corpus:
    all_j.update(lemmatize_sentence(sen))
all_j = set(filter(lambda x: not has_digit(x), all_j))
print(all_j)

# with open(target_dir + '/' + data_name_3 + '_tagged_tokens.txt', 'w', encoding='UTF-8') as f:
#     for item in ftt_list:
#         f.write(str(item))
#         f.write('\n')

# for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重
#     print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
#     print(sorted(list(zip(word, weight[i])), key=lambda x: x[1], reverse=True)[:10])

# nltk_sentiment(corpus)

# with open(target_dir + '/' + data_name_1 + '.txt', 'w', encoding='UTF-8') as f:
#     for i in range(len(weight)):  # 打印每类文本的tf-idf词语权重
#         # print("-------这里输出第", i, u"类文本的词语tf-idf权重------")
#         # for j in range(len(word)):
#         f.write(' '.join(list(map(lambda x: str(x), filter(lambda x: x[1] > 0.1, list(
#             zip(word, list(map(lambda x: round(x, 3), weight[i])))))))))
#         f.write('\n')

print('Done')
