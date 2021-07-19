import requests
import django

url = 'https://www.cnki.net/'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
r = requests.get(url,headers = headers)
print('Status code :',r.status_code)
