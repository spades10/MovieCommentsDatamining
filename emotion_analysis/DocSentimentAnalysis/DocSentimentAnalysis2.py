import sys
from 情感分析.DocSentimentAnalysis.sentence_parser import *
import ahocorasick
import jieba
import re
import math
import os
sys.path.append("DocSentimentAnalysis")
class Sentimentor():
    def __init__(self):
        # CUR_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        CUR_DIR = ''
        DICT_DIR = os.path.join(CUR_DIR,'dict')
        DescPath = os.path.join(DICT_DIR, 'desc_words.txt')
        SenPath = os.path.join(DICT_DIR, 'sentiment_words.txt')
        self.DescDict = {i.strip().split('\t')[0]:float(i.strip().split('\t')[1]) for i in open(DescPath, encoding='utf-8') if i.strip()}#修饰词典
        self.SenDict = {i.strip().split('\t')[0]:float(i.strip().split('\t')[1]) for i in open(SenPath, encoding='utf-8') if i.strip()}#情感词典
        self.SenTree = self.build_actree(list(self.SenDict.keys()))#情感词
        self.UserWords = list(set(list(self.DescDict.keys()) + list(self.SenDict.keys())))#总的词：情感词典加修饰词典
        jieba.load_userdict(self.UserWords)#载入
        self.senti_parser = LtpParser()
        self.senti_parser.aaa()


    def build_actree(self, wordlist):#建树：形如(0,(0,情感词))的列表
        actree = ahocorasick.Automaton()#字符串匹配，比如现在有个大的列表，客户输入一句话，如何根据客户输入的一句话，从大列表中匹配出字符串交集
        for index, word in enumerate(wordlist):
            word = ' ' + word + ' '
            actree.add_word(word, (index, word))
        actree.make_automaton()
        return actree

    '''content分句处理'''
    def seg_sentences(self, content):
        #文章标点符号分句后，去除各种特殊空格
        return [sentence.replace('\u3000','').replace('\xc2\xa0', '').replace(' ','') for sentence in re.split(r'[!?？！:;。\n\r]',content) if sentence]

    '''利用情感词过滤情感句'''
    def check_senti(self, sentence):
        flag = 0
        word_list = list(jieba.cut(sentence))#jieba对句子分词
        # print(word_list)
        senti_words = []
        for i in self.SenTree.iter(' '.join(word_list + [' '])):#将分割后的句子以空格将每个词分开
            senti_words.append(i[1][1].replace(' ', ''))
            flag += 1
        return flag, word_list, senti_words#返回包含的情感词数量，分词后的列表，一个句子的情感词列表

    '''情感句过滤'''
    #对文章中的每一个句子，返回（句子索引号，句子，分词后的列表，该句子的情感词列表）
    def filter_sentence(self, sentences):
        senti_sentences = list()
        for index, sentence in enumerate(sentences):
            flag, word_list, senti_words = self.check_senti(sentence)
            if flag:
                senti_sentences.append([index, sentence, word_list, senti_words])
        return senti_sentences

    '''sentence analysis'''
    def get_sentence_score(self, sent_words, senti_words):#对每一个句子计算得分
        sent_postag = self.senti_parser.get_postag(sent_words)#得到词性
        sent_tuples = self.senti_parser.syntax_parser(sent_words, sent_postag)#依存句法分析，返回列表，列表中每一个元素代表：单词索引，单词，单词词性，单词依存的单词和词性，索引和依存关系
        dep_dict = self.senti_parser.parser_dict(sent_words, sent_postag, sent_tuples)
        # 返回一个列表，其中每一个元素对应一个单词：依存于该单词的单词的列表（单词，词性，单词索引，依存关系对应的依存儿子和依存父亲的字典，父亲用B_依存关系作key）
        sent_score = 0.0
        for dep in dep_dict:
            word = dep[0]
            word_desc = dep[3]
            word_score = self.get_abs_sentiment(word, word_desc, senti_words)
            sent_score += word_score
            # print(dep, word_score)

        return math.tanh(sent_score)

    def get_abs_sentiment(self, word, word_desc, senti_words):
        if word not in senti_words:
            return 0.0
        else:
            word_score = self.SenDict.get(word, 0.6)
            if not word_desc:
                return word_score
            else:
                desc_words = []
                for rel, info in word_desc.items():#返回字典可遍历的键值对
                    desc_words += [i[1] for i in info if i[2][0] not in ['w', 'u']]#如果是依存儿子，如果他的词性不以w或u开头，则加入，如果是依存父亲，则加入其依存父亲
                for desc_word in desc_words:
                    desc_score = self.DescDict.get(desc_word, 1.0)
                    word_score *= desc_score#乘权重
            return word_score

    def doc_sentiment_score(self, contents):
        scores1 = []
        for content in contents:
            sents = self.seg_sentences(content)
            senti_sentences = self.filter_sentence(sents)
            scores = []
            for sent in senti_sentences:
                sent_words = sent[2]
                senti_words = sent[3]
                sent_score = self.get_sentence_score(sent_words, senti_words)
                # print(sent[1], sent_score)
                if sent_score:
                    scores.append(sent_score)
            if len(scores) > 0:
                scores1.append( sum(scores)/len(scores))
            else:
                scores1.append( 0.0 )
        return scores1
#整体思路：
#输入文本，将文本以标点符号为界限划分为很多句子，对每个句子分词，计算每个句子包含的情感词个数和情感词列表，然后过滤掉不包含情感词的句子。
# 对每个句子：
# 分词后得到每个词的词性，根据分词列表和词性列表进行该句子的依存句法分析，它返回一个列表，列表中每一个元素代表：单词索引，单词，单词词性，单词依存的单词和词性，索引和依存关系
# 然后基于上述得到的列表和分词列表词性列表计算句子中每一个词（不同依存关系-依存儿子和依存父亲）的字典映射
#最终流程：对过滤后的每个句子分词列表遍历，若单词是情感词，则根据情感词典得到其对应分数，接着若该词存在依存父亲和儿子，则该依存父亲或儿子是修饰词且词性不以w或u
# 开头，则在修饰词典找到其权重，与上述分数相乘，迭代后得到该词的最终分数，每个句子所有词分数相加得到该句子的最终分数。
# 文章最后分数等于所有句子分数之和/句子总数
# 词性详见https://ltp.readthedocs.io/zh_CN/latest/appendix.html#id5
