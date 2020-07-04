import shutil

path = '../result/result_news/important_doc.txt'
lines = open(path, encoding='utf-8').readlines()
f1 = open('../result/result_news/top_50.txt', 'w', encoding='utf-8')
f2 = open('../result/result_news/sorted_top_50.txt', 'w', encoding='utf-8')

count = 0
top_50_time = []
for line in lines:
    f1.write(line)
    date = line.split('#')[1].replace('-', '')
    top_50_time.append(date)
    count += 1
    if count == 50:
        break
top_50 = lines[0:50]

l1, l2 = (list(t) for t in zip(*sorted(zip(top_50_time, top_50))))
print(l1)
print(l2)
for ss in l2:
    f2.write(ss)
titles = [ss.split('\t')[0] for ss in l2]
for path in titles:
    shutil.copy('../data/news/' + path, '../result/result_news/sorted_news_50')
