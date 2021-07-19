#coding:gbk
#������Ŀ����ӰƬ�ռ�
import requests
import re
import json
import time
from requests.exceptions import RequestException
from tqdm import tqdm


'''url���� http://20dyy.cn/index.php?m=vod-list-id-18-order--by-time-class-0-year-0-letter--area--lang-.html
http://20dyy.cn/index.php?m=vod-list-id-18-pg-2-order--by-time-class-0-year-0-letter--area--lang-.html
������pg-����'''

#��һ����ҳ��#return movie_list #ǰ��һ���ո�
def open_url(url):
	try:
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
		r = requests.get(url,headers=headers)
		if r.status_code == 200:
			return r.text
		else:
			return None
	except RequestException:
		return None


#�������ݳ�ȡ�������ֺ�����Ϊ��
def parse_one_page(html):
	pattern = re.compile(r'<div class="v-pic">.*?title=\"(.*?)\".*?>��Ա��<a.*?>(.*?)</a>', re.S)
	#����ԭ���е�û����Ա����,�����ǰ��
	items = re.findall(pattern,html)#findall ���ֵ����ֵ�
	dics = []
	for item  in items:
		dic = {'title' : item[0], 'role' : item[1]}
		dics.append(dic)
	return dics
	#����return,��Ϊͨ����ֵ����
#�˺���û�з���ֵ,returnҲֻ�����һ��

def write_to_file(content):
	with open('movie_list.txt', 'a', encoding ='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False) + '\t')
	#dump!=dumps,û��ensure_���´����ַ���������
	#д��֮ǰҪ���룬��ʾʱ��Ҳ�н���

#write_to_file(item)

def main(other_url):
	url = 'http://20dyy.cn/index.php?m=vod-list-id-18-pg-' + str(other_url)
	html = open_url(url)
	content = parse_one_page(html)
	write_to_file(content)

if __name__ == '__main__':
	for other_url in tqdm(range(50)):
		main(other_url)
		time.sleep(0.1)


#��ַ�����������Ժ���     unbound localerror
'''status_code = []
def require():
	for url_1 in url():
		headers =
		r = requests.get(url_1,headers = headers)
		status_code.append(r.status_code)
	return status_code
require()

		
#print(r.content)
#with open('sss','wb') as f:
	#f.write(r.content)
	#f.close()
	
	
#url���ݽ���Ƭ������
movie_name = []
def decoding():
	for url_1 in url():
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
		r = requests.get(url_1,headers = headers)
		content = BeautifulSoup(r.text,'lxml')
		for movie in content.findAll('div',attrs={'class' : 'v-txt'}):
#print(movie)#��Ҫ�������������֣�����ֻ�����������һ������
#div�У�����p��û�У��Ƿ���Ҫ��εݽ�____����Ҫ��ֻ����Ҫ�Ķ�������Ҫ�ٴ�findAll
			for one in movie:
				a = movie.a.get('title')
			movie_name.append(a.strip())
	return movie_name

#���ڵ����� 
#Ϊʲô���У�����ֱ��.p���룬�ƺ����ڶ�λ������
#movie_name.append(a.strip())����aͬ�������ͻ��ظ����Σ�ͬ�������µõ�ѭ����Ķ���������������?
#������δ�������Ҫѭ���Ķ�����Ҫ��ѭ��ͬ��������Ѱ�ң��������ݻᰴ��ѭ���Ĵ�������ظ�
#return ��break ����˼
ֻ��һ�����֣���Ϊ���һ�����Ӻ���ǰ����֮ǰ�����б����õ�����һ�����ݣ�������ֻ��һ����print(a.strip())'''
'''
print(r.encoding)
print(r.text)#text ��content һ����ֻ��ǰ���ַ����Ѿ������
print(r.content)
print(r.json())
print(r.headers)
print(r.cookies)
print(r.url)


'''
'''
#Ƭ���洢
def warehouse():
	wb = xlwt.Workbook(encoding='ascii')
	ws = wb.add_sheet('movie�б�',cell_overwrite_ok=True)
	while decoding():
		b = 0
		ws.write(0, b,decoding().pop())
		b += 1
	wb.save('����Excel.xls')
	print('����Excel.xls-�ɹ�')
warehouse()
'''
#���⣺�ڲ�û�ж�b ��ֵ��unboundlocalerror,�ڲ�bû�и�ֵ�����Ǽ��ˣ����ǲ��ӻ����ڲ��и�

