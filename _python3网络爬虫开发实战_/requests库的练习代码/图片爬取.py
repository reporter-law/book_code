#coding:gbk
import requests
url ='http://cn2.3days.cc/1583204789680889.jpeg'#'http://www.law-lib.com/cpws/cpwsml-cx.asp?bbdw=&pages=1&tm1=&tm2='#
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
r = requests.get(url,headers = headers)
print('Status code :',r.status_code)
print(r.content)
with open('sss.jpeg','wb') as f:
	f.write(r.content)
	f.close()
#z֮ǰ������������ʵս���������϶���pythonѧϰ����ļ�����
