# -*- encoding:utf-8 -*-
import re
import string

sch = {}
remain_sch = {}

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
					if sch.has_key(history_name):
						sch[sch_name].append(history_name)
						for item in sch[history_name]:
							sch[sch_name].append(item)
						del sch[history_name]
					else:
						sch[sch_name].append(history_name)
				else:
					#补充未记录学校
					sch[sch_name] = []
					sch[sch_name].append(history_name)
					remain_sch[sch_name] = []
					remain_sch[sch_name].append(history_name)

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
				if sch.has_key(history_name):
					sch[sch_name].append(history_name)
					for item in sch[history_name]:
						sch[sch_name].append(item)
					del sch[history_name]
				else:
					sch[sch_name].append(history_name)
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
				if sch.has_key(history_name):
					sch[sch_name].append(history_name)
					for item in sch[history_name]:
						sch[sch_name].append(item)
					del sch[history_name]
				else:
					sch[sch_name].append(history_name)
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

def dealFoundRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	for rp in rps:
		flag = 0 
		if flag != 1:
			tmp = re.findall('在(.*?)的基础上建立(.*?)，', rp)
			if tmp != None:
				flag = 1
		if flag != 1:
			tmp = re.findall('在(.*?)基础上建立(.*?)，', rp)
			if tmp != None:
				flag = 1
		if flag == 1:
			for item in tmp:
				sch_name = item[1]
				history_name = item[0]
				history_name = history_name.split('、')
				if sch.has_key(sch_name):
					for name in history_name:
						if sch.has_key(name):
							for x in sch[name]:
								sch[sch_name].append(x)
							del sch[name]
						else:
							sch[sch_name].append(name)
				else:
					sch[sch_name] = []
					remain_sch[sch_name] = []
					for name in history_name:
						sch[sch_name].append(name)
						remain_sch[sch_name].append(name)

def dealCombineRP(rp_file):
	global sch
	global remain_sch
	rps = loadReports(rp_file)
	rps = reversed(rps)
	for rp in rps:
		rp = rp.strip().replace("教育部关于同意","")
		rp = rp.strip().replace("关于同意","")
		rp = rp.strip().replace("关于","")
		rp = rp.strip().replace("的函","")
		rp = rp.strip().replace("的决定","")
		rp = rp.strip().replace("的通知","")
		rp = rp.strip().replace("的批复","")
		rp = rp.strip().replace("合并成立",",")
		rp = rp.strip().replace("合并建立",",")
		rp = rp.strip().replace("合并组建",",")
		rp = rp.strip().replace("合并筹建",",")
		rp = rp.strip().replace("合并","")
		rp = rp.strip().replace("筹备","")
		rp = rp.strip().replace("与",",")
		rp_split = rp.split(',')
		print rp

def loadSchoolName(filename):
	sch_name = {}
	f = open(filename)
	for name in f.readlines():
		name = name.strip()
		#print name
		sch_name[name] = []
	return sch_name

def loadReports(filename):
	f = open(filename)
	content = f.readlines()
	return content

def showResult():
	global sch
	global remain_sch
	cnt = 0
	for tmp in sch:
		if len(sch[tmp]) != 0:
			print tmp+':'+','.join(sch[tmp]); cnt += 1
	print cnt
	
	cnt = 0
	for tmp in remain_sch:
		print tmp+':'+','.join(remain_sch[tmp]); cnt += 1
	print cnt

def main():
	global sch
	global remain_sch

	sch_file = "./data/sch_name/sch_name_gov.txt"
	rp_rename_file = "./data/reports/reports_rename.txt"
	rp_upgrade_file = "./data/reports/reports_upgrade.txt"
	rp_setup_file = "./data/reports/reports_setup.txt"
	rp_found_file = "./data/reports/reports_found.txt"
	rp_combine_file = "./data/reports/reports_combine.txt"

	sch = loadSchoolName(sch_file)
	print "before:",len(sch)
	dealCombineRP(rp_combine_file)
	'''
	dealSetupRP(rp_setup_file)
	dealFoundRP(rp_found_file)
	dealRenameRP(rp_rename_file)
	dealUpgradeRP(rp_upgrade_file)
	'''
	print "after:",len(sch)
	
	showResult()

	
if __name__ == '__main__':
	main()