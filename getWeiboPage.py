# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib2
import urllib
import sys
import time
import random
 


class getWeiboPage:
	

	body = {
		'ajwvr':'6',
		'domain':'100505',
		'topnav':'1',
		'wvr':'6',
		'pre_page':'0',
		'page':1,
		'max_id':'',
		'end_id':'3913592300339412',
		'pagebar':'',
		'filtered_min_id':'',
		'pl_name':'Pl_Official_MyProfileFeed__22',
		'id':'1005051950964011',
		'script_uri':'/1950964011/profile',
		'feed_type':'0',
		'domain_op':'100505',
		'__rnd':'',
	}
	uid_list = [];
	charset = 'utf8'

	def get_msg(self,uid):
		getWeiboPage.body['uid'] = uid
		url = self.get_url(uid)
		self.get_firstPage(url)  
		self.get_secondPage(url)  
		self.get_thirdPage(url)

	def get_firstPage(self,url):
		getWeiboPage.body['pre_page'] = getWeiboPage.body['page'] - 1
		url = url + urllib.urlencode(getWeiboPage.body)
		req = urllib2.Request(url)
		result = urllib2.urlopen(req)
		text = result.read().decode('utf-8')
		print "第一页"
		print text
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\text1',text)
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\result1.txt',eval("u'''" + text + "'''"))

	def get_secondPage(self,url):
		getWeiboPage.body['count'] = '15'
		getWeiboPage.body['pagebar'] = '0'
		getWeiboPage.body['pre_page'] = getWeiboPage.body['page']
		getWeiboPage.body['__rnd'] = str(int(time.time())) + str(int(random.uniform(500,1000)))

		urlAjax = 'http://weibo.com/p/aj/v6/mblog/mbloglist?'
		urlAjax = urlAjax + urllib.urlencode(getWeiboPage.body)
		# print 'theSecond'
		# print urlAjax
		req = urllib2.Request(urlAjax)
		result = urllib2.urlopen(urlAjax)
		text = result.read().decode('utf-8')
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\text2',text)
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\result2.txt',eval("u'''"+text+"'''"))

	def get_thirdPage(self,url):
		getWeiboPage.body['count'] = '15'
		getWeiboPage.body['pagebar'] = '1'
		getWeiboPage.body['pre_page'] = getWeiboPage.body['page']
		getWeiboPage.body['__rnd'] = str(int(time.time())) + str(int(random.uniform(500,1000)))

		urlAjax = 'http://weibo.com/p/aj/v6/mblog/mbloglist?'
		urlAjax = urlAjax + urllib.urlencode(getWeiboPage.body)
		# print 'theSecond'
		# print urlAjax
		req = urllib2.Request(urlAjax)
		result = urllib2.urlopen(urlAjax)
		text = result.read().decode('utf8')
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\text3',text)
		self.writefile('C:\Users\Administrator\Desktop\py\8_weiBo\output\\result3.txt',eval("u'''"+text+"'''"))
	def get_url(self,uid):
		# url = 'http://weibo.com/u/' + uid + '?is_search=0&visible=0&is_tag=0&profile_ftype=1&page=2#feedtop'
		url = 'http://m.weibo.cn/u/' + uid
		return url
	def get_uid(self,filename):
		fread = file(filename)
		for line in fread:
			getWeiboPage.uid_list.append(line)
			print line
			time.sleep(1)

	def writefile(self,filename,content):
		fw = open(filename,'w+')
		fw.writelines(content)
		fw.close()

