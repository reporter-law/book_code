#coding:gbk
import re

pattern = "\b[358]\d{1}"   #��ʽ����ͷ��־\b���ݱ�־������־\b��β
phoneStr = "18230092223"
 
result = re.findall(pattern, phoneStr)
print(result)


