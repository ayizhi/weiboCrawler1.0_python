# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
import lxml.html as HTML
import re


def getIp(maxPage):
    pageNum = 0
    f = open('F:\py\\proxyList1.txt',"w")

    while True:
        pageNum += 1
        if pageNum>maxPage:
            break
        getPage(pageNum,f)
        
def getPage(pageNum,f):
    print "pageNum:",pageNum
    loginUrl = 'http://www.xicidaili.com/nn/' + str(pageNum)
    postData = urllib.urlencode({})
    postHeader = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
    req = urllib2.Request(loginUrl)
    req.add_header('User-Agent',postHeader)
    result = urllib2.urlopen(req).read()
    allId = HTML.fromstring(result).xpath('//tr[@class="odd"]')
    for i in allId:
        tds = i.xpath('./td')
        port = tds[3].xpath('text()')[0]
        ip = tds[2].xpath('text()')[0]
        protocol = tds[6].xpath('text()')[0]

        # print port,ip,protocol
        f.write('%s=%s:%s\n' % (protocol,ip,port))
        

getIp(364)