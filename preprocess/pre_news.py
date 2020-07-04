import os.path


path = '../data/news'
files = os.listdir(path)

count = 0
f = open('../source_data/news.txt', 'a', encoding='utf-8')
for file in files:
    txt_path = '../data/news/' + file
    contents = open(txt_path, 'r', encoding='utf-8',errors='ignore')
    count += 1
    for content in contents:
        content = content.strip('\n').strip('\r').strip('\r\n')
        f.write(content)
    f.write('\r')

print(count)
