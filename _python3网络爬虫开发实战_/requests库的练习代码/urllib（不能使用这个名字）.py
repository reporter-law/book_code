import urllib.request
from urllib.parse import urlparse
import http.cookiejar
url ="https://www.bilibili.com"
headers ={'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

cookie = http.cookiejar.CookieJar()
handle = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handle)
r =opener.open(url)
for item in cookie:
	print(item.name + '=' +item.value)
#url = request.Request(url = url, headers=headers)
#r = request.urlopen(url)
content = urlparse(url)
print(type(content), content)
#一次请求：request.Request(url, data, method,header)——request.urlopen()
#多次请求：ProxyHandler()/http.cookiejar.CookieJar(),
#opener=build_opener(proxyhandler/HTTPCOOKIEPROCESSOR()),opener.open(Request())
