import jieba
import re
from gensim import corpora
from gensim.similarities import Similarity
import gensim
import os

def Symbol_filter(str):
    # 使用正则表达式过滤标点符号
    result = re.sub('\W+', '', str).replace("_", '')
    return result
def get_content (path):
    # 文本处理，将我们的文本处理为字符串，并且过滤掉标点符号
    string = ''
    file = open(path, 'r', encoding='UTF-8')
    one_line = file.readline()
    while one_line:
        string += one_line
        one_line = file.readline()
    # 调用标点符号过滤函数
    string = Symbol_filter(string)
    file.close()
    return string
def Turn_vector(str):
    # 将我们的字符串切片
    string = jieba.lcut(str)
    return string
def similarity_vul(str_x,str_y):
    texts = [str_x, str_y]
    # 语料库
    dictionary = gensim.corpora.Dictionary(texts)
    print(dictionary)
    num_features = len(dictionary.token2id)
    # 利用doc2bow作为词袋模型
    corpus = [dictionary.doc2bow(text) for text in texts]
    print(corpus)
    similarity = gensim.similarities.Similarity('-Similarity-index', corpus, num_features)
    # 获取文章相似度
    test_corpus_1 = dictionary.doc2bow(str_x)
    cosine_sim = similarity[test_corpus_1][1]
    return cosine_sim
def main_test():
    path_1 = input("参考论文的绝对路径：")
    path_2 = input("待检察文件的绝对路径：")
    if not os.path.exists(path_1):
        print("文件不存在")
        exit()
    if not os.path.exists(path_2):
        print("文件不存在")
        exit()
    #path_1 = "d:/test1/orig.txt"  # 参考的论文
    #path_2 = "d:/test1/orig_0.8_dis_15.txt"  # 待检察论文
    save_path = 'D:/test1/out.txt'  # 输出结果的文件
    print('将文本提取出来，去除标点符号，转化为字符串: ')
    str_1 = get_content(path_1)
    str_2 = get_content(path_2)
    print(str_1)
    print(str_2)
    vector_1=Turn_vector(str_1)
    vector_2=Turn_vector(str_2)
    similarity = similarity_vul(vector_1, vector_2)
    print("这两篇文章的相似度： %.2f"%similarity)
    #  将相似度结果写入指定文件
    f = open(save_path, 'w', encoding="utf-8")
    f.write("这两篇文章的相似度： %.2f"%similarity)
    f.close()
if __name__ == '__main__':
    main_test()