# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings,sys,re,random
import numpy as np
warnings.filterwarnings("ignore")
os.environ["KERAS_BACKEND"] = "plaidml.keras.backend"
from keras.models import load_model
print("Using loaded model to predict...")
model = load_model("J:\PyCharm项目\学习书籍成果\keras深度学习\model\lstm_word_shici2.h5")

path = r"C:\Users\lenovo\Desktop\古诗语料库\3390.txt"
text = open(path).read().replace("“","").replace("《","").replace("”","").replace("》","").replace("丨","")
text = "".join(re.findall(r'[\u3002\uff1b\uff0c\uff1a\u201c\u201d\uff08\uff09\u3001\uff1f\u300a\u300b\u4e00-\u9fa5]', text))
print('Corpus length:', len(text))
"""文本向量化处理"""
# 提取字符序列的长度
"""分为长度为60个字的句子"""
maxlen = 24
# 我们每个`step`字符都采样一个新序列,
"""隔开三个字为一个句子，会存在重复！！！！！"""
step = 2
# 这保存了我们提取的序列
sentences = []
# 保留目标（后续角色）
next_chars = []
for i in range(0, len(text) - maxlen, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i + maxlen])
print('Number of sequences:', len(sentences))

# 语料库中的唯一字符列表
"""去掉重复的字"""
chars = sorted(list(set(text)))
"""每个字及每个字的索引的字典"""
char_indices = dict((char, chars.index(char)) for char in chars)
print(char_indices)

generated_text = "佳人"
#print('--- 初始文本: "' + generated_text + '"')
# 随机选择一个文本种子
start_index = random.randint(0, len(text) - maxlen - 1)
generated_text = text[start_index: start_index + maxlen]
print('--- 初始文本: "' + generated_text + '"')
generated_text = "佳人"



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
for temperature in [ 1.0]:
    #print('------ 初始随机:', temperature)
    sys.stdout.write("元日")##屏幕显示

        # 我们生成400个字符
    for i in range(50):
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
