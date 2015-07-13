# -*- encoding:utf8 -*-
import urllib2
import urllib
import re

REPORT_RENAME = ""

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
模式匹配，匹配更名通知
'''
def patternRec(content):
	global REPORT_RENAME
	reports = re.findall('var abc = "(.*?)"', content, re.S)
	for item in reports:
		print item
		REPORT_RENAME += item+'\n'

'''
构建查询的URL
'''
def urlBuild(report_type, page):
	url_head = "http://www.moe.gov.cn/was5/web/search?page="
	url_query_part1 = "&channelid=239278&searchword=xxlb%3D%27%27+and+doctitle%3D%27"
	url_query_part2 = "%27+and+fwjg%3D%27%27+and+idxID%3D%27%27+and+fwzh%3D%27%27+and+yysj%3D%27%27++and+gwbt%3D%27%27&keyword=xxlb%3D%27%27+and+doctitle%3D%27"
	url_query_part3 = "%27+and+fwjg%3D%27%27+and+idxID%3D%27%27+and+fwzh%3D%27%27+and+yysj%3D%27%27++and+gwbt%3D%27%27&orderby=-SCRQ&perpage=20&outlinepage=10&searchscope=&timescope=&timescopecolumn=&orderby=-SCRQ&andsen=&total=&orsen=&exclude="
	rp_type = urllib.quote(report_type)
	url = url_head + str(page) + url_query_part1 + rp_type + url_query_part2 + rp_type + url_query_part3
	return url

'''
逐页获取教育部通知
'''
def getReportOnPage(content,report_type):
	total_num = re.findall('var zong=(\d+);', content)
	#print total_num[0]
	if int(total_num[0]) % 20 == 0:
		total_page = int(total_num[0]) / 20
	else:
		total_page = int(total_num[0]) / 20 + 1
	cnt = 2
	while cnt <= total_page:
		#print cnt
		url = urlBuild(report_type, cnt)
		content = getUrl(url)
		patternRec(content)
		cnt += 1

'''
模板：根据不同报告类型获取教育部通知
'''
def getReportsTemplate(report_type):
	url = urlBuild(report_type, page=1)
	content = getUrl(url)
	patternRec(content)
	getReportOnPage(content,report_type)
	#print total_page
	

'''
获取合并通知，存入本地文件reports_combine.txt
'''
def getCombineReports():
	global REPORT_RENAME
	report_type = "合并"
	getReportsTemplate(report_type)
	saveResult('report s_combine.txt',REPORT_RENAME)

'''
获取更名通知，存入本地文件reports_combine.txt
'''
def getRenameReports():
	global REPORT_RENAME
	report_type = "更名"
	getReportsTemplate(report_type)
	saveResult('reports_rename.txt',REPORT_RENAME)

'''
获取专科升学院通知，存入本地文件reports_upgrade.txt
'''
def getUpgradeReports():
	global REPORT_RENAME
	report_type = "基础上建立"
	getReportsTemplate(report_type)
	saveResult('reports_upgrade.txt',REPORT_RENAME)

'''
获取转设学院通知，存入本地文件reports_setup.txt
'''
def getSetupReports():
	global REPORT_RENAME
	report_type = "转设"
	getReportsTemplate(report_type)
	saveResult('reports_setup.txt',REPORT_RENAME)

'''
获取建立学院通知，存入本地文件reports_found.txt
注意：需进一步抓取细节，在什么学院基础上建立新学院
'''
def getFoundReports():
	global REPORT_RENAME
	report_type = "同意建立"
	getReportsTemplate(report_type)
	saveResult('reports_found.txt',REPORT_RENAME)
	

'''
将程序结果写到本地文件
'''
def saveResult(filename, content):
	f = open(filename, 'w+')
	f.write(content)
	f.close()

def main():
	#getCombineReports()
	#getRenameReports()
	#getUpgradeReports()
	#getSetupReports()
	getFoundReports()
		
if __name__ == '__main__':
	main()