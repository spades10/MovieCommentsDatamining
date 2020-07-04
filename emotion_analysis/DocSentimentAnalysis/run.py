import os, sys
import importlib
importlib.reload(sys)
from 情感分析.DocSentimentAnalysis.DocSentimentAnalysis2 import *

# f = open('../../source_data/all_weibo.txt', 'r', encoding='utf-8')
# f = open('../../source_data/man_weibo.txt', 'r', encoding='utf-8')
# f = open('../../source_data/woman_weibo.txt', 'r', encoding='utf-8')

# f = open('../../source_data/douban.txt', 'r', encoding='utf-8')

f = open('../../source_data/news.txt', 'r', encoding='utf-8')


# f1 = open('../../result/result_weibo/sentiment_analysis_result/senti_pyltp_weibo_all.txt', 'w', encoding='utf-8')
# f1 = open('../../result/result_weibo/sentiment_analysis_result/senti_pyltp_weibo_man.txt', 'w', encoding='utf-8')
# f1 = open('../../result/result_weibo/sentiment_analysis_result/senti_pyltp_weibo_woman.txt', 'w', encoding='utf-8')

# f1 = open('../../result/result_douban/sentiment_analysis_result/senti_pyltp_douban.txt', 'w', encoding='utf-8')

f1 = open('../../result/result_news/sentiment_analysis_result/senti_pyltp_news.txt', 'w', encoding='utf-8')

lines = f.readlines()
handler = Sentimentor()
doc_sentiment_score = handler.doc_sentiment_score(lines)
length = len(doc_sentiment_score)
print(length)
print(doc_sentiment_score)
count_pos = 0
count_neg = 0
for score in doc_sentiment_score:
    if score > 0:
        count_pos += 1
    if score < 0:
        count_neg += 1
    f1.write(str(score) + '\r')
pos = (count_pos * 1.0 / length)*100
neg = (count_neg * 1.0 / length)*100
f1.write('支持人数为：' + str(count_pos) + '\r')
f1.write('反对人数为：' + str(count_neg) + '\r')
f1.write('总人数为：' + str(length) + '\r')
f1.write('支持率为：' + str(pos) + '%\r')
f1.write('反对率为：' + str(neg) + '%\r')
print(count_pos)
print(count_neg)



