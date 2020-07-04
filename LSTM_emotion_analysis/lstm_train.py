
import pandas as pd 
import numpy as np 
import jieba
import multiprocessing
import keras.utils
from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
from keras.preprocessing import sequence

from sklearn.cross_validation import train_test_split
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout,Activation
from keras.models import model_from_yaml
np.random.seed(1337)  # For Reproducibility
import sys
sys.setrecursionlimit(1000000)
import yaml

# set parameters:
cpu_count = multiprocessing.cpu_count()  # 控制训练的并行数
vocab_dim = 100  # 特征向量的维度
n_iterations = 4  # 迭代的次数
n_exposures = 10  # 可以对字典做截断. 词频少于min_count次数的单词会被丢弃掉
window_size = 7  # 窗口大小，表示当前词与预测词在一个句子中的最大距离是多少
n_epoch = 15
input_length = 100
maxlen = 100

batch_size = 32


def loadfile():
    neg=pd.read_csv('data/neg.csv',header=None,index_col=None)
    pos=pd.read_csv('data/pos.csv',header=None,index_col=None,error_bad_lines=False)
    neu=pd.read_csv('data/neutral.csv', header=None, index_col=None)

    combined = np.concatenate((pos[0], neu[0], neg[0]))
    y = np.concatenate((np.ones(len(pos), dtype=int), np.zeros(len(neu), dtype=int), 
                        -1*np.ones(len(neg),dtype=int)))

    return combined, y


# 对句子经行分词，并去掉换行符
def tokenizer(text):
    text = [jieba.lcut(document.replace('\n', '')) for document in text]
    return text


def create_dictionaries(model=None,
                        combined=None):
    if (combined is not None) and (model is not None):
        gensim_dict = Dictionary()
        gensim_dict.doc2bow(model.wv.vocab.keys(),
                            allow_update=True)
        w2indx = {v: k+1 for k, v in gensim_dict.items()}  # 所有频数超过10的词语的索引,(k->v)=>(v->k)
        f = open("word2index.txt",'w',encoding='utf8')
        for key in w2indx:
            f.write(str(key))
            f.write(' ')
            f.write(str(w2indx[key]))
            f.write('\n')
        f.close()
        w2vec = {word: model[word] for word in w2indx.keys()}  # 所有频数超过10的词语的词向量, (word->model(word))

        def parse_dataset(combined):
            data=[]
            for sentence in combined:
                new_txt = []
                for word in sentence:
                    try:
                        new_txt.append(w2indx[word])
                    except:
                        new_txt.append(0)
                data.append(new_txt)
            return data # word=>index
        combined=parse_dataset(combined)  # [[1,2,3...],[]]
        combined= sequence.pad_sequences(combined, maxlen=maxlen)  # 每个句子所含词语对应的索引，所以句子中含有频数小于10的词语，索引为0
        return w2indx, w2vec,combined
    else:
        print ('No data provided...')


#  创建词语字典，并返回每个词语的索引，词向量，以及每个句子所对应的词语索引
def word2vec_train(combined):

    model = Word2Vec(size=vocab_dim,
                     min_count=n_exposures,
                     window=window_size,
                     workers=cpu_count,
                     iter=n_iterations)
    model.build_vocab(combined) # input: list
    model.train(combined,total_examples=model.corpus_count,epochs=model.iter)
    model.save('model/Word2vec2_model.pkl')
    index_dict, word_vectors,combined = create_dictionaries(model=model,combined=combined)
    return   index_dict, word_vectors,combined


def get_data(index_dict,word_vectors,combined,y):

    n_symbols = len(index_dict) + 1  # 所有单词的索引数，频数小于10的词语索引为0，所以加1
    embedding_weights = np.zeros((n_symbols, vocab_dim))  # 初始化 索引为0的词语，词向量全为0
    for word, index in index_dict.items():  # 从索引为1的词语开始，对每个词语对应其词向量
        embedding_weights[index, :] = word_vectors[word]
    x_train, x_test, y_train, y_test = train_test_split(combined, y, test_size=0.2)
    y_train = keras.utils.to_categorical(y_train, num_classes=3)
    y_test = keras.utils.to_categorical(y_test, num_classes=3)
    # print x_train.shape,y_train.shape
    return n_symbols,embedding_weights, x_train, y_train, x_test, y_test


##定义网络结构
def train_lstm(n_symbols, embedding_weights, x_train, y_train, x_test, y_test):
    print ('Defining a Simple Keras Model...')
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=n_symbols,  # 字典长度
                        mask_zero=True,
                        weights=[embedding_weights],
                        input_length=input_length))  # 当输入序列的长度固定时，该值为其长度
    model.add(LSTM(output_dim=50, activation='tanh'))
    # model.add(Dropout(0.5))
    model.add(Dense(3, activation='softmax'))
    model.add(Activation('softmax'))

    print ('Compiling the Model...')
    model.compile(loss='categorical_crossentropy',
                  optimizer='adam',metrics=['accuracy'])

    print ("Train...") # batch_size=32
    model.fit(x_train, y_train, batch_size=batch_size, epochs=n_epoch,verbose=1)

    print ("Evaluate...")
    score = model.evaluate(x_test, y_test,
                                batch_size=batch_size)

    yaml_string = model.to_yaml()
    with open('model/lstm2.yml', 'w') as outfile:
        outfile.write( yaml.dump(yaml_string, default_flow_style=True) )
    model.save_weights('model/lstm2.h5')
    print('Test score:', score)


# 训练模型，并保存
print ('Loading Data...')
combined,y=loadfile()
print (len(combined),len(y))
print ('Tokenising...')
combined = tokenizer(combined)
print ('Training a Word2vec model...')
index_dict, word_vectors,combined=word2vec_train(combined)

print ('Setting up Arrays for Keras Embedding Layer...')
n_symbols,embedding_weights,x_train,y_train,x_test,y_test=get_data(index_dict, word_vectors,combined,y)
print ("x_train.shape and y_train.shape:")
print (x_train.shape,y_train.shape)
train_lstm(n_symbols,embedding_weights,x_train,y_train,x_test,y_test)
