from __future__ import print_function

try:
    import os, sys
    import importlib

    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import TextRank4Keyword

# texts = codecs.open('../../source_data/all_weibo.txt', 'r', 'utf-8', 'ignore').readlines()
# texts = codecs.open('../../source_data/man_weibo.txt', 'r', 'utf-8', 'ignore').readlines()
texts = codecs.open('../../source_data/woman_weibo.txt', 'r', 'utf-8', 'ignore').readlines()
# file = "../../result/result_weibo/keywords_all_weibo.txt"
# file = "../../result/result_weibo/keywords_man_weibo.txt"
file = "../../result/result_weibo/keywords_woman_weibo.txt"

# texts = codecs.open('../../source_data/douban.txt', 'r', 'utf-8', 'ignore').readlines()
# file = "../../result/result_douban/keywords_douban.txt"

# texts = codecs.open('../../source_data/news.txt', 'r', 'utf-8', 'ignore').readlines()
# file = "../../result/result_news/keywords_news.txt"

f = open(file, 'w', encoding='utf-8')
for text in texts:
    tr4w = TextRank4Keyword()
    tr4w.analyze(text=text, lower=True, window=3, pagerank_config={'alpha': 0.85})

    for item in tr4w.get_keywords(3, word_min_len=2):  # for others
    # for item in tr4w.get_keywords(5, word_min_len=2):  # for news
        f.write(item.word + ' ')
        print(item.word, item.weight, type(item.word))
    f.write('\r')
