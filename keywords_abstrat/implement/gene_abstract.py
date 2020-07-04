#-*- encoding:utf-8 -*-
from __future__ import print_function

try:
    import os, sys
    import importlib

    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Sentence


path = '../../result/result_news/sorted_news_50'
files = os.listdir(path)
f = open('../../result/result_news/sorted_sum_news_50.txt', 'w', encoding='utf-8')
for file in files:
    txt_path = '../../result/result_news/sorted_news_50/' + file
    contents = open(txt_path, 'r', encoding='utf-8',errors='ignore')
    for content in contents:
        content = content.strip('\n').strip('\r').strip('\r\n')
        f.write(content)
    f.write('\r')
f.close()

texts = codecs.open('../../result/result_news/sorted_sum_news_50.txt', 'r', 'utf-8').readlines()
titles = codecs.open('../../result/result_news/sorted_top_50.txt', 'r', 'utf-8').readlines()
file = "../../result/result_news/abstract_news.txt"

f = open(file, 'w', encoding='utf-8')
i = 0
for text in texts:
    tr4s = TextRank4Sentence()
    tr4s.analyze(text=text, lower=True, source = 'all_filters')

    for item in tr4s.get_key_sentences(num=1):
        f.write(titles[i].strip('\r').strip('\n').strip('\r\n') + '\r')
        f.write(item.sentence + '\r')
        print(item.weight, item.sentence, type(item.sentence))
    i += 1
    f.write('\r')