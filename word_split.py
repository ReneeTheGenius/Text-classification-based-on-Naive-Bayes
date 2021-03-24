import time
#加载词典
def load_dict():
     filename = '词典.txt'
     f = open(filename,encoding = 'utf-8')
     word_set = set()
     length = 1
     for line in f:
         line = line.strip()
         word_set.add(line)
         if len(line) > length:
             length = len(line)
     return length,word_set
 
 #遍历分割begin-end最大长度词是否在集合中，在集合中则加入列表，break,begin = end
 #不在列表中，继续for循环判断最大长度-1词是否在集合中
 #分割句子
def split_word(sentence,max_len,word_set):    
     begin = 0
     words = []
     while begin < len(sentence):
         for end in range(min(begin + max_len,len(sentence)),begin,-1):
             if sentence[begin:end] in word_set or end == begin + 1:
                 words.append(sentence[begin:end])
                 break
         begin = end
     return words
 #分割文章，保存分词结果，计算速度
def split(test,output):
    mylist=[]
    f=open(test,'r',encoding='utf-8',)
    lines = f.readlines()
    f.close
    start=time.time()
    max_len,word_set = load_dict()
    for line in lines:
        mylist.extend(split_word(line,max_len,word_set))
    running_time = time.time()-start
    out = open(output,'w',encoding='utf-8',)
    for t in mylist:#将分词结果写入生成文件
         if t == '\n' :
             out.write('\n')
         else:
             out.write(t)
             out.write("  ")
    out.close()
    return running_time

def precision(out,gold):
    #计算区间
    def to_region_set(line):
        region =[]
        start = 0
        for word in line.split():
            end = start + len(word)
            region.append((start,end-1))
            start = end
        return region 
    
    fpredict = open(out,'r',encoding='utf-8',)
    mylines = fpredict.readlines()
    fpredict.close()
  
    fgold = open(gold,'r',encoding = 'utf-8',)
    gold_lines = fgold.readlines()
    fgold.close()

 #计算准确率   
    B_size = 0
    A_cap_B_size = 0
    for g,p in list(zip(gold_lines,mylines)):
        A,B = set(to_region_set(g)),set(to_region_set(p))
        #print(A)
        #print(B)
        B_size += len(B)
        A_cap_B_size += len(A & B)
    Precision = A_cap_B_size / B_size
    return Precision,A_cap_B_size ,B_size 

test = "test.txt"
output = "out.txt"
gold = "gold.txt"

running_time = split(test,output)
Precision,correct_words,total_words = precision(output,gold)
Precision*=100
rate = running_time/total_words

print("速度:%.8f 秒/词" %rate)
print("总分词数:",total_words)
print("正确分词数:",correct_words)
print("准确率:%.2f%%" % Precision)