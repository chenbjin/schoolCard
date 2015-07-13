# -*- encoding:utf8 -*-
import urllib2

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

def saveResult(filename, content):
	f = open(filename, 'w+')
	f.write(content)
	f.close()

def main():
	schools = loadSchoolName("./data/sch_name.txt")
	for sch in schools[1:10]:
		print sch
	#getSchoolDataTest(schools[1])

if __name__ == '__main__':
	main()