import os
import fenci
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib
from sklearn.metrics import confusion_matrix
import pickle

# 数据预处理
def preprocess(file):
    text_with_space = ""
    textcute = fenci.split(file)#正向最大分词
    for word in textcute:
        text_with_space += word + " "#以空格划分词语
    return text_with_space


#加载数据集
def loadtrainset(path, classtag):
    allfiles = os.listdir(path)  # os.path.isdir()用于判断对象是否为一个目录，并返回此目录下的所有文件名
    processed_textset = []
    allclasstags = []

    for thisfile in allfiles:
        path_name = path + "/" + thisfile
        processed_textset.append(preprocess(path_name))
        allclasstags.append(classtag)
    return processed_textset, allclasstags  # list形式--processed_textset 文件的具体内容， allclasstags 文件分类

#预测
def predict(file):
    x = preprocess(file)
    count_vector = CountVectorizer(decode_error="replace", vocabulary=pickle.load(open('tf_features', "rb")))
    new_count_vector = count_vector.transform([x])
    new_tfidf = TfidfTransformer(use_idf=False).fit_transform(new_count_vector)
    clf=joblib.load('clf.model')
    predict_result = clf.predict(new_tfidf)
    return predict_result


if __name__ == '__main__':
    classes = ['体育', '娱乐', '彩票', '房产', '教育', '时尚', '社会', '科技', '股票']
    data = []
    classtags_list =[]
    for c in classes:
        processed_textdata, class1 = loadtrainset("语料/"+c, c)
        data += processed_textdata
        classtags_list += class1
    
    train_x,test_x, train_y, test_y = train_test_split(data,classtags_list,test_size=0.1,)
    del data

    count_vector = CountVectorizer()
    vecot_matrix = count_vector.fit_transform(train_x)
    train_tfidf = TfidfTransformer(use_idf=False).fit_transform(vecot_matrix)
    with open('tf_features', 'wb') as fw:
        pickle.dump(count_vector.vocabulary_, fw)
    
    '''
    
    TfidfTransformer是统计CountVectorizer中每个词语的tf-idf权值
    tfidf = transformer.fit_transform(vectorizer.fit_transform(corpus))
    vectorizer.fit_transform(corpus)将文本corpus输入，得到词频矩阵
    
    将这个矩阵作为输入，用transformer.fit_transform(词频矩阵)得到TF-IDF权重矩阵
    TfidfTransformer + CountVectorizer  =  TfidfVectorizer

    '''
    
    #clf = MultinomialNB().fit(train_tfidf, train_y)
    #joblib.dump(clf,'clf.model')#保存模型
    
    clf=joblib.load('clf.model')
    pred_list=[]
    for i in range(0,len(test_x)):
        new_count_vector = count_vector.transform([test_x[i]])
        new_tfidf = TfidfTransformer(use_idf=False).transform(new_count_vector)
        predict_result = clf.predict(new_tfidf)
        pred_list.append(predict_result)
   
    m = confusion_matrix(test_y, pred_list, classes)#混淆矩阵
    n = len(m)
    for i in range(len(m[0])):
        rowsum, colsum = sum(m[i]), sum(m[r][i] for r in range(n))
        try:
            print (classes[i],'类别的准确率: %.4f%%' % (m[i][i]/float(colsum)*100), '召回率: %.4f%%'  % (m[i][i]/float(rowsum)*100))
        except ZeroDivisionError:
            print (classes[i],'类别的准确率: %.4f%%' % 0, '召回率: %.4f%%' %0)
