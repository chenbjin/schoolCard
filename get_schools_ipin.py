# -*- encoding:utf-8 -*-
import urllib2
import string
import re
import os

'''
从iPIN抓取高校名称
'''	
def loadSchoolName(filename):
	freader = open(filename)
	return freader.readlines()

def getSchoolNameByFile(htmlname):
	html = readFile(htmlname)
	schoolItem = re.findall('<a target="_blank" href="http://www.ipin.com/school/(.*?)">(.*?)</a>', html, re.S)
	schoolranking = ""
	cnt = 1
	for item in schoolItem:
		schoolranking += item[1]+'\n'
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
	except Exception, e:
		raise e
	else:
		saveResult('./data/school.html',content)

def readFile(filename):
	content = open(filename).read()
	return content

def saveResult(filename, content):
	filepath = './data/sch_name/'
	f = open(filepath+filename, 'w+')
	f.write(content)
	f.close()

def main():
	#url_path = "http://www.ipin.com/school/ranking.do"
	#url_path = "http://ziyuan.eol.cn/list.php?listid=128"
	#getSchoolNameByUrl(url_path)
	html_path = './data/schoolranking_ipin.html'
	getSchoolNameByFile(html_path)

if __name__ == '__main__':
	main()