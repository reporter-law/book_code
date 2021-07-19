# -*-  coding: utf-8 -*-
# Author: cao wang
# Datetime : 2020
# software: PyCharm
# 收获:
import locale,re
import os, warnings,sys
"""当前编码"""
print("默认编码：",locale.getpreferredencoding())
print("控制台编码：",sys.stdout.encoding)

import re
text = u'Français złoty Österreich'
pattern = r'\w+'
ascii_pattern = re.compile(pattern, re.ASCII)
unicode_pattern = re.compile(pattern)
print('Text  :', text)
print('Pattern :', pattern)
print('ASCII  :', list(ascii_pattern.findall(text)))
"""re.ASCII就是有些字符串不在里面"""
print('Unicode :', list(unicode_pattern.findall(text)))
