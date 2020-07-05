# MovieCommentsDataMining
data mining for movie comments
# 基于TextRank与情感分析的电影多维度评判
对《流浪地球》在豆瓣、新浪网等网站的用户评论情感进行数据挖掘，采用方法包括:词频统计、TextRank算法、LSTM
模型、Apriori算法、词云等。 
# Install
```
git clone https://github.com/Bruce-yi/MovieCommentsDatamining
cd MovieCommentsDataMining
pip install requirements.txt
```
# Usage
## Data collect
```
python Scrapy/WeiboCommentScrapy.py
python Scrapy/WeiboTopicScrapy.py
python DoubanScrapy.py --user username --passwd password
```
you can change your prefer setting in the script
## Data preprocess
split the sentence into words
```
python keywords_abstract/implement/split_words.py
```
extract keywords
```
python keywords_abstract/implement/key_word.py
```
# Algorithms
## LSTM
using LSTM to analyze emotion in comments which is divided into two phases. Firstly training a LSTM model using existed data, then using trained model to predict the emotion in comments.
```
python LSTM_emotion_analysis/lstm_train.py
python LSTM_emotion_analysis/lstm_test.py
```
## LTP
using LTP to analyze emotion in comments
```
python emotion_analysis/DocSentimentAnalysis/run.py
```
## Apriori
using Apriori to mine frequency and association
```
python association main.py
```
# Notes
Because the project is divided into a several steps, you need to gain previous step's result before starting next step. Also, arranging all the result into a common folder is a nice choice.
# Samples
## douban
word frenquency chart  
![chart](https://github.com/Bruce-yi/MovieCommentsDatamining/blob/master/sample/barChart_douban.jpg)  
word cloud  
![word cloud](https://github.com/Bruce-yi/MovieCommentsDatamining/blob/master/sample/cloud_douban.jpg)  
you can find more detial in sample
## comparision
comments comparision in different platform  
![platform](https://github.com/Bruce-yi/MovieCommentsDatamining/blob/master/sample/platform_comments_comparasion.png)  
comments comparision in different sex  
![sex](https://github.com/Bruce-yi/MovieCommentsDatamining/blob/master/sample/weibo_men_women_comments.png)
