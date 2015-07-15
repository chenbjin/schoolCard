# -*- encoding:utf-8 -*-
#@author:  chenbjin
#@time:    2015-07-14
import re
import string
import json

sch = {} #学校更名历史字典
remain_sch = {}  #添加的学校
'''
处理高校合并通知
'''
def dealCombineRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	for rp in rps:
		rp = rp.strip().replace("教育部关于同意在","")
		rp = rp.strip().replace("教育部关于同意","")
		rp = rp.strip().replace("关于同意","")
		rp = rp.strip().replace("关于","")
		rp = rp.strip().replace("教育部办公厅在","")
		rp = rp.strip().replace("的函","")
		rp = rp.strip().replace("的决定","")
		rp = rp.strip().replace("的通知","")
		rp = rp.strip().replace("的批复","")
		rp = rp.strip().replace("基础上筹建",",")
		rp = rp.strip().replace("基础上建立",",")
		rp = rp.strip().replace("合并成立",",")
		rp = rp.strip().replace("合并建立",",")
		rp = rp.strip().replace("合并组建",",")
		rp = rp.strip().replace("合并筹建",",")
		rp = rp.strip().replace("合并为","")
		rp = rp.strip().replace("合并","")
		rp = rp.strip().replace("筹备","")
		rp = rp.strip().replace("与",",")
		rp_split = rp.split(',')
		#print rp_split[0]
		if len(rp_split) == 2:
			sch_name = rp_split[1]
			history_name = rp_split[0]
			history_name = history_name.split('、')
			#print len(history_name)
			if sch.has_key(sch_name):
			#更新记录
				#print sch_name
				for name in history_name:
					if name != sch_name:
						sch[sch_name].append(name)
						if sch.has_key(name):	
							#print "---",name
							for item in sch[name]:
								if item != sch_name:
									sch[sch_name].append(item)
							del sch[name]
			else:
				#补充未记录学校
				sch[sch_name] = []
				remain_sch[sch_name] = []
				for name in history_name:
					sch[sch_name].append(name)
					remain_sch[sch_name].append(name)

		if len(rp_split) == 3:
			sch_name = rp_split[2]
			#print sch_name
			history_name1 = rp_split[0]
			history_name2 = rp_split[1]
			if sch.has_key(sch_name):
				if history_name1 != sch_name:
					sch[sch_name].append(history_name1)
				if history_name2 != sch_name:	
					sch[sch_name].append(history_name2)
			else:
				sch[sch_name] = []
				sch[sch_name].append(history_name1)
				sch[sch_name].append(history_name2)
				remain_sch[sch_name] = []
				remain_sch[sch_name].append(history_name1)
				remain_sch[sch_name].append(history_name2)

'''
处理高校建立通知，原通知不完整，数据已从通知文件中补全
'''
def dealFoundRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	cnt = 0
	for rp in rps:
		cnt+=1
		rp = rp.strip().replace("经研究，教育部同意在","")
		rp = rp.strip().replace("经研究，同意在","")
		rp = rp.strip().replace("教育部同意在","")
		rp = rp.strip().replace("经研究，教育部同意","")
		rp = rp.strip().replace("同意在","")
		rp = rp.strip().replace("在","")
		rp = rp.strip().replace("的基础上建立",",")
		rp = rp.strip().replace("基础上建立",",")
		rp = rp.strip()
		rp_split = rp.split(',')
		#print len(rp_split)
		sch_name = rp_split[1]
		history_name = rp_split[0]
		#print history_name
		history_name = history_name.split('、')
		if sch.has_key(sch_name):
			for name in history_name:
				if name != sch_name:
					sch[sch_name].append(name)
					if sch.has_key(name):
						for item in sch[name]:
							if item != sch_name:
								sch[sch_name].append(item)
						del sch[name]						
		else:
			sch[sch_name] = []
			remain_sch[sch_name] = []
			for name in history_name:
				sch[sch_name].append(name)
				remain_sch[sch_name].append(name)

'''
处理高校更名通知
'''
def dealRenameRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)	
	for rp in rps:
		rp = rp.strip().replace("教育部","")
		rp = rp.strip().replace("办公厅","")
		rp = rp.strip().replace("函","")
		rp = rp.strip().replace("通知","")
		rp = rp.strip().replace("决定","")
		rp = rp.strip().replace("批复","")
		rp = rp.strip().replace("升格为本科院校并更名为",",")
		rp = rp.strip().replace("更名为",",")
		rp = rp.strip().replace("关于","")
		rp = rp.strip().replace("同意将","")
		rp = rp.strip().replace("同意","")
		rp = rp.strip().replace("的","")
		rp = rp.strip().replace("、",",")
		rp_split = rp.split(',')
		i = 0
		while i < len(rp_split):
			j = i + 1
			i = i + 2
			if j < len(rp_split):
				sch_name = rp_split[j]
				history_name = rp_split[j-1]
				if sch.has_key(sch_name):
					#print sch_name
					#更新记录
					if history_name != sch_name:
						sch[sch_name].append(history_name)
						if sch.has_key(history_name):
							for item in sch[history_name]:
								if item != sch_name:
									sch[sch_name].append(item)
							del sch[history_name]
				else:
					#补充未记录学校
					sch[sch_name] = []
					sch[sch_name].append(history_name)
					remain_sch[sch_name] = []
					remain_sch[sch_name].append(history_name)

'''
处理高校转设通知
'''
def dealSetupRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	for rp in rps:
		rp = rp.strip().replace("教育部关于同意","")
		rp = rp.strip().replace("的函","")
		rp = rp.strip().replace("的通知","")
		rp = rp.strip().replace("的批复","")
		rp = rp.strip().replace("联合","")
		rp = rp.strip().replace("转设为",",")
		rp = rp.strip().replace("与",",")
		rp_split = rp.split(',')
		if len(rp_split) == 2:
			sch_name = rp_split[1]
			history_name = rp_split[0]
			if sch.has_key(sch_name):
			#更新记录
				if sch_name != history_name:
					sch[sch_name].append(history_name)
					if sch.has_key(history_name):
						for item in sch[history_name]:
							if item != sch_name:
								sch[sch_name].append(item)
						del sch[history_name]
			else:
				#补充未记录学校
				sch[sch_name] = []
				sch[sch_name].append(history_name)
				remain_sch[sch_name] = []
				remain_sch[sch_name].append(history_name)
		if len(rp_split) == 3:
			sch_name = rp_split[2]
			#print sch_name
			history_name1 = rp_split[0]
			history_name2 = rp_split[1]
			if sch.has_key(sch_name):
				if sch_name != history_name1:
					sch[sch_name].append(history_name1)
				if sch_name != history_name2:
					sch[sch_name].append(history_name2)
			else:
				sch[sch_name] = []
				sch[sch_name].append(history_name1)
				sch[sch_name].append(history_name2)
				remain_sch[sch_name] = []
				remain_sch[sch_name].append(history_name1)
				remain_sch[sch_name].append(history_name2)

'''
处理高校建立通知
'''
def dealUpgradeRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	for rp in rps:
		rp = rp.strip().replace("教育部","")
		rp = rp.strip().replace("关于","")
		rp = rp.strip().replace("的函","")
		rp = rp.strip().replace("的通知","")
		rp = rp.strip().replace("的批复","")
		rp = rp.strip().replace("同意在","")
		rp = rp.strip().replace("同意","")
		rp = rp.strip().replace("在","")
		rp = rp.strip().replace("合并基础上","")
		rp = rp.strip().replace("的基础上","")
		rp = rp.strip().replace("基础上","")
		rp = rp.strip().replace("建立",",")
		rp = rp.strip().replace("与",",")
		rp_split = rp.split(',')
		#print len(rp_split)
		if len(rp_split) == 2:
			sch_name = rp_split[1]
			history_name = rp_split[0]
			if sch.has_key(sch_name):
			#更新记录
				if sch_name != history_name:
					sch[sch_name].append(history_name)
					if sch.has_key(history_name):
						for item in sch[history_name]:
							if item != sch_name:
								sch[sch_name].append(item)
						del sch[history_name]			
			else:
				#补充未记录学校
				sch[sch_name] = []
				sch[sch_name].append(history_name)
				remain_sch[sch_name] = []
				remain_sch[sch_name].append(history_name)
		if len(rp_split) == 3:
			sch_name = rp_split[2]
			#print sch_name
			history_name1 = rp_split[0]
			history_name2 = rp_split[1]
			if sch.has_key(sch_name):
				sch[sch_name].append(history_name1)
				sch[sch_name].append(history_name2)
			else:
				sch[sch_name] = []
				sch[sch_name].append(history_name1)
				sch[sch_name].append(history_name2)
				remain_sch[sch_name] = []
				remain_sch[sch_name].append(history_name1)
				remain_sch[sch_name].append(history_name2)

'''
处理教育部合并通知：1990-20060515
'''
def dealCombineFile(combine_file):
	global sch
	global remain_sch
	rp = loadReports(combine_file)
	cnt = 0
	while cnt < len(rp):
		sch_name = rp[cnt+1].strip()
		history_name = rp[cnt+3].strip()
		history_name = history_name.replace(' <br>',',')
		history_name = history_name.replace('<br>',',')
		#print sch_name+" : "+history_name
		history_name = history_name.split(',')
		if sch.has_key(sch_name):
			#更新记录
			for name in history_name:
				if name != sch_name:
					sch[sch_name].append(name)
					if sch.has_key(name):
						for item in sch[name]:
							if item != sch_name:
								sch[sch_name].append(item)
						del sch[name]
		else:
			#补充未记录学校
			sch[sch_name] = []
			remain_sch[sch_name] = []
			for name in history_name:
				sch[sch_name].append(name)
				remain_sch[sch_name].append(name)
		cnt += 5

'''
去重处理，去掉重复更名（合并）
'''
def removeDuplicate():
	global sch
	for school in sch:
		sch[school] = list(set(sch[school]))

'''
导入学校名
'''
def loadSchoolName(filename):
	sch_name = {}
	f = open(filename)
	for name in f.readlines():
		name = name.strip()
		#print name
		sch_name[name] = []
	return sch_name

'''
导入通知文件
'''
def loadReports(filename):
	f = open(filename)
	content = f.readlines()
	return content

'''
结果保存为json格式
'''
def showResult():
	global sch
	global remain_sch
	cnt = 0
	for tmp in sch:
		if len(sch[tmp]) != 0:
			print tmp+' : '+', '.join(sch[tmp]); cnt += 1
	print cnt
	result = json.dumps(sch, sort_keys=True, indent=2)
	result = result.decode('gbk').encode('utf-8')
	saveResult('result.json', result)
	'''
	cnt = 0
	for tmp in remain_sch:
		print tmp+':'+','.join(remain_sch[tmp]); cnt += 1
	print cnt
	'''

'''
将程序结果写到本地文件
'''
def saveResult(filename, content):
	filepath = './data/result/'
	f = open(filepath+filename, 'w+')
	f.write(content)
	f.close()

def main():
	global sch
	global remain_sch

	sch_file = "./data/sch_name/sch_name_new.txt"
	rp_rename_file = "./data/reports/reports_rename.txt"
	rp_upgrade_file = "./data/reports/reports_upgrade.txt"
	rp_setup_file = "./data/reports/reports_setup.txt"
	rp_found_file = "./data/reports/reports_found.txt"
	rp_combine_file = "./data/reports/reports_combine.txt"
	school_combine_since1990 = "./data/reports/school_combine_since1990.txt"

	sch = loadSchoolName(sch_file)
	print "before:",len(sch)

	dealSetupRP(rp_setup_file)
	dealCombineFile(school_combine_since1990)
	dealCombineRP(rp_combine_file)	
	dealFoundRP(rp_found_file)
	dealRenameRP(rp_rename_file)
	dealUpgradeRP(rp_upgrade_file)

	print "after:",len(sch)
	removeDuplicate()
	showResult()

	
if __name__ == '__main__':
	main()