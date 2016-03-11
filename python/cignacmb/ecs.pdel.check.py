#!/usr/bin/env python
# -*- coding: utf-8 -*-

'验证保单在CICAP中是否存在'

__author__ = 'Cheney'

import sys
import fileinput
import time,datetime
import os
import shutil
import xlrd
import Tkinter
import tkMessageBox

reload(sys)
sys.setdefaultencoding("utf-8")

rootdir = "jettbatchbakup/"  	# 接口文件目录
collectFileName = "TRKPOTXT"  	# 提取保单号的文件
startRow = 2  					# 接口文件第一行不是保单号，所以从第二行开始统计

#policyNoListFile = "需要跑的保单号.txt".encode("GBK")  		# 收集的保单号存在的临时文件，CICAP上传该文件内容
policyNoListFile = "需要跑的保单号.txt"  		# 收集的保单号存在的临时文件，CICAP上传该文件内容
TotalCount = 0									# 统计收集到的保单量

CICAPPolicyNoXls = "result-保单号在CICAP存在.xls"  	# CICAP中存在的保单号清单
CICAPPDELXls = "result-保单号在PDEL存在.xls"  		# CICAP中存在PDEL信息的保单号清单
XlsStartRow = 2  									# CICAP导出的结果文件，保单号的起始行

resultFile = "result.txt"  							# 比对后的结果文件，存储相关的分析结果
BackUpDir = "backup/"								# 分析完成后，相关结果文件的备份目录
NewLine = '\r\n'									# 换行符

def collectPolicyNos(dirPath):
	'遍历指定目录包括子目录下的所有文件，提取保单号写入临时文件'
	for rt, dirs, files in os.walk(dirPath):
		for f in files:
			if os.path.splitext(f)[0] == collectFileName :
				filePath = os.path.join("%s\\%s" % (rt, f))
				readAndWritePolicyNos(filePath)

def readAndWritePolicyNos(fileName):
	'提取指定文件中的保单号写入临时文件'
	global TotalCount
	writer = file(policyNoListFile.encode('GBK'), 'a+')
	index = 0
	for line in fileinput.input(fileName) :
		index += 1
		if index < startRow :
			continue
		TotalCount += 1

		writer.write(line[:10])
		writer.write(NewLine)
	writer.close



def checkPolicyNo():
	'1. 保单号在CICAP中是否存在'
	'2. 保单的PDEL信息是否存在'

	# 获取需调整的保单号集合
	totalPolicyList = getTotalPolicyNos()
	
	# result-保单号在CICAP存在.xls
	cicapPolicyList = getResultPolicyNos(CICAPPolicyNoXls)

	# result-保单号在PDEL存在.xls
	cicapPDELList = getResultPolicyNos(CICAPPDELXls)

	resultList = []
	resultList.append(time.strftime('%Y-%m-%d %H:%M:%S'))
	resultList.append('总保单数量：' + str(len(totalPolicyList)))
	resultList.append('已导入CICAP中的单量：' + str(len(cicapPolicyList)))
	resultList.append('CICAP中PDEL信息存在的单量：' + str(len(cicapPDELList)))
	resultList.append(NewLine)

	resultList.append('未导入CICAP中的保单：')
	resultList.append(NewLine.join(set(totalPolicyList).difference(set(cicapPolicyList))))
	resultList.append(NewLine)

	resultList.append('缺失PDEL信息的保单：')
	resultList.append(NewLine.join(set(totalPolicyList).difference(set(cicapPDELList))))
	resultList.append(NewLine)

	writer = open(resultFile.encode('GBK'), 'w')
	writer.write(NewLine.join(resultList))
	writer.close

	return NewLine.join(resultList)

def getTotalPolicyNos():
	'提取收集到的所有保单号'
	list = []
	for line in fileinput.input(policyNoListFile.encode('GBK')) :
		line = line.replace('\r', '').replace('\n', '')
		list.append(line)
	return list


def getResultPolicyNos(resultFileName):
	'根据CICAP工具导出的excel文件，提取结果集中的保单号清单'
	data = xlrd.open_workbook(resultFileName.encode('GBK'))
	table = data.sheets()[0]          #通过索引顺序获取

	list = []
	for i in range(XlsStartRow - 1, table.nrows):
		list.append(table.row(i)[0].value)
	return list

def checkFiles():
	'解析前，判断相关接口文件是否已存在'
	if not os.path.exists(policyNoListFile.encode('GBK')):
		msg = '文件【%s】不存在'.encode('GBK') % policyNoListFile.encode('GBK')
		print msg
		return False, msg
	if not os.path.exists(CICAPPolicyNoXls.encode('GBK')):
		msg = '文件【%s】不存在'.encode('GBK') % CICAPPolicyNoXls.encode('GBK')
		print msg
		return False, msg
	if not os.path.exists(CICAPPDELXls.encode('GBK')):
		msg = '文件【%s】不存在'.encode('GBK') % CICAPPDELXls.encode('GBK')
		return False, msg
	return True, ''

def backupResult():
	'备份结果文件'
	backupPath = BackUpDir + time.strftime('%Y%m%d_%H%M%S')
	os.mkdir(backupPath)

	shutil.move(policyNoListFile.encode('GBK'), backupPath)
	shutil.move(CICAPPolicyNoXls.encode('GBK'), backupPath)
	shutil.move(CICAPPDELXls.encode('GBK'), backupPath)
	shutil.move(resultFile.encode('GBK'), backupPath)

def loadWindow():
	def sendmessage():
		windowCallback(t)

	root = Tkinter.Tk()
	root.resizable(False,False)
	root.title('CICAP PDEL 工具')
	root.update()


	curWidth = 400
	curHeight = 350
	scnWidth,scnHeight = root.maxsize()  		# get screen width and height
	tmpcnf = '%dx%d+%d+%d' % (curWidth, curHeight, (scnWidth-curWidth)/2, (scnHeight-curHeight)/2)
	root.geometry(tmpcnf)

	Tkinter.Button(root, text='开始', command=sendmessage).pack()

	t = Tkinter.Text(root)
	t.pack()

	root.mainloop()


def windowCallback(text):
	text.insert(Tkinter.END, '收集要验证的保单...')
	text.insert(Tkinter.END, NewLine)
	text.update()

	collectPolicyNos(rootdir)  						# 提取需验证的保单号清单

	text.insert(Tkinter.END, '收集到的总单量：')
	text.update()
	text.insert(Tkinter.END, TotalCount)

	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, '启动上载工具...')
	text.update()

	os.system("upload.dtt")							# 启动外部工具上传保单号清单

	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, '下载已上传CICAP的保单号...')
	text.update()
	
	os.system("download-保单号存在.dtf".encode("GBK"))  	# 启动外部工具下载已上传CICAP的保单号清单

	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, '下载已存在PDEL信息的保单号...')
	text.update()

	os.system("download-PDEL信息存在.dtf".encode("GBK"))  	# 启动外部工作下载存在PDEL信息的保单号清单

	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, NewLine)
	text.insert(Tkinter.END, '开始解析导入结果...')
	text.update()

	flag, msg = checkFiles()
	if flag :
		result = checkPolicyNo()
		backupResult()

		text.insert(Tkinter.END, NewLine)
		text.insert(Tkinter.END, NewLine)
		text.insert(Tkinter.END, '--------------------------------------')
		text.update()
		text.insert(Tkinter.END, NewLine)
		text.insert(Tkinter.END, '解析成功，最终结果：')
		text.insert(Tkinter.END, NewLine)
		text.update()
		text.insert(Tkinter.END, NewLine)
		text.insert(Tkinter.END, result)
	else:
		text.insert(Tkinter.END, NewLine)
		text.insert(Tkinter.END, msg.decode('GBK').encode('utf-8'))

	text.insert(Tkinter.END, NewLine)


if __name__ == '__main__':
	loadWindow()

