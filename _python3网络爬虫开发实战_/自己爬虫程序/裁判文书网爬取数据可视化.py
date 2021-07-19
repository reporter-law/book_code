#coding:gbk
#网页进入调取
import requests
from bs4  import BeautifulSoup
import lxml
import json
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS  


#调用api
url = ''
#https:通配符；s.taobao.com：服务器地址；后面为根目录、子目录、内容
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
#Mozilla/5.0 - 浏览器标识符，Windows; U; Windows NT 6.1;- 系统平台，Gecko/20091201：渲染器；Firefox/3.5.6'：浏览器版本号
data = {'project':'python'}
#data里面可以增加表单数据，即请求返回数据类型，包括表明内容以及返回内容：用户身份、返回内容、返回编码方式、返回自然语言等等
r = requests.get(url,params = data,headers = headers)
print('Status code: ', r.status_code)

#处理文章信息
'''
content = r.content
catalogue = []
for box in soup.findAll('div',attrs={'class' : 'box'}):

	for a in box.findAll('a'):
		href = a.get('href')#get()意思通过键找到值
		catalogue.append(href)
#print(catalogue)
title_big = []
for mulu in soup.findAll('div',attrs={'class':'mulu-title'}):
		#传入的是实参，不能是变量
	title_big = mulu.h2.string
	#print(title_big)
	catalogue.append({'mulu_title':title_big, 'mulu': list})
	
f = '网页内容1.json'
with open(f,'w') as fp:
	json.dump(catalogue, fp)
all_messages = []
for value in catalogue[:30]:
	url = value
	setion_content = requests.get(url)
	#print('Status code : ',setion_content.status_code)
	#print(setion_content)#继续lxml解析
	
	setion_content_json = setion_content.json()
	print(setion_content_json)
	content = setion_content.content
	soup = BeautifulSoup(content, 'lxml')
	
	#读者评论：
	comments = []
	
	for box in soup.findAll('li',attrs={'class':'msgarticle'}):
		不用div开始也可以，只要是标签即可
		print(box)
		a = box.text
		comments.append(len(a))
	comments = sum(comments)
	#print(sum(comments))#sum求和可行
	#print(comments)
		#a = box.string
		#print(a)
		
	for box in soup.findAll('title'):#div是划分层级的，即attrs不必都有
		all_message = {'title':box.text, 'comments':comments}
	all_messages.append(all_message)
#print(all_messages)#all_messages若在循环内无法append增加上，需要将all_messages提前！
submission_dicts = sorted(all_messages, key = itemgetter('comments'),
	#reverse = True)
	#keyword 指向排序的起始点，true\false指向从大到小还是从小到大。
#print(submission_dicts)
names,article_comments = [],[]
for submission_dict in submission_dicts:
	#print(submission_dict)
	#print('\nTitle: ',submission_dict['title'])#错误在all_messages['tltle'] 变量错误！！！！！！
	#print('comments:',submission_dict['comments'])#错误在all_messages['comments']
	#names.append(submission_dict['title'])
	#article_comments.append(submission_dict['comments'])	

#可视化
my_style =LS('#339999',base_style = LCS)#base 而不是bace
my_config = pygal.Config()
my_config.show_y_guides = False
my_config.width = 1000
my_config.truncate_label = 10#直接赋值需要附在括号内pygal.Config(truncate_label = 5)
chart = pygal.Bar(my_config,style = my_style,x_label_rotation = 45)
#show_legend似乎是标签

chart.title = '盗墓笔记评论数分析——前30章'
chart.x_labels = names

chart.add('',article_comments)
chart.render_to_file('python_article1.svg')#注意不能直接呈现图形而是导出了！！
'''
