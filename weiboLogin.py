# !/usr/bin/python
# coding=utf-8

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import urllib
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs
import time
import re
import base64
import rsa
import binascii
import re
import json
import copy
import soupForCommonInfo
import getWeiboPage
import HTMLParser
import types
import getUsers

def PostEncode(userName,passWord,serverTime,nonce,pubkey,rsakv):
	encodedUserName = GetUserName(userName) # 64位加密用户名
	encodedPassWord = get_pwd(passWord,serverTime,nonce,pubkey)

	postPara = {
		'entry':'weibo',
		'gateway': '1',
		'from': '',
		'savestate': '7',
		'userticket':'1',
		'ssosimplelogin': '1',
		'vsnf':'1',
		'vsnval':'',
		'su': encodedUserName,
		'service':'miniblog',
		'servertime':serverTime,
		'nonce':nonce,
		'pwencode':'rsa2',
		'sp':encodedPassWord, 
		'encoding':'UTF-8', 
		'prelt': '115', 
		'rsakv':rsakv, 
		'url':'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack', 'returntype':'META'
	}
	postData = urllib.urlencode(postPara)
	return postData

def GetUserName(userName):
	userNameTemp = urllib.quote(userName)
	# print userName
	# print userNameTemp
	userNameEncoded = base64.encodestring(userNameTemp)[:-1]
	# print base64.encodestring(userNameTemp)
	# print userNameEncoded
	return userNameEncoded

def get_pwd(password,servertime,nonce,pubkey):
	rsaPublickey = int(pubkey,16)
	key = rsa.PublicKey(rsaPublickey,65537) #创建公钥
	message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)  #拼接明文js加密文件中得到
	passwd = rsa.encrypt(message,key)
	passwd = binascii.b2a_hex(passwd)
	return passwd

def sServerData(serverData):
	p = re.compile(r'\((.*)\)')
	jsonData = p.search(serverData).group(1)
	data = json.loads(jsonData)
	# print data
	serverTime = str(data['servertime'])
	# print "servertime:",serverTime
	nonce = data['nonce']
	# print "nonce:",nonce
	pubkey = data['pubkey']
	# print 'pubkey:',pubkey
	rsakv = data['rsakv']
	# print "rsakv:",rsakv

	return serverTime,nonce,pubkey,rsakv

def sRedirectData(text):
	p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')
	loginUrl = p.search(text).group(1)
	# print 'loginUrl:',loginUrl
	return loginUrl




class weiboLogin:
	def __init__(self,user,pwd,enableProxy = False):
		#enableProxy表示是否使用代理服务器，默认关闭
		print 'Initializing WeiboLogin'
		self.username = user
		self.password = pwd
		self.enableProxy = enableProxy
		# print "username:",user
		# print "password:",pwd
		
		self.serverUrl = "http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683"
		self.loginUrl = "http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.11)"
		self.postHeader = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; rv:24.0) Gecko/20100101 Firefox/24.0'}

	def GetServerTime(self):
		print "Getting server time and nonce..."
		# print self.serverUrl
		url = self.serverUrl
		svData = urllib2.urlopen(url).read()
		# print svData

		try:
			serverTime,nonce,pubkey,rsakv = sServerData(svData)
		
			return serverTime,nonce,pubkey,rsakv
		except:
			print 'Get server time & nonce error'
			return None

	def EnableCookie(self,enableProxy):
		cookieJar = cookielib.LWPCookieJar()
		cookie_support = urllib2.HTTPCookieProcessor(cookieJar)
		if enableProxy:
			proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})
			opener = urllib2.build_opener(proxy_support,cookie_support,urllib2.HTTPHandler)
			print 'proxy enabled'
		else:
			opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)

		urllib2.install_opener(opener)

		return cookieJar
		
		
	def Login(self,enableProxy = False):
		cookieJar = cookielib.LWPCookieJar()
		cookie_support = urllib2.HTTPCookieProcessor(cookieJar)
		if enableProxy:
			proxy_support = urllib2.ProxyHandler({'http':'http://xxxxx.pac'})
			opener = urllib2.build_opener(proxy_support,cookie_support,urllib2.HTTPHandler)
			print 'proxy enabled'
		else:
			opener = urllib2.build_opener(cookie_support,urllib2.HTTPHandler)

		urllib2.install_opener(opener)

		# self.EnableCookie(self.enableProxy)
		serverTime,nonce,pubkey,rsakv = self.GetServerTime()
		postData = PostEncode(self.username,self.password,serverTime,nonce,pubkey,rsakv)
		# print 'Post data length:\n',len(postData


		req = urllib2.Request(self.loginUrl,postData,self.postHeader)
		result = urllib2.urlopen(req)
		text = result.read()

		try:
			loginUrl = sRedirectData(text)  #解析重定位结果
			urllib2.urlopen(loginUrl)
		except:
			print 'Login error!'
			return False

		print 'Login sucess!'
		# print cookieJar


		return {"cookie":cookieJar}


idGroup = ['10151501_2269313','10151501_1236630','10151501_56575459','10151501_2860765','10151501_2850248','10151501_770940'];

if __name__ == '__main__':
	aaaa = weiboLogin('xxxxxxxxxxxxxxxxxxx','xxxxxxxxxxxxxxxxxx',False)
	if aaaa.Login()['cookie']:
		for i in range(0,len(idGroup)-1):
			print '打开',idGroup[i]
			print '===================================================='
			print '===================================================='
			print '===================================================='
			print '===================================================='
			f = open('C:\Users\Administrator\Desktop\ouput\\'+ str(i) +'.txt','w+')
			getUsers.getUsers(f,idGroup[i],2000,aaaa.Login()['cookie'])
			print '===================================================='
			print '===================================================='
			print '===================================================='
			print '===================================================='
			print '===================================================='
			f.close()
			print '关闭',idGroup[i]
