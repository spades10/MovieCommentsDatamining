
import jieba.analyse
from PIL import Image,ImageSequence
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties  
from wordcloud import WordCloud,ImageColorGenerator


font = FontProperties(fname='./simsun.ttc')
bar_width = 0.5
lyric = ''

f = open('../result/result_weibo/keywords_all_weibo.txt', 'r', encoding='utf-8')
# f = open('../result/result_weibo/keywords_man_weibo.txt', 'r', encoding='utf-8')
# f = open('../result/result_weibo/keywords_woman_weibo.txt', 'r', encoding='utf-8')

# f = open('../result/result_douban/keywords_douban.txt', 'r', encoding='utf-8')

# f = open('../result/result_news/keywords_news.txt', 'r', encoding='utf-8')

for i in f:
    lyric += f.read()

result = jieba.analyse.textrank(lyric, topK=50, withWeight=True)

keywords = dict()
for i in result:
    keywords[i[0]] = i[1]
print(keywords)

image= Image.open('./background.png')
graph = np.array(image)
print(graph)
wc = WordCloud(font_path='./simsun.ttc', background_color='White', max_words=50,mask=graph)
wc.generate_from_frequencies(keywords)
image_color = ImageColorGenerator(graph)#设置背景图像
plt.imshow(wc)
plt.imshow(wc.recolor(color_func=image_color))  #根据背景图片着色
plt.axis("off") #不显示坐标轴
plt.show()
wc.to_file('../result/result_weibo/cloud/cloud_all.jpg')
# wc.to_file('../result/result_weibo/cloud/cloud_man.jpg')
# wc.to_file('../result/result_weibo/cloud/cloud_woman.jpg')

# wc.to_file('../result/result_douban/cloud/cloud_douban.jpg')

# wc.to_file('../result/result_news/cloud/cloud_news.jpg')

X=[]
Y=[]

for key in keywords:
    
    X.append(key)
    Y.append(keywords[key])

num = len(X)
   
fig = plt.figure(figsize=(28, 10))  #图的高宽
plt.bar(range(num), Y, tick_label = X, width = bar_width)
plt.xticks(rotation=50, fontproperties=font, fontsize=20)
plt.yticks(fontsize=20)
plt.title("words-frequency chart", fontproperties=font, fontsize=30)
plt.savefig("../result/result_weibo/cloud/barChart_all.jpg", dpi=360)
# plt.savefig("../result/result_weibo/cloud/barChart_man.jpg", dpi=360)
# plt.savefig("../result/result_weibo/cloud/barChart_woman.jpg", dpi=360)

# plt.savefig("../result/result_douban/cloud/barChart_douban.jpg", dpi=360)

# plt.savefig("../result/result_news/cloud/barChart_news.jpg", dpi= 60)

plt.show()
