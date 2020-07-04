import jieba
import numpy as np
import yaml
import sys
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence
from keras import backend as K
from keras.models import model_from_yaml
# K.clear_session()


np.random.seed(1337)  # For Reproducibility
sys.setrecursionlimit(1000000)
# define parameters
maxlen = 100
w2indx = {}
f = open("word2index.txt", 'r', encoding='utf8')
lines = f.readlines()
for line in lines:
    if line.strip()=='':
        continue
    s = line.split()
    # print(s)
    w2indx[s[0]]=int(s[1])
f.close()

def create_dictionaries(words):
    data =[]
    for sentence in words:
        new_txt = []
        for word in sentence:
            try:
                new_txt.append(w2indx[word])
            except:
                new_txt.append(0)
        data.append(new_txt)
    combined= sequence.pad_sequences(data, maxlen=maxlen)
    return combined



def input_transform(string):
    words = jieba.lcut(string)
    print(words)
    words = np.array(words).reshape(1,-1)
    #model=Word2Vec.load('../model/Word2vec_model.pkl')
    #_,_,combined=create_dictionaries(model,words)
    combined = create_dictionaries(words)

    return combined


def lstm_predict(comments):
    # f1 = open('../result/result_weibo/sentiment_analysis_result/with_senti_lstm_weibo_all.txt','w',
    #           encoding='utf-8')
    # f1 = open('../result/result_weibo/sentiment_analysis_result/with_senti_lstm_weibo_man.txt', 'w',
    #           encoding='utf-8')
    # f1 = open('../result/result_weibo/sentiment_analysis_result/with_senti_lstm_weibo_woman.txt', 'w',
    #           encoding='utf-8')
    # f1 = open('../result/result_douban/sentiment_analysis_result/with_senti_lstm_douban.txt', 'w',
    #           encoding='utf-8')
    f1 = open('../result/result_news/sentiment_analysis_result/with_senti_lstm_news.txt', 'w',
              encoding='utf-8')

    # f2 = open('../result/result_weibo/sentiment_analysis_result/without_senti_lstm_weibo_all.txt', 'w',
    #           encoding='utf-8')
    # f2 = open('../result/result_weibo/sentiment_analysis_result/without_senti_lstm_weibo_man.txt', 'w',
    #           encoding='utf-8')
    # f2 = open('../result/result_weibo/sentiment_analysis_result/without_senti_lstm_weibo_woman.txt', 'w',
    #           encoding='utf-8')
    # f2 = open('../result/result_douban/sentiment_analysis_result/without_senti_lstm_douban.txt', 'w',
    #           encoding='utf-8')
    f2 = open('../result/result_news/sentiment_analysis_result/without_senti_lstm_news.txt', 'w',
              encoding='utf-8')

    print ('loading model......')
    with open('model/lstm.yml', 'r') as f:
        yaml_string = yaml.load(f)
    model = model_from_yaml(yaml_string)

    print ('loading weights......')
    model.load_weights('model/lstm.h5')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])
    count_pos = 0
    count_neg = 0
    length = len(comments)
    for string in comments:
        data=input_transform(string)
        data.reshape(1,-1)
        print(data)
        result=model.predict_classes(data)

        if result[0] == 1:
            f1.writelines(string+' '+ 'positive\n')
            f2.write('positive\r')
            count_pos += 1
        elif result[0] == 0:
            f1.writelines(string+' '+ 'neural\n')
            f2.write('neural\r')
        else:
            f1.writelines(string+' '+ 'negative\n')
            f2.write('negative\r')
            count_neg +=1

    pos = (count_pos * 1.0 / length) * 100
    neg = (count_neg * 1.0 / length) * 100

    f1.write('支持人数为：' + str(count_pos) + '\r')
    f1.write('反对人数为：' + str(count_neg) + '\r')
    f1.write('总人数为：' + str(length) + '\r')
    f1.write('支持率为：' + str(pos) + '%\r')
    f1.write('反对率为：' + str(neg) + '%\r')

    f2.write('支持人数为：' + str(count_pos) + '\r')
    f2.write('反对人数为：' + str(count_neg) + '\r')
    f2.write('总人数为：' + str(length) + '\r')
    f2.write('支持率为：' + str(pos) + '%\r')
    f2.write('反对率为：' + str(neg) + '%\r')


if __name__=='__main__':
    # f = open('../source_data/all_weibo.txt', 'r', encoding='utf-8').readlines()
    # f = open('../source_data/man_weibo.txt', 'r', encoding='utf-8').readlines()
    # f = open('../source_data/woman_weibo.txt', 'r', encoding='utf-8').readlines()

    # f = open('../source_data/douban.txt', 'r', encoding='utf-8').readlines()

    f = open('../source_data/news.txt', 'r', encoding='utf-8').readlines()

    lstm_predict(f)
