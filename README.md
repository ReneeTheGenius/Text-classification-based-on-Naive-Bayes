# Text-classification-based-on-Naive-Bayes
Simple text classification using Naive Bayes
## 流程
1. 预处理：将样本集进行正向最大匹配法分词
1. 生成带标签的数据集
1. 分割训练集和测试集，测试集占比0.1
1. 提取训练集tf-idf特征矩阵
1. 训练分类模型
1. 测试模型
## 文件
- train.py：训练模型
- fenci.py：分词工具
- text filter.py:UI界面