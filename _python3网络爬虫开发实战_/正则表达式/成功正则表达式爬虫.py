#coding:gbk
#爬虫项目——影片收集
import requests
import re
import json
import time
from requests.exceptions import RequestException
from tqdm import tqdm


'''url分析 http://20dyy.cn/index.php?m=vod-list-id-18-order--by-time-class-0-year-0-letter--area--lang-.html
http://20dyy.cn/index.php?m=vod-list-id-18-pg-2-order--by-time-class-0-year-0-letter--area--lang-.html
增加了pg-数字'''

#第一个网页打开#return movie_list #前进一个空格
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


#函数内容抽取，以名字和评分为例
def parse_one_page(html):
	pattern = re.compile(r'<div class="v-pic">.*?title=\"(.*?)\".*?>演员：<a.*?>(.*?)</a>', re.S)
	#出错原因：有的没有演员名字,后面填补前面
	items = re.findall(pattern,html)#findall 出现的是字典
	dics = []
	for item  in items:
		dic = {'title' : item[0], 'role' : item[1]}
		dics.append(dic)
	return dics
	#不用return,因为通过赋值调用
#此函数没有返回值,return也只有最后一个

def write_to_file(content):
	with open('movie_list.txt', 'a', encoding ='utf-8') as f:
		f.write(json.dumps(content,ensure_ascii=False) + '\t')
	#dump!=dumps,没有ensure_导致存在字符而非中文
	#写入之前要解码，显示时候也有解码

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


#网址访问正常测试函数     unbound localerror
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
	
	
#url内容解码片名函数
movie_name = []
def decoding():
	for url_1 in url():
		headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
		r = requests.get(url_1,headers = headers)
		content = BeautifulSoup(r.text,'lxml')
		for movie in content.findAll('div',attrs={'class' : 'v-txt'}):
#print(movie)#需要遍历出单个名字，否则只能整块遍历出一个名字
#div有，但是p就没有，是否需要层次递进____不需要，只是想要的东西还需要再次findAll
			for one in movie:
				a = movie.a.get('title')
			movie_name.append(a.strip())
	return movie_name

#存在的问题 
#为什么不行？不能直接.p进入，似乎由于定位不明？
#movie_name.append(a.strip())放在a同样缩进就会重复六次？同样缩进下得到循环后的而不是整个函数的?
#问题暂未解决，想要循环的东西需要在循环同样缩进中寻找，否则内容会按照循环的次数多次重复
#return 有break 的意思
只有一个名字，且为最后一个？从后往前数？之前不进行遍历得到的是一块内容，遍历就只是一个了print(a.strip())'''
'''
print(r.encoding)
print(r.text)#text 与content 一样，只是前者字符串已经解码过
print(r.content)
print(r.json())
print(r.headers)
print(r.cookies)
print(r.url)


'''
'''
#片名存储
def warehouse():
	wb = xlwt.Workbook(encoding='ascii')
	ws = wb.add_sheet('movie列表',cell_overwrite_ok=True)
	while decoding():
		b = 0
		ws.write(0, b,decoding().pop())
		b += 1
	wb.save('测试Excel.xls')
	print('测试Excel.xls-成功')
warehouse()
'''
#问题：内部没有对b 赋值，unboundlocalerror,内部b没有赋值，但是加了，除非不加或者内部有赋

