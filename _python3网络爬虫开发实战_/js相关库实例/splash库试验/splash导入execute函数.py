# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
import requests
from urllib.parse import quote

lua = '''
function main(splash)
  assert(splash:go('http://wenshu.court.gov.cn'))
  input_=splash:select('input[placeholder="输入案由、关键词、法院、当事人、律师"]')
  input_:send_text('刑事')
  splash:wait(3)
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
  }
end
'''
url = 'http://192.168.99.100:8050/execute?lua_source=' + quote(lua)
r = requests.get(url)
print(r.text)
#失败！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！！
'''百度成功，360成功但是不能mouse_click()'''