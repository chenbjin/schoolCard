# -*- encoding:utf-8 -*-
import urllib2
import string
import re
import os
		
#baike 
def getSchoolDataTest(schoolname):
	url = 'http://api.baike.baidu.com/search/word?word='+schoolname
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	request = urllib2.Request(url, headers=headers)
	try:
		con = urllib2.urlopen(request, timeout=10)
		content = con.read()
		print content
	except Exception, e:
		raise e
	else:
		pass

def loadSchoolName(filename):
	freader = open(filename)
	return freader.readlines()

def getSchoolData():
	pass

def getSchoolNameByFile(htmlname):
	html = readFile(htmlname)
	schoolItem = re.findall('<a target="_blank" href="http://www.ipin.com/school/(.*?)">(.*?)</a>', html, re.S)
	schoolranking = ""
	cnt = 1
	for item in schoolItem:
		schoolranking += str(cnt) + " "+item[1]+'\n'
		cnt += 1 
	saveResult('sch_name_ipin.txt',schoolranking)

def getSchoolNameByUrl(url):
	user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
	headers = { 'User-Agent' : user_agent }
	request = urllib2.Request(url, headers=headers)
	try:
		con = urllib2.urlopen(request, timeout=10)
		content = con.read()
		
		#print content
		#From iPIN.com
		schoolItem = re.findall('<a target="_blank" href="/school/(.*?)">(.*?)</a>', content, re.S)
		for item in schoolItem:
			print item[0], item[1]
		'''
		#From ziyuan.eol.cn
		provinceItem = re.findall("<a class=a13 href='(.*?)'>(.*?)</a>", content, re.S)
		schoolnum = 0
		for item in provinceItem:
			print item[0],item[1]
			url2 = "http://ziyuan.eol.cn/" + item[0]
			print url2
			request2 = urllib2.Request(url2, headers=headers)
			try:
				con2 = urllib2.urlopen(request2, timeout=10)
				content2 = con2.read()
				#print content2
				schoolItem = re.findall('<a class=a17 href="(.*?)" target="_blank">(.*?)</a>', content, re.S)
				for sitem in schoolItem:
					print sitem[0],sitem[1]
			except Exception, e:
				raise e
		'''
	except Exception, e:
		raise e
	else:
		saveResult('./data/school.html',content)

def readFile(filename):
	content = open(filename).read()
	return content

def saveResult(filename, content):
	f = open(filename, 'w+')
	f.write(content)
	f.close()

def main():
	#url_path = "http://www.ipin.com/school/ranking.do"
	#url_path = "http://ziyuan.eol.cn/list.php?listid=128"
	#getSchoolNameByUrl(url_path)
	#html_path = './data/schoolranking_ipin.html'
	#getSchoolNameByFile(html_path)
	#schoolname='四川大学'
	#getSchoolDataTest(schoolname)

if __name__ == '__main__':
	main()