# -*- encoding:utf-8 -*-
#@author:  chenbjin
#@time:    2015-07-12
import csv
import re

'''
从教育部csv文件读取高校名称
'''
def readCSV(filename):
	result = ""
	csvfile = file(filename,'rb')
	reader = csv.reader(csvfile)
	cnt = 0
	for row in reader:
		newrow = ','.join(row).decode('utf-8').encode('utf-8')
		if re.match(r'^\d+', newrow):
			result += row[1]+'\n'
	saveResult('sch_name_gov.txt',result)

'''
将程序结果写到本地文件
'''
def saveResult(filename, content):
	filepath = './data/sch_name/'
	f = open(filepath+filename, 'w+')
	f.write(content)
	f.close()

def main():
	filename = './data/sch_gov.csv'
	readCSV(filename)

if __name__ == '__main__':
	main()