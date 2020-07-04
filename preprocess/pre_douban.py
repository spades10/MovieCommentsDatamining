import csv


file1 = "../data/douban_changping.csv"
file2 = "../data/douban_duanping.csv"
file3 = "../source_data/douban.txt"
with open(file1, 'r', encoding='UTF-8', errors='ignore') as f1:
    reader1 = csv.DictReader(f1)
    comments1 = []
    for row in reader1:
        comments1.append(row['text'])
with open(file2, 'r', encoding='UTF-8', errors='ignore') as f2:
    reader2 = csv.DictReader(f2)
    comments2 = []
    for row in reader2:
        comments2.append(row['text'])

f = open(file3, 'a', encoding='utf-8')
count_all = 0
for s in comments1:
    i = s.replace(' ', '').replace('\n', '').replace('\r', '')
    if len(i) > 0:
        count_all += 1
        f.write(i + '\r')
for s in comments2:
    i = s.replace(' ', '').replace('\n', '').replace('\r', '')
    if len(i) > 0:
        count_all += 1
        f.write(i + '\r')

print(count_all)
