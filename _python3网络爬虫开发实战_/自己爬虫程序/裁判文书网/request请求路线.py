# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import requests
url = 'http://wenshu.court.gov.cn/website/wenshu/181107ANFZ0BXSK4/index.html?docId=b50177f2afdf459d9579ab8a011641a3 HTTP/1.1'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
           #'cookies':'Cookie wzws_cid=86ec2bea4164ad2aeabc345d70569bea079b53d1d91189f1975ae50d6f4d8e5797937422de45f5c2f8936e613a320c976aa0030c6724cb7d243403c633f72fc3c7aae09c9dda493bbed2ab3bd9380d7a for wenshu.court.gov.cn'
           'Cookie': 'wzws_cid=c6b87ccf2a20dfa6cd3fbb129d8f94067e26ac64cb6bd49dbec486e761f343aa615b29fb227493b4b2bfba53dc04b7eb86284f2d579014b72663889ecffc864039f6b4dfb6d8aa248c98a880b9cd19e4 for wenshu.court.gov.cn'}
params = {
    's8': '02',
    'pageId': 0.5817147490503494,
    'sortFields': 's50:desc',
    'ciphertext': '1110110 110100 1110101 1001011 1111010 1100110 1100111 1100010 1001111 1100001 1010100 1000100 1001000 1100001 111000 1110100 1011000 1101011 1110010 111001 1000111 1101100 1101110 1001001 110010 110000 110010 110000 110000 110011 110011 110000 1110000 1110101 1101010 1111000 1010100 110000 1100100 1111001 1001011 1010101 1010000 1110100 111000 1001100 1000100 1000100 1111010 1010100 110111 1101110 1010100 1100111 111101 111101',
    'pageNum': 1,
    'queryCondition': [{"key":"s8","value":"02"}],
    'cfg': 'com.lawyee.judge.dc.parse.dto.SearchDataDsoDTO@queryDoc',
    '__RequestVerificationToken': 'Ml6Q3ehlzvtGt8eigXP1hnEj',
}

r= requests.post(url = url,headers = headers,params = params)
r.encoding = r.apparent_encoding
print(r.status_code)
print(r.encoding)
print(r.cookies)
print(r.text)