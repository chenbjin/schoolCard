# -*- encoding:utf-8 -*-
import urllib2
import re
import os
from sgmllib import SGMLParser 
'''
功能： 从"中国教育和科研计算机网"获取各省份高校数目及名称。
URL： http://ziyuan.eol.cn/list.php?listid=128
'''
SCH_NUM = 0  #国内高校总数
'''
SGML解析器，解析HTML标签
'''
class ListName(SGMLParser):
	"""docstring for ListName"""
	def __init__(self):
		SGMLParser.__init__(self)
		self.prov_urls = []
		self.sch_urls = []
		self.provincename =[]
		self.schoolname = []
		self.is_a13 = 0
		self.is_a17 = 0

	def start_a(self, attrs):
		for k, v in attrs:
			if k == 'class' and v == 'a13':
				self.is_a13 = 1
			if k == 'class' and v == 'a17':
				self.is_a17 = 1
			if k == 'href' and self.is_a13 == 1:
				self.prov_urls.append(v)
			if k == 'href' and self.is_a17 == 1:
				self.sch_urls.append(v)

	def end_a(self):
		self.is_a13 = 0
		self.is_a17 = 0
	
	def handle_data(self,text):
		if self.is_a13:
			self.provincename.append(text)
		if self.is_a17:
			if text == "(未入网)" or text == "（未入网）" or text == "未入网":
				self.schoolname[-1] = self.schoolname[-1]+"(未入网)"
			else:
				self.schoolname.append(text)

'''
抓取网页
'''
def getUrl(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	request = urllib2.Request(url, headers=headers)
	try:
		con = urllib2.urlopen(request, timeout=10)
		content = con.read()
	except Exception, e:
		raise e
	else:
		return content
	return content

'''
获取各省份，及对应高校数目及名称。
'''
def getProvince(data, base_url):
	global SCH_NUM  #国内高校总数
	result = ""
	province = ListName()
	province.feed(data)
	cnt = 0
	total = 0
	for item in province.provincename:
		if province.prov_urls[cnt].startswith("list.php?"):
			total += 1
			#result += "--------"+item.decode('utf-8').encode('utf-8') + "--------\n"
			print item.decode('utf-8').encode('utf-8'), province.prov_urls[cnt]
			url = base_url + province.prov_urls[cnt]
			content = getUrl(url)
			result += getSchool(content)
		cnt += 1
	print "total:",total
	#result += str(total) + ' ' + str(SCH_NUM)
	saveResult('sch_name_SGMLParser.txt',result)

'''
获取学校名称
'''
def getSchool(data):
	global SCH_NUM
	result = ""
	school = ListName()
	school.feed(data)
	cnt = 0
	#print "num_school:",len(school.schoolname)
	for x in xrange(0,len(school.schoolname)):
		if school.sch_urls[x].startswith("director.php?"):
			result += str(SCH_NUM) + ' ' + school.schoolname[x]+"\n"
			SCH_NUM += 1
			#print cnt, school.schoolname[x]
			cnt += 1
	return result

'''
将程序结果写到本地文件
'''
def saveResult(filename, content):
	filepath = './data/sch_name/'
	f = open(filename, 'w+')
	f.write(content)
	f.close()

def main():
	base_url = "http://ziyuan.eol.cn/"
	url = "http://ziyuan.eol.cn/list.php?listid=128"
	data = getUrl(url)
	#print data
	getProvince(data, base_url)

if __name__ == '__main__':
	main()