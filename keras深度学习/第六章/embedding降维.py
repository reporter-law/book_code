"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:注意：此处没有词向量，只有词索引列表，embedding只是对索引列表进行降维,即高维数据低维表示
#再次强调，降低了运算量不是因为词向量的出现，而是因为把one hot型的矩阵运算简化为了查表操作
#词向量通过降维技术表征文本数据集中的词的共现信息
import os
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
"""词例token,文本向量化的两种方法：one-hor,词嵌入emebedding"""
"""单词级的one-hot
embedding只是一个对one-hot进行降维的网络层，one-hot经过emnedding后降维成低维稠密向量，因而没有考虑单词之间的关系与句子结构
验证精度74实际上是根据字计算的分类"""

def word_one_hot():
    import numpy as np

    samples = ['This is a dog', 'The is a cat']

    all_token_index = {}  # 构建一个字典来存储数据中的所有标记的索引

    for sample in samples:
        for word in sample.split():  # 拆分每一个单词
            if word not in all_token_index:  # 为每一个单词指定一个索引
                all_token_index[word] = len(all_token_index) + 1

    max_length = 10
    result = np.zeros(shape=(len(samples), max_length, max(all_token_index.values()) + 1))  # 向量长度为词典长度+1

    for i, sample in enumerate(samples):  # 获取sample中的索引和值
        for j, word in list(enumerate(sample.split()))[:max_length]:  # 获取单词的索引和值
            index = all_token_index.get(word)
            result[i, j, index] = 1
    print(result)

def charate_one_hot():
    import string
    import numpy as np
    samples = ['This is a dog', 'The is a cat']
    characters = string.printable  # 包含所有可打印的ASCII字符
    # 把所有可打印字符都装进字典中，从1开始索引
    all_token_index = dict(zip(range(1, len(characters) + 1), characters))

    max_length = 50#限制长度
    result = np.zeros(shape=(len(samples), max_length, max(all_token_index.keys()) + 1))

    for i, sample in enumerate(samples):  # 获取sample中的索引和值
        for j, character in enumerate(sample):
            index = all_token_index.get(character)
            result[i, j, index] = 1
    print(result)
#charate_one_hot()

def keras_one_hot():
    from keras.preprocessing.text import Tokenizer

    samples = ['The cat sat on the mat.', 'The dog ate my homework, he dog ate my homework.']

    # 我们创建一个标记器，配置为仅考虑前1000个最常用的词

    tokenizer = Tokenizer(num_words=1000)
    # 这将建立单词索引
    tokenizer.fit_on_texts(samples)

    # 他是如何恢复计算出的单词索引的方法
    word_index = tokenizer.word_index
    print('word_index:', word_index)
    # 这会将字符串转换为整数索引列表。
    """就是用索引表示当前句子结构"""
    sequences = tokenizer.texts_to_sequences(samples)
    print('sequences:', sequences)
    print('sequences.type', type(sequences))
    """先建立的是字典，然后向量化"""
    # 您还可以直接获得一键二进制表示。请注意，除了一键编码之外，还支持其他矢量化模式！
    one_hot_results = tokenizer.texts_to_matrix(samples, mode='binary')
    print('one_hot_results:\n', one_hot_results)
    print('one_hot_results.shape:', one_hot_results.shape)
    print('Found %s unique tokens.' % len(word_index))

"""词嵌入技术：就是词向量，就是将语言映射到低维稠密的几何空间中，特点是使得几何关系表述语义关系，方法为随机权重然后训练
一个任务一个词嵌入，因为语义关系复杂"""
def embedding():
    """生成这种映射的方法包括神经网络，单词共生矩阵的降维，寻找共现频次，进行标签降维"""
    from keras.layers import Embedding
    # 嵌入层至少接受两个参数：可能的token数（此处为1000（1 +最大字索引））和嵌入的维数（此处为64）。
    """这里是 64,有64个特征组成一个单词）"""
    embedding_layer = Embedding(1000, 64)
    from keras.datasets import imdb
    from keras import preprocessing

    #视为特征的字数，对字典限制
    max_features = 10000
    # 在此数量的单词之后剪切文本（在最常见的max_features个单词中）,评论长度限制20个单词
    """分句？？？？？？,不是而是对每一条输入评论的大小限制"""
    maxlen = 20
    #将数据加载为整数列表。
    (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
    print(imdb.load_data(num_words=max_features))
    # 这会将我们的整数列表转换为形状为（（samples，maxlen）`）的2D整数张量，每一个训练集的样本数，与输入频评论的大小
    x_train = preprocessing.sequence.pad_sequences(x_train, maxlen=maxlen)
    x_test = preprocessing.sequence.pad_sequences(x_test, maxlen=maxlen)

    print(x_train)


    """训练"""
    from keras.models import Sequential
    from keras.layers import Flatten, Dense

    model = Sequential()
    # W们将最大输入长度指定给我们的“嵌入”层，以便以后可以平整嵌入的输入
    """网络将对每个词都学习一个 8维嵌入"""
    model.add(Embedding(10000, 8, input_length=maxlen))
    # 在嵌入层之后，我们的激活形状为（（samples，maxlen，8）`。我们将嵌入的3D张量展平为形状为`（samples，maxlen 8）`的2D张量
    model.add(Flatten())

    # 我们在顶部添加分类器
    model.add(Dense(1, activation='sigmoid'))
    model.compile(optimizer='rmsprop', loss='binary_crossentropy', metrics=['acc'])
    model.summary()


    history = model.fit(x_train, y_train,epochs=10,batch_size=32,validation_split=0.2)
embedding()