# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import os, warnings,csv,pprint
warnings.filterwarnings("ignore")
from tqdm import tqdm
def read_csv():
    origin = r"C:\Users\lenovo\Desktop\古诗语料库"
    for i in tqdm(os.listdir(origin)):
        path = os.path.join(origin,i)
        csv.field_size_limit(500 * 1024 * 1024)
        csvfile = open(path, 'r', encoding="utf-8")
        readers = csv.DictReader(csvfile)
        for row in readers:
            with open(origin+"\\古诗.txt","a+",encoding="utf-8")as f1:
                #print(dict(row)['内容'])
                try:
                    f1.write(dict(row)['内容']+"\n")
                except:
                    pass


def reads_csv():
    origin = r"C:\Users\lenovo\Desktop\古诗语料库\唐.csv"
    csv.field_size_limit(500 * 1024 * 1024)
    csvfile = open(origin, 'r', encoding="utf-8")
    readers = csv.DictReader(csvfile)
    for row in readers:
        with open(os.path.dirname(origin) + "\\唐诗.txt", "a+", encoding="utf-8")as f1:
            # print(dict(row)['内容'])
            try:
                f1.write(dict(row)['内容'] + "\n")
            except:
                pass



reads_csv()

