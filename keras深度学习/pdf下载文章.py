# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os

def nlp_download(url):

    path = os.path.dirname(__file__)
    file=path+"\keras_gru.pdf"
    os.system(f'wkhtmltopdf {url} {file}')
    print("下载完成")
url = "https://blog.csdn.net/a321123b/article/details/115719305?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522162013638116780366580397%2522%252C%2522scm%2522%253A%252220140713.130102334.pc%255Fblog.%2522%257D&request_id=162013638116780366580397&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~blog~first_rank_v2~times_rank-1-115719305.nonecase&utm_term=GRU+re&spm=1018.2226.3001.4450"
nlp_download(url)

