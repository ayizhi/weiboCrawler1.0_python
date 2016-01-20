# !/usr/bin/python
# coding=utf-8

import sys
import urllib
import urllib2
import cookielib
from BeautifulSoup import BeautifulSoup as bs
import time
import re
import getWeiboPage
reload(sys)
sys.setdefaultencoding('utf-8')


def prase_html(html_data):
		soup = bs(html_data)
		# print "soup:",soup
		f = open('C:\Users\Administrator\Desktop\weiboHtmlData.txt','w+')
		f.writelines(str(soup))
		f.close()
		for x_str in soup.findAll('script'):
			x_str_split = str(x_str).split('{')[-1]

			if '"domid":"v6_pl_rightmod_myinfo"' in x_str_split and 'fans' in x_str_split:
				text = x_str_split.replace('\/','/')
				text_split = text.split('"html":')[-1].split('}')[0]

				text_split_l = text_split.replace('&lt;','<')

				text_split_001 = text_split_l.replace('&gt','>')

				tmp_html = bs(text_split_001).prettify()
				# print tmp_html
				three_url = [x.split("href=")[-1].split('"')[1].strip('\\') for x in re.findall('<a.*?href=.*?<\/a>',text_split_001)]
				# print three_url
				# print text_split
				# print "==============================================================================="
				# print "==============================================================================="
				# print "==============================================================================="
				# print "==============================================================================="
				data = bs(tmp_html)
				
				a_value_list = data.findAll("strong")
				
				a_label_list = data.findAll("span")
				

				three_value = [str(value.string).strip()[1:] for value in a_value_list]
				# print "three_value:",three_value
				three_label = [str(value.string).strip()[1:] for value in a_label_list]
				three_label = three_label[4:]
				# print "three_label:",three_label

				url_name = [name + 'url' for name in three_label]
				label_url = dict(zip(url_name,three_url))
				label_value = dict(zip(three_label,three_value))
			else:
				pass
			if '$CONFIG' in x_str_split:
				tag_string = x_str.string.replace('$CONFIG[',"")
				tag_list = [tag.strip().strip('\n') for tag in tag_string.replace(']', '').split(';')]
				tag_label = ['oid','onick']
				tag_data = dict([(tag.split('=')[0].strip("'"),tag.split('=')[1].strip("'")) for tag in tag_list if tag.split('=')[0].strip("'") in tag_label])
			else:
				pass
			if 'level' in x_str_split:
				level_soup = bs(x_str_split.split("html")[-1].split('":')[-1].split('}')[0].replace('&gt;','>').replace('&lt;', '<').replace('\/','/'))
				for x in level_soup.findAll('a'):
					if 'Lv' in str(x):
						level = x.span.string if x.span.string else 'null'   #获取用户等级积分

			else:
				pass
     
		user_sns_data = label_value.copy()
		user_sns_data.update(label_url)
		user_sns_data.update(tag_data)
		# print "user_sns_data:",user_sns_data
		user_sns_data['update_time'] = time.ctime()   #插入获取时间
		user_sns_data['level'] = level
		print user_sns_data
    
		return user_sns_data


aaa = 'value=weibo_page\">\u7b2c&nbsp'
bbb = str(aaa).decode('utf-8').encode('utf-8')
print bbb