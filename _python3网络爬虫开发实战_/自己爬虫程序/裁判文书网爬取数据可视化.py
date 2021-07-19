#coding:gbk
#��ҳ�����ȡ
import requests
from bs4  import BeautifulSoup
import lxml
import json
from operator import itemgetter
import pygal
from pygal.style import LightColorizedStyle as LCS, LightenStyle as LS  


#����api
url = ''
#https:ͨ�����s.taobao.com����������ַ������Ϊ��Ŀ¼����Ŀ¼������
headers = {'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}
#Mozilla/5.0 - �������ʶ����Windows; U; Windows NT 6.1;- ϵͳƽ̨��Gecko/20091201����Ⱦ����Firefox/3.5.6'��������汾��
data = {'project':'python'}
#data����������ӱ����ݣ������󷵻��������ͣ��������������Լ��������ݣ��û���ݡ��������ݡ����ر��뷽ʽ��������Ȼ���Եȵ�
r = requests.get(url,params = data,headers = headers)
print('Status code: ', r.status_code)

#����������Ϣ
'''
content = r.content
catalogue = []
for box in soup.findAll('div',attrs={'class' : 'box'}):

	for a in box.findAll('a'):
		href = a.get('href')#get()��˼ͨ�����ҵ�ֵ
		catalogue.append(href)
#print(catalogue)
title_big = []
for mulu in soup.findAll('div',attrs={'class':'mulu-title'}):
		#�������ʵ�Σ������Ǳ���
	title_big = mulu.h2.string
	#print(title_big)
	catalogue.append({'mulu_title':title_big, 'mulu': list})
	
f = '��ҳ����1.json'
with open(f,'w') as fp:
	json.dump(catalogue, fp)
all_messages = []
for value in catalogue[:30]:
	url = value
	setion_content = requests.get(url)
	#print('Status code : ',setion_content.status_code)
	#print(setion_content)#����lxml����
	
	setion_content_json = setion_content.json()
	print(setion_content_json)
	content = setion_content.content
	soup = BeautifulSoup(content, 'lxml')
	
	#�������ۣ�
	comments = []
	
	for box in soup.findAll('li',attrs={'class':'msgarticle'}):
		����div��ʼҲ���ԣ�ֻҪ�Ǳ�ǩ����
		print(box)
		a = box.text
		comments.append(len(a))
	comments = sum(comments)
	#print(sum(comments))#sum��Ϳ���
	#print(comments)
		#a = box.string
		#print(a)
		
	for box in soup.findAll('title'):#div�ǻ��ֲ㼶�ģ���attrs���ض���
		all_message = {'title':box.text, 'comments':comments}
	all_messages.append(all_message)
#print(all_messages)#all_messages����ѭ�����޷�append�����ϣ���Ҫ��all_messages��ǰ��
submission_dicts = sorted(all_messages, key = itemgetter('comments'),
	#reverse = True)
	#keyword ָ���������ʼ�㣬true\falseָ��Ӵ�С���Ǵ�С����
#print(submission_dicts)
names,article_comments = [],[]
for submission_dict in submission_dicts:
	#print(submission_dict)
	#print('\nTitle: ',submission_dict['title'])#������all_messages['tltle'] �������󣡣���������
	#print('comments:',submission_dict['comments'])#������all_messages['comments']
	#names.append(submission_dict['title'])
	#article_comments.append(submission_dict['comments'])	

#���ӻ�
my_style =LS('#339999',base_style = LCS)#base ������bace
my_config = pygal.Config()
my_config.show_y_guides = False
my_config.width = 1000
my_config.truncate_label = 10#ֱ�Ӹ�ֵ��Ҫ����������pygal.Config(truncate_label = 5)
chart = pygal.Bar(my_config,style = my_style,x_label_rotation = 45)
#show_legend�ƺ��Ǳ�ǩ

chart.title = '��Ĺ�ʼ���������������ǰ30��'
chart.x_labels = names

chart.add('',article_comments)
chart.render_to_file('python_article1.svg')#ע�ⲻ��ֱ�ӳ���ͼ�ζ��ǵ����ˣ���
'''
