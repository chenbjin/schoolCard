# -*- encoding:utf-8 -*-
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
			result += str(row[0]) +' '+ row[1]+'\n'
	saveResult('./data/sch_name_gov.txt',result)

'''
将程序结果写到本地文件
'''
def saveResult(filename, content):
	f = open(filename, 'w+')
	f.write(content)
	f.close()

def main():
	filename = 'sch_gov.csv'
	readCSV(filename)

if __name__ == '__main__':
	main()