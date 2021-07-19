# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os,re,warnings
warnings.filterwarnings("ignore")
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"

"""字符级神经语言模型，即生成下一个字,假设空间就在完全复制于完全随机之间"""

def reweight_distribution(origin_data,temprature=0.5):
    distribution = np.log(origin_data)/temprature
    distribution = np.exp(distribution)
    return  distribution/np.sum(distribution)

"""尼采作品"""
import keras
import numpy as np
from keras.models import load_model
from keras.layers import Dropout
from keras.preprocessing.text import Tokenizer
from keras.callbacks import ReduceLROnPlateau

path = r"C:\Users\lenovo\Desktop\古诗语料库\唐诗.txt"


#path = keras.utils.get_file('nietzsche.txt',origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
text = open(path, encoding="utf-8").read().replace("“", "").replace("《", "").replace("”", "").replace("》","").replace("丨", "")
#print(len(text)/9600)
chars = sorted(list(set(text)))
print(len(chars))
def data(chars):
    start = 0
    while 1:
        text = open(path, encoding="utf-8").read().replace("“", "").replace("《", "").replace("”", "").replace("》","").replace(
            "丨", "")[start:start+1200]
        # text = "".join(re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', text))
        #print('Corpus length:', len(text))
        """文本向量化处理"""
        # 提取字符序列的长度
        """分为长度为60个字的句子"""
        maxlen = 48
        # 我们每个`step`字符都采样一个新序列,
        """隔开三个字为一个句子，会存在重复！！！！！"""
        step = 3
        # 这保存了我们提取的序列
        sentences = []
        # 保留目标（后续角色）
        next_chars = []
        for i in range(0, len(text) - maxlen, step):
            sentences.append(text[i: i + maxlen])
            next_chars.append(text[i + maxlen])
        #print('Number of sequences:', len(sentences))

        # 语料库中的唯一字符列表
        """去掉重复的字"""
        #chars = sorted(list(set(text)))
        """这个是英文字母而不是单词"""
        #print('Unique characters:', len(chars))
        # 将唯一字符映射到其在chars中的索引的字典,
        """每个字及每个字的索引的字典"""
        char_indices = dict((char, chars.index(char)) for char in chars)
        #print(char_indices)

        # 接下来，将字符一键编码为二进制数组。
        """形成句子数量，句子最大长度，独特字符的三位数组,y为下一个字"""

        #print('Vectorization...')
        x = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
        y = np.zeros((len(sentences), len(chars)), dtype=np.bool)
        for i, sentence in enumerate(sentences):
            for t, char in enumerate(sentence):
                x[i, t, char_indices[char]] = 1.
            y[i, char_indices[next_chars[i]]] = 1.
        start+=1201
        #print(x,y)
        yield x,y

"""网络"""
from keras import layers
from keras.models import Sequential
#print(x.shape)
#z#再训练
"""
model = load_model('J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici.h5')
model.summary()
"""
model = Sequential()#双向rnn、
#print(x)
model.add(layers.Conv1D(4,12,input_shape=(48, 7720),activation='relu'))
model.add(layers.MaxPooling1D(1))
model.add(layers.Conv1D(4,6,input_shape=(48, 7720),activation='relu'))
model.add(layers.MaxPooling1D(1))
model.add(layers.Conv1D(4,1,input_shape=(48, 7720),activation='relu'))
model.add(layers.MaxPooling1D(1))
#model.add(layers.Bidirectional(layers.LSTM(48,recurrent_initializer='glorot_uniform',activation='relu')))#两层以上lstm需要return_sequences=True
model.add(layers.Flatten())
model.add(layers.Dense(7720, activation='softmax'))
#学习率
callbacks_list =[keras.callbacks.ModelCheckpoint(filepath=f'J:\PyCharm项目\学习进行中\keras深度学习\model\lstm_tanshi.h5', monitor='loss',mode='auto', save_best_only=True),keras.callbacks.EarlyStopping(monitor='loss', patience=3, verbose=0, mode='auto')]

optimizer = keras.optimizers.RMSprop()
#模型保存
model.compile(loss='categorical_crossentropy', optimizer=optimizer,metrics=['accuracy'])

model.fit_generator(data(chars),steps_per_epoch=2400,epochs=100,callbacks=callbacks_list,verbose=1)#必须加上这一句callbacks=callbacks_list
model.save("J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shi6.h5")
"""加权函数：加权值为现有文本的字符概率，训练的权重为纯重复的权重，f
文本概率加权本质上也是随机只是更贴近文本的随机，即生成字母的权重等于重复概率进行加权"""
def sample(preds, temperature=1.0):
    #print("重复的概率为：",preds)
    preds = np.asarray(preds).astype('float64')#训练得到的概率浮点数化
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    #加权后
    #print("加权后的概率：",preds)
    probas = np.random.multinomial(1, preds, 1)#
    """–n : 从矩阵中取值次数；
–pvals：根据概率取值，这是一个数组，并且所有数据之和为1；
–size：输出的维度，默认为1，即1 x pvals"""
    """随机选择"""
    return np.argmax(probas)


"""文本生成"""
import random
import sys


# 随机选择一个文本种子
start_index = random.randint(0, len(text) - maxlen - 1)
generated_text = text[start_index: start_index + maxlen]
print('--- 初始文本: "' + generated_text + '"')

for temperature in [ 0.5, 1.0, 1.2]:
    print('------ 初始随机:', temperature)
    sys.stdout.write("元日")##屏幕显示

        # 我们生成400个字符
    for i in range(40):
        sampled = np.zeros((1, maxlen, len(chars)))
        for t, char in enumerate(generated_text):
            sampled[0, t, char_indices[char]] = 1.
        """将选择的文本向量化，之前是对训练的文本向量化，此时的text是原始的text"""
        preds = model.predict(sampled, verbose=0)[0]
        next_index = sample(preds, temperature)#以temperature作为随机性变量
        next_char = chars[next_index]

        generated_text += next_char
        generated_text = generated_text[1:]

        sys.stdout.write(next_char)
        sys.stdout.flush()
    print()
