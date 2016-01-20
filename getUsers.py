# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
import sys
from time import sleep , ctime
import random
import lxml.html as HTML
import re
import HTMLParser
from time import sleep,ctime
import random
import cookielib
import threading
from threading import Thread
from Queue import Queue
from time import sleep


def getUsers(filename,urlId,maxPageNum,cookie):
	
	pageNum = 1
	user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
	proxyFile = open('F:\py\\available.txt','r')
	proxyList = []

	f = filename
	
	while True:
		line = proxyFile.readline()
		if line:
			pass
			proxy = line.strip()
			
			proxyList.append({
				"proxy":proxy
				})
		else:
			break
	
	
	proxyCount = 0	



	while True:
		print 'pageNum:',pageNum
		pageNum = getPage(urlId,pageNum,f,proxyList[proxyCount],cookie)
		if pageNum > maxPageNum:
			break
		
		pageNum += 1
		proxyCount +=1
		if proxyCount >= len(proxyList)-1:
			proxyCount = 0
		sleep(0.5)

	proxyFile.close()

def getPage(urlId,pageNum,f,theProxy,cookie):
	# cj = cookielib.CookieJar()
	# print cookie
	cookie_support = urllib2.HTTPCookieProcessor(cookie)
	ip = theProxy['proxy']
	print "ip:",ip
	try:
		proxy_handler = urllib2.ProxyHandler({'HTTP':ip})

		opener = urllib2.build_opener(proxy_handler,cookie_support,urllib2.HTTPHandler)
		loginUrl = 'http://weibo.com/p/' + str(urlId) + '/like?page='+ str(pageNum) +'#Pl_Core_F4RightUserList__47'
		print loginUrl
		user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:36.0) Gecko/20100101 Firefox/36.0'
		opener.addheaders = [('User_agent',user_agent)]

		result = opener.open(loginUrl)
		
		content = HTML.fromstring(result.read()).xpath('//script/text()')
	
		for i in content:
			
			if '"domid":"Pl_Core_F4RightUserList__47"' in i:
				pattern = re.compile(r',"html":"(.*?)"\}\)')
				i = pattern.search(i).group(1)
				blank_line = re.compile(' +')#去掉多余的空行
				htmlContent = blank_line.sub(' ',i)
				htmlContent = htmlContent.replace('\\n',"").replace('\\t',"").replace('\\r',"").replace("\\", "")
				
				
				personalInfo = HTML.fromstring(htmlContent).xpath('//dl[@class = "clearfix"]')#找到微博人
				for r in personalInfo:
					img = r.xpath('./dt[@class = "mod_pic"]/a/img/@src')[0]
					name = r.xpath('./dt[@class = "mod_pic"]/a/img/@alt')[0]
					location = r.xpath('./dd[@class = "mod_info S_line1"]/div[@class = "info_add"]/span/text()')[0]
					sex = r.xpath('./dd[@class = "mod_info S_line1"]/div[@class = "info_name W_fb W_f14"]/a[not(@target)]/i[@class][not(@title)]/@class')[0]
					
					print img,name,location,sex
					f.write('headImg@@@%s=name@@@%s=location@@@%s=sex@@@%s\n' % (
						img.encode('utf-8'),
						name.encode('utf-8'),
						location.encode('utf-8'),
						sex.encode('utf-8')))
		return pageNum
		

	except urllib2.URLError as e:
		print e.reason
		return pageNum - 1
		



