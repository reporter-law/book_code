import requests
import re

#url = 'https://www.zhihu.com/explore'
#r = requests.get(url)
#print(r.text)
#文件上传
url = 'http://p2.qhimgs4.com/t0150aabb432c4c0517.jpg'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

r = requests.get(url,headers=headers)
print(r.status_code)
print(r.cookies)
for key,values in r.cookies.items():
    print('ok')
    print(key +'=' + values)

'''with open('cc.jpg', 'wb')as f:
	f.write(r.content)
	f.close()'''
#失败
'''files={'file':open('cc.jpg','wb')}
r = requests.post('https://httpbin.org/get',files = files)
print(r.text)'''

#cookie
headers = {'Cookie': '_qda_uuid=af1e94e2-f6ba-0f62-5a83-282336a11760;_csrfToken=fQ3O2kwzPnWEy3TmwhFWDV91Du6nzyhTugzPJxzF; newstatisticUUID=1583399655_985214042;e1=%7B%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A10%22%2C%22l1%22%3A1%7D;e2=%7B%22pid%22%3A%22qd_p_qidian%22%2C%22eid%22%3A%22qd_A08%22%2C%22l1%22%3A1%7D'
}
r = requests.get('https://qidian.com',headers = headers)
print(r.cookies)
for key,values in r.cookies.items():
    print('ok')
    print(key +'=' + values)



url = 'https://www.12306.cn'
r = requests.get(url,headers=headers)
print(r.status_code,r.cookies)

content = 'abc123456 .world'
result = re.match('^(\w+).*?$',content)    #需要全部匹配然后提取，提取内容在group()中
print(result)
print(result.group(1))
'''没有cookies'''


