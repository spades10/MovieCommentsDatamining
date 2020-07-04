from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import jieba.posseg as pseg
import codecs
import os

from . import util

def get_default_stop_words_file():
    d = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(d, 'stopwords.txt')

class WordSegmentation(object):
    """ 分词 """
    
    def __init__(self, stop_words_file = None, allow_speech_tags = util.allow_speech_tags):
        
        allow_speech_tags = [util.as_text(item) for item in allow_speech_tags]

        self.default_speech_tag_filter = allow_speech_tags
        self.stop_words = set()
        self.stop_words_file = get_default_stop_words_file()
        if type(stop_words_file) is str:
            self.stop_words_file = stop_words_file
        for word in codecs.open(self.stop_words_file, 'r', 'utf-8', 'ignore'):
            self.stop_words.add(word.strip())
    
    def segment(self, text, lower = True, use_stop_words = True, use_speech_tags_filter = False):
        # 对一段文本进行分词，返回list类型的分词结果


        text = util.as_text(text)
        jieba_result = pseg.cut(text)
        
        if use_speech_tags_filter == True:
            jieba_result = [w for w in jieba_result if w.flag in self.default_speech_tag_filter]
        else:
            jieba_result = [w for w in jieba_result]

        # 去除特殊符号
        word_list = [w.word.strip() for w in jieba_result if w.flag!='x']
        word_list = [word for word in word_list if len(word)>0]
        
        if lower:
            word_list = [word.lower() for word in word_list]

        if use_stop_words:
            word_list = [word.strip() for word in word_list if word.strip() not in self.stop_words]

        return word_list
        
    def segment_sentences(self, sentences, lower=True, use_stop_words=True, use_speech_tags_filter=False):
        # 将列表sequences中的每个元素/句子转换为由单词构成的列表。
        
        res = []
        for sentence in sentences:
            res.append(self.segment(text=sentence, 
                                    lower=lower, 
                                    use_stop_words=use_stop_words, 
                                    use_speech_tags_filter=use_speech_tags_filter))
        return res
        
class SentenceSegmentation(object):#分句
    
    def __init__(self, delimiters=util.sentence_delimiters):
        self.delimiters = set([util.as_text(item) for item in delimiters])
    
    def segment(self, text):
        res = [util.as_text(text)]
        
        util.debug(res)
        util.debug(self.delimiters)

        for sep in self.delimiters:
            text, res = res, []
            for seq in text:
                res += seq.split(sep)
        res = [s.strip() for s in res if len(s.strip()) > 0]
        return res 
        
class Segmentation(object):
    
    def __init__(self, stop_words_file = None, 
                    allow_speech_tags = util.allow_speech_tags,
                    delimiters = util.sentence_delimiters):
        self.ws = WordSegmentation(stop_words_file=stop_words_file, allow_speech_tags=allow_speech_tags)
        self.ss = SentenceSegmentation(delimiters=delimiters)
        
    def segment(self, text, lower = False):
        text = util.as_text(text)
        sentences = self.ss.segment(text)
        words_no_filter = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = False,
                                                    use_speech_tags_filter = False)
        words_no_stop_words = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = True,
                                                    use_speech_tags_filter = False)

        words_all_filters = self.ws.segment_sentences(sentences=sentences, 
                                                    lower = lower, 
                                                    use_stop_words = True,
                                                    use_speech_tags_filter = True)

        return util.AttrDict(
                    sentences           = sentences, 
                    words_no_filter     = words_no_filter, 
                    words_no_stop_words = words_no_stop_words, 
                    words_all_filters   = words_all_filters
                )
    
        

if __name__ == '__main__':
    pass