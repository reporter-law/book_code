"""程序说明"""
# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(min_df=0,lowercase=False)
word = ["I like you","he likes her"]
vec.fit(word)
print(vec.vocabulary_)
print(vec.transform(word).toarray())