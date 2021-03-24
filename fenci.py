#加载词典
def load_dict():
     filename = '词典.txt'#词典路径
     f = open(filename,encoding = 'utf-8')#打开词典
     word_set = set()
     length = 1
     for line in f:#读取每一行
         line = line.strip()#去掉空格
         word_set.add(line)#添加词语
         if len(line) > length:
             length = len(line)#取最长词语长度
     return length,word_set
 
#分割句子
def split_word(sentence,max_len,word_set):    
     begin = 0
     words = []
     while begin < len(sentence):#句子不为空
         for end in range(min(begin + max_len,len(sentence)),begin,-1):#先取最长单词
             if sentence[begin:end] in word_set or end == begin + 1:#词语在词典中或是单字
                 words.append(sentence[begin:end])#分词
                 break
         begin = end
     return words
 
#分割文章
def split(test):
    mylist=[]
    f=open(test,'r',encoding='utf-8',)#读取要分词的文件
    lines = f.readlines()#读取每一行
    f.close
    max_len,word_set = load_dict()
    for line in lines:   #对每一行单独分词
        mylist.extend(split_word(line,max_len,word_set))
    return mylist