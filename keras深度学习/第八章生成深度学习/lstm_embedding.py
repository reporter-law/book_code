# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings

warnings.filterwarnings("ignore")
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os,re
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
from keras.preprocessing import sequence

#path = keras.utils.get_file('nietzsche.txt',origin='https://s3.amazonaws.com/text-datasets/nietzsche.txt')
path = r"C:\Users\lenovo\Desktop\古诗语料库\唐诗.txt"
text = open(path,encoding="utf-8").read().replace("“","").replace("《","").replace("”","").replace("》","").replace("丨","")
text = "".join(re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', text))[:10000]
text = list(text)
maxlen = 2
print('Corpus length:', len(text))
tokenizer = Tokenizer(num_words=6000000)
tokenizer.fit_on_texts(text)
"""就是用索引表示当前句子结构"""
print(tokenizer.index_word)
x = tokenizer.texts_to_matrix(text)
print(x)
y = tokenizer.texts_to_sequences(text[1:])
x = sequence.pad_sequences(x,maxlen=maxlen)
y = sequence.pad_sequences(y,maxlen=maxlen)
print(x)
print(y.shape[0])
"""网络"""
from keras import layers
from keras.models import Sequential
#z#再训练
#model = load_model('J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici.h5')
model = Sequential()#双向rnn、
model.add(layers.Conv1D(32,1,activation='relu',input_shape=x.shape))
model.add(layers.MaxPooling1D(1))
model.add(Dropout(0.4))
model.add(layers.Bidirectional(layers.LSTM(256,recurrent_initializer='glorot_uniform')))
model.add(Dropout(0.1))#两层以上lstm需要return_sequences=True
model.add(layers.Dense(y.shape[0], activation='softmax'))
optimizer = keras.optimizers.Adam(lr=0.001)
#callbacks_list = [keras.callbacks.EarlyStopping(monitor='val_loss', patience=1,), keras.callbacks.ModelCheckpoint(filepath=f'J:\PyCharm项目\学习进行中\keras深度学习\model\lstm_word_诗词2.h5', monitor='val_loss',mode='max', save_best_only=True)]
model.compile(loss='categorical_crossentropy', optimizer=optimizer)
model.fit(x, y,batch_size=2048,epochs=250)#必须加上这一句callbacks=callbacks_list
model.save("J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici2.h5")
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
test_data = "中华人民共和国国务院总理周恩来在外交部长陈毅的陪同下，连续访问了埃塞俄比亚等非洲10国以及阿尔巴尼亚"
    test_data = [i for i in test_data]
    tokenizer = Tokenizer(num_words=6000000)
    tokenizer.fit_on_texts(test_data)
    """就是用索引表示当前句子结构"""
    print(tokenizer.index_word)
    x = tokenizer.texts_to_matrix(text)
    print(x)
    y = tokenizer.texts_to_sequences(text[1:])
    x = sequence.pad_sequences(x, maxlen=maxlen)
    y = sequence.pad_sequences(y, maxlen=maxlen)
    print(x)