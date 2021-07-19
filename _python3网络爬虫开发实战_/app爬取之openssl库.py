# -*-  coding: utf-8 -*-
# Author: caowang
# Datetime : 2020
# software: PyCharm
from OpenSSL import crypto



cert_file = 'F:\新建文件夹\mitmproxy-ca-cert.pem'
cert = crypto.load_certificate(crypto.FILETYPE_PEM, open(cert_file).read())

subject = cert.get_subject()
certIssue = cert.get_issuer()

issued_to = subject.CN
print(issued_to)
'''颁发机构'''
issuer = cert.get_issuer()
print(issuer)
issued_by = issuer.CN
print(issued_by)
'''返回hash值'''
hash = cert.subject_name_hash()
#hash_ = X509Name.hash()
print(hash)
