# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
import requests
from pyquery import PyQuery

url = 'http://quotes.toscrape.com'
doc = PyQuery(url = url)
a = doc('.text::text').extract_first()
'''raise ExpressionError('Pseudo-elements are not supported.')
cssselect.xpath.ExpressionError: Pseudo-elements are not supported.'''