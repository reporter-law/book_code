# -*-  coding: utf-8 -*-
# Author: xxx
# Datetime : 2019/12/12 10:25
# software: PyCharm
# usage:
from mitmproxy import ctx
def request(flow):#request必须这样写
    url = 'https://baidu.com'
    flow.request.url = url#修改url导致手机访问的url改变

    request = flow.request
    info = ctx.log.info
    info(request.url)
    info(str(request.headers))
    info(str(request.cookies))
    info(request.host)
    info(request.method)
    info(str(request.port))
    info(request.scheme)
    #问题避免总是询问安全证书过期
    '''
    flow.request.headers['User-Agent'] = 'MitmProxy'
    ctx.log.info(str(flow.request.headers))
    #ctx.log.warn(str(flow.request.headers))
    ctx.log.error(str(flow.request.headers))
    '''


