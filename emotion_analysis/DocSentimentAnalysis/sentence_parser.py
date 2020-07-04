import jieba
from pyltp import Postagger,Parser
import os

class LtpParser():
    def __init__(self):
        # CUR_DIR = '/'.join(os.path.abspath(__file__).split('/')[:-1])
        CUR_DIR = 'D:/Programming/Python_project/big_data/情感分析/DocSentimentAnalysis'
        # LTP_DIR = os.path.join(CUR_DIR, "ltp_data")
        LTP_DIR = 'C:/Users/Admin/Desktop/ltp_data_v3.4.0'
        self.postagger = Postagger()
        # self.postagger.load(os.path.join(LTP_DIR, "pos.model"))
        self.parser = Parser()
        # self.parser.load(os.path.join(LTP_DIR, "parser.model"))

    def aaa(self):
        LTP_DIR = 'C:/Users/Admin/Desktop/ltp_data_v3.4.0'
        self.postagger.load(os.path.join(LTP_DIR, "pos.model"))
        self.parser = Parser()
        self.parser.load(os.path.join(LTP_DIR, "parser.model"))
    '''ltp基本操作'''
    def get_postag(self, words):#词性标注
        return list(self.postagger.postag(words))

    '''依存关系格式化'''
    def syntax_parser(self, words, postags):
        arcs = self.parser.parse(words, postags)#依存句法分析
        words = ['Root'] + words
        postags = ['w'] + postags
        dep_tuples = list()
        for index in range(len(words)-1):
            arc_index = arcs[index].head#依存弧父节点的索引，ROOT节点的索引是0，第一个词开始的索引依次为1、2、3，
            arc_relation = arcs[index].relation#表示依存弧的关系
            dep_tuples.append([index+1, words[index+1], postags[index+1], words[arc_index], postags[arc_index], arc_index, arc_relation])
        return dep_tuples#返回列表，列表中每一个元素代表：单词索引，单词，单词词性，单词依存的单词和词性，索引和依存关系

    '''为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def parser_dict_old(self, words, postags, tuples):
        child_dict_list = list()
        for index, word in enumerate(words):
            child_dict = dict()
            for arc in tuples:
                if arc[3] == word:
                    if arc[-1] in child_dict:
                        child_dict[arc[-1]].append(arc)
                    else:
                        child_dict[arc[-1]] = []
                        child_dict[arc[-1]].append(arc)
            child_dict_list.append([word, postags[index], index, child_dict])
        return child_dict_list#返回一个列表，其中每一个元素对应一个单词：依存于该单词的单词的列表（单词，词性，单词索引，依存关系对应的依存儿子的字典）


    '''为句子中的每个词语维护一个保存句法依存儿子节点的字典'''
    def parser_dict(self, words, postags, tuples):
        child_dict_list = list()
        for index, word in enumerate(words):
            child_dict = dict()
            for arc in tuples:
                if arc[3] == word:
                    rel = arc[-1]
                    if rel in child_dict:
                        child_dict[rel].append(arc)
                    else:
                        child_dict[rel] = []
                        child_dict[rel].append(arc)
                if arc[1] == word:
                    rel = 'B_' + arc[-1]
                    arc = [arc[-2], arc[-4], arc[-3], arc[1], arc[2], arc[0], rel]
                    if rel in child_dict:
                        child_dict[rel].append(arc)
                    else:
                        child_dict[rel] = []
                        child_dict[rel].append(arc)
            child_dict_list.append([word, postags[index], index, child_dict])
        return child_dict_list
#返回一个列表，其中每一个元素对应一个单词：依存于该单词的单词的列表（单词，词性，单词索引，依存关系对应的依存儿子和依存父亲的字典，父亲用B_依存关系作key

