import os
import association


def mkdir_if_missing(path):
    if not os.path.exists(path):
        os.mkdir(path)

 
if __name__ == "__main__":
    # a = association('../result/result_douban/keywords_douban.txt', 0.5, 0.5, 3)
    prefix = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    platforms = ['douban', 'news', 'weibo']
    result_path = os.path.join(prefix, 'result', 'association')
    mkdir_if_missing(result_path)
    for platform in platforms:
        if platform == 'weibo':
            data_file = os.path.join(prefix, 'result', 'result_{}'.format(platform), 'keywords_all_{}.txt'.format(platform))
            result_file = os.path.join(result_path, 'association_{}.txt'.format(platform))
        else:
            data_file = os.path.join(prefix, 'result', 'result_{}'.format(platform), 'keywords_{}.txt'.format(platform))
            result_file = os.path.join(result_path, 'association_{}.txt'.format(platform))
        print(data_file)
        print(result_file)
        a = association.association(data_file, result_file, 0.005, 0.1, 5)
    