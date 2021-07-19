#coding:gbk
import re

pattern = "\b[358]\d{1}"   #格式：开头标志\b内容标志次数标志\b结尾
phoneStr = "18230092223"
 
result = re.findall(pattern, phoneStr)
print(result)


