# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer

vector1 = "The faster Harry got to the store, the faster and faster Harry would get home."
vector2 = "Jill is faster than Harry."
vector3 = "Jill and Harry fast."
corpus = [vector1, vector2, vector3]
vectorizer = TfidfVectorizer(min_df=1)
model = vectorizer.fit_transform(corpus)
print(model)
print(model.todense().round(2))
