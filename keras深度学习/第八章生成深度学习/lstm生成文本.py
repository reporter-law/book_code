"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os,re,warnings,time
warnings.filterwarnings("ignore")
"""字符级神经语言模型，即生成下一个字,假设空间就在完全复制于完全随机之间"""
def reweight_distribution(origin_data,temprature=0.5):
    distribution = np.log(origin_data)/temprature
    distribution = np.exp(distribution)
    return  distribution/np.sum(distribution)

import keras,time
import numpy as np
from keras.models import load_model
from keras.layers import Dropout
from keras.preprocessing.text import Tokenizer


#path = keras.utils.get_file('nietzsche.txt',origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
path = r"C:\Users\lenovo\Desktop\古诗语料库\唐诗.txt"
text = open(path,encoding="utf-8").read().replace("“","").replace("《","").replace("”","").replace("》","").replace("丨","")
texts = "".join(re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', text))
print('Corpus length:', len(text))
# 须加上这一句callbacks=callbacks_list
class Data_generate():
    def __init__(self,texts):
        self.texts = texts

    def data_generate(self):
        """分为长度为60个字的句子"""
        # 我们每个`step`字符都一个新序列,
        """隔开三个字为一个句子，会存在重复！！！！！"""
        count = 0
        batch_size = 10000
        while 1:
            text = self.texts[count * batch_size:(count + 1) * batch_size]
            maxlen = 42
            step = 2
            # 这保存了我们提取的序列
            sentences = []
            # 保留目标（后续角色）
            """去掉重复的字"""
            self.chars = sorted(list(set(text)))

            print(f"第{count}轮：")
            next_chars = []
            for i in range(0, len(text) - maxlen, step):
                sentences.append(text[i: i + maxlen])
                next_chars.append(text[i + maxlen])
            print('Number of sequences:', len(sentences))
            # 语料库中的唯一字符列表
            """这个是英文字母而不是单词"""
            print('Unique characters:', len(self.chars))
            # 将唯一字符映射到其在chars中的索引的字典,
            """每个字及每个字的索引的字典"""
            char_indices = dict((char, chars.index(char)) for char in self.chars)
            """形成句子数量，句子最大长度，独特字符的三位数组,y为下一个字"""
            print('Vectorization...')
            x = np.zeros((len(sentences), maxlen, len(self.chars)), dtype=np.bool)
            y = np.zeros((len(sentences), len(self.chars)), dtype=np.bool)
            for i, sentence in enumerate(sentences):
                for t, char in enumerate(sentence):
                    x[i, t, char_indices[char]] = 1
                y[i, char_indices[next_chars[i]]] = 1
            yield (x, y)
            count += 1
"""网络"""
from keras import layers
from keras.models import Sequential
# z#再训练

#model = load_model('J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shicipoem.h5')
#print(x.shape[2],y.shape)
model = Sequential()
# model.add(models)
# model.summary()
model.add(layers.InputLayer(input_shape=(42,1369)))
model.add(layers.Conv1D(8, 7, activation="relu"))
model.add(layers.Bidirectional(layers.LSTM(256, recurrent_initializer='glorot_uniform', return_sequences=True)))
model.add(layers.GRU(256, recurrent_initializer='glorot_uniform'))
model.add(layers.Dropout(0.1))
model.add(layers.Dense(1369, activation='softmax'))
# model.load_weights('J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici3.h5',by_name=True)
model.summary()
optimizer = keras.optimizers.Adam(lr=0.005)

callbacks_list = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=1, ), keras.callbacks.ModelCheckpoint(
        filepath=f'J:\PyCharm项目\学习进行中\keras深度学习\model\lstm_word_shici3.h5', monitor='val_loss', save_best_only=True)]
model.compile(loss='categorical_crossentropy', optimizer=optimizer)

"""
model.load_weights('J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici_weight.h5',by_name=True)#  File "C:\\Users\lenovo\AppData\Roaming\Python\Python37\site-packages\numpy\core\fromnumeric.py", line 58, in _wrapfunc,keras降级
model.trainable = True
"""

model.fit_generator(data_generate(texts), steps_per_epoch=6, epochs=1, verbose=1)
model.save("J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici3poem.h5")

#加权函数：加权值为现有文本的字符概率，训练的权重为纯重复的权重，f文本概率加权本质上也是随机只是更贴近文本的随机，即生成字母的权重等于重复概率进行加权"""
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

for temperature in [1.2,1.5,2.0,2.5]:
    print('------ 初始随机:', temperature)
    sys.stdout.write(f"{generated_text}")##屏幕显示

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