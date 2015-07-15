# -*- encoding:utf8 -*-
#@author:  chenbjin
#@time:    2015-07-12
import urllib2
import urllib
import re
from sgmllib import SGMLParser
'''
功能： 从教育部获取各高校更名/合并/转设/建立的通知
URL： http://www.moe.gov.cn/jyb_xxgk/moe_xxgk/xxgk_left/nfo_search/
'''
REPORT_RENAME = ""

'''
SGML解析器，解析<a>标签
'''
class ReportName(SGMLParser):
	"""docstring for ListName"""
	def __init__(self):
		SGMLParser.__init__(self)
		self.urls = []
		self.reportsname = []
		self.is_a = 0

	def start_a(self, attrs):
		for k, v in attrs:
			if k == 'href' and v.startswith("http://www.moe.gov.cn/srcsite"):
				self.urls.append(v)
				is_a = 1

	def end_a(self):
		self.is_a = 0
	
	def handle_data(self,text):
		if self.is_a:
			self.reportsname.append(text)

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
模式匹配，匹配通知标题，对"建立"的学院进一步分析
'''
def patternRec(content, report_type):
	global REPORT_RENAME
	if report_type == "同意建立":
		report_list = ReportName()
		report_list.feed(content)
		for rp_url in report_list.urls:
			rp_content = getUrl(rp_url)
			rp_summary = re.findall('<td class="gongkai_font_gray" colspan="5" valign="top">(.*?)</td>',rp_content,re.S)
			#print rp_summary[0].find("基础上建立")
			if rp_summary[0].find("基础上建立") != -1:
				print rp_summary[0]
				REPORT_RENAME += rp_summary[0]+'\n'
	else:
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
		patternRec(content,report_type)
		cnt += 1

'''
模板：根据不同报告类型获取教育部通知
'''
def getReportsTemplate(report_type):
	url = urlBuild(report_type, page=1)
	content = getUrl(url)
	patternRec(content, report_type)
	getReportOnPage(content, report_type)
	#print total_page
	

'''
获取合并通知，存入本地文件reports_combine.txt
'''
def getCombineReports():
	global REPORT_RENAME
	report_type = "合并"
	getReportsTemplate(report_type)
	saveResult('reports_combine.txt',REPORT_RENAME)

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
注意：需进一步抓取细节，在什么学院基础上建立新学院。
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
	filepath = './data/reports/'
	f = open(filepath+filename, 'w+')
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