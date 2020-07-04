import csv


ff1 = "../data/weibo_comments.csv"
ff2 = "../data/weibo_topic.csv"
file1 = "../source_data/man_weibo.txt"
file2 = "../source_data/woman_weibo.txt"
file3 = "../source_data/all_weibo.txt"
with open(ff1, 'r', encoding='UTF-8', errors='ignore') as f:
    reader1= csv.DictReader(f)
    sex1 = []
    comments1 = []
    for row in reader1:
        if row['gender'] == 'f':
            sex1.append("男")
        else:
            sex1.append("女")
        comments1.append(row['text'])
with open(ff2, 'r', encoding='UTF-8', errors='ignore') as f:
    reader2 = csv.DictReader(f)
    sex2 = []
    comments2 = []
    for row in reader2:
        sex2.append(row['发布者性别'])
        comments2.append(row['微博正文'])

f1 = open(file1, 'a', encoding='utf-8')
f2 = open(file2, 'a', encoding='utf-8')
f3 = open(file3, 'a', encoding='utf-8')
count_man = 0
count_woman = 0
count_all = 0
for i in range(len(sex1)):
    s = comments1[i].replace(' ', '').replace('\n', '').replace('\r', '')
    if len(s) > 0:
        f3.write(s + '\r')
        count_all += 1
        if sex1[i] == '男':
            f1.write(s + '\r')
            count_man += 1
        else:
            f2.write(s + '\r')
            count_woman += 1
for i in range(len(sex2)):
    s = comments2[i].replace(' ', '').replace('\n', '').replace('\r', '')
    if len(s) > 0:
        f3.write(s + '\r')
        count_all += 1
        if sex2[i] == '男':
            f1.write(s + '\r')
            count_man += 1
        else:
            f2.write(s + '\r')
            count_woman += 1

print(count_man)
print(count_woman)
print(count_all)
