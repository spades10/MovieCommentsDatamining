#-*- encoding:utf-8 -*-
from __future__ import print_function

import sys
try:
    import os, sys
    import importlib

    importlib.reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass

import codecs
from textrank4zh import Segmentation

seg = Segmentation.Segmentation()

# text = codecs.open('../../source_data/all_weibo.txt', 'r', 'utf-8', 'ignore').read()
# text = codecs.open('../../source_data/man_weibo.txt', 'r', 'utf-8', 'ignore').read()
text = codecs.open('../../source_data/woman_weibo.txt', 'r', 'utf-8', 'ignore').read()
# file = "../../result/result_weibo/fenci_all_weibo.txt"
# file = "../../result/result_weibo/fenci_man_weibo.txt"
file = "../../result/result_weibo/fenci_woman_weibo.txt"

# text = codecs.open('../../source_data/douban.txt', 'r', 'utf-8', 'ignore').read()
# file = "../../result/result_douban/fenci_douban.txt"

# text = codecs.open('../../source_data/news.txt', 'r', 'utf-8', 'ignore').read()
# file = "../../result/result_news/fenci_news.txt"

f = open(file, 'w', encoding='utf-8')
result = seg.segment(text=text, lower=True)
words = []

for ss in result.words_all_filters:
    for word in ss:
        words.append(word)

for ss in words:
    f.write(ss + ' ')
