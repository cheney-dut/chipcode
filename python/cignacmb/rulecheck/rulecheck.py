#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Cheney'

'''
产品投核保规则验证工具
'''

import ConfigParser
import codecs
import re, string, os, sys
import xlrd
import wx
import wx.grid
import wx.py.images as images

dir = 'products' # 产品目录
RuleSheetIndex = 1 # 规则用例在第二张sheet
RuleSheetTitleIndex = 0

RuleCaseXlsxTemplate = 'rulecase.xlsx' 	# 初始化显示用
RuleCaseXlsxParasCol = 6 				# 规则校验参数列：G列
ProductConfigFile = 'product.ini'
ProductConfigBaseTag = 'base'
ProductConfigTemplateTag = 'template'

RequestTemplateXMLFile = 'template.xml'

reload(sys)
sys.setdefaultencoding('utf-8')

class MyConfigParser(ConfigParser.ConfigParser):
	'''
	参考：修改Python ConfigParser option 大小写的问题  http://blog.csdn.net/xluren/article/details/40298561
	'''
	def __init__(self,defaults=None):
		ConfigParser.ConfigParser.__init__(self,defaults=None)
	def optionxform(self, optionstr):
		# 源码中此处为：return optionstr.lower()
		return optionstr

class RuleCheckMainFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, parent=None, title=u'产品投核保规则验证工具')
		self.icon = wx.Icon('worker.ico', wx.BITMAP_TYPE_ICO) # 相同文件夹下
		self.SetIcon(self.icon)
		c_x, c_y, c_w, c_h = wx.ClientDisplayRect() # 取得桌面显示区域高
		self.SetSize(wx.Size(c_w,c_h))
		#self.SetPosition(wx.Point(0,0))
		self.Centre()

		productTreePanel = wx.Panel(self,-1)

		#rulesGridPanel = wx.Panel(self, -1)
		rulesGridPanel = wx.Panel(self, -1, size=(300,300))

		requestXMLPanel = wx.Panel(self, -1)
		responseXMLPanel = wx.Panel(self, -1)

		# 产品树+（规则+报文）
		hbox = wx.BoxSizer(wx.HORIZONTAL)
		hbox.Add(productTreePanel, proportion=1, flag=wx.EXPAND, border=10)

		vbox = wx.BoxSizer(wx.VERTICAL)
		vbox.Add(rulesGridPanel, proportion=0, flag=wx.EXPAND, border=10)

		xmlhBox = wx.BoxSizer(wx.HORIZONTAL)
		xmlhBox.Add(requestXMLPanel, proportion=1, flag=wx.EXPAND, border=10)
		xmlhBox.Add(responseXMLPanel, proportion=1, flag=wx.EXPAND, border=10)

		vbox.Add(xmlhBox, proportion=8, flag=wx.EXPAND, border=10)

		hbox.Add(vbox, proportion=4, flag=wx.EXPAND, border=10)
		self.SetSizer(hbox)

		self.InitMenu()
		self.InitProductTree(productTreePanel)
		self.InitRulesGrid(rulesGridPanel)
		self.InitRequestXMLPanel(requestXMLPanel)
		self.InitResponseXMLPanel(responseXMLPanel)
		# 创建状态栏
		statusBar = self.CreateStatusBar()

	def InitToolBar(self):
		# 创建工具栏，自动放置在框架的顶部
		toolBar = self.CreateToolBar()
		# 给工具栏增加一个工具
		toolBar.AddSimpleTool(wx.NewId(), images.getPyBitmap(), "New", "Long help for 'New'")
		# 准备显示工具栏
		toolBar.Realize()

	def InitMenu(self):
		menuBar = wx.MenuBar()
		menu1 = wx.Menu()
		menuBar.Append(menu1, "&File")

		menu2 = wx.Menu()
		menuBar.Append(menu2, "&Edit")

		menuHelp = wx.Menu()
		menuBar.Append(menuHelp, "&Help")
		self.SetMenuBar(menuBar)

	def InitProductTree(self, parent):
		self.productTree = wx.TreeCtrl(parent)
		root = self.productTree.AddRoot(u"产品")

		files = os.listdir(dir)
		files.sort(reverse=True)
		for f in files:
			self.productTree.AppendItem(root, f)

		self.productTree.Expand(root) # Expand the first level
		self.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.OnProudctTreeActivated, self.productTree)

		vbox = wx.BoxSizer(orient=wx.VERTICAL)
		vbox.Add(self.productTree, proportion=1, flag=wx.EXPAND, border=0)
		parent.SetSizer(vbox)

	def InitRulesGrid(self, parent):
		#wx.ScrolledWindow(parent, id=-1, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.HSCROLL | wx.VSCROLL)
		self.ruleGridTitle = wx.StaticText(parent, -1) # 显示当前操作的产品

		#resultFileName = 'rulecase.xlsx'
		self.ruleGrid = wx.grid.Grid(parent)
		self.LoadGridTable(RuleCaseXlsxTemplate)

		vbox = wx.BoxSizer(orient=wx.VERTICAL)
		vbox.Add(self.ruleGridTitle, proportion=0, flag=wx.EXPAND, border=0)
		vbox.Add(self.ruleGrid, proportion=1, flag=wx.EXPAND, border=0)
		parent.SetSizer(vbox)

	def InitRequestXMLPanel(self, parent):
		requestXMlLabel = wx.StaticText(parent, -1, u"请求报文：")
		self.requestXMlText = wx.TextCtrl(parent, -1, value='fdaf', style=(wx.TE_MULTILINE | wx.TE_AUTO_SCROLL | wx.TE_DONTWRAP))

		vbox = wx.BoxSizer(orient=wx.VERTICAL)
		vbox.Add(requestXMlLabel, proportion=0, flag=wx.EXPAND, border=0)
		vbox.Add(self.requestXMlText, proportion=1, flag=wx.EXPAND, border=0)
		parent.SetSizer(vbox)

	def InitResponseXMLPanel(self, parent):
		responseXMlLabel = wx.StaticText(parent, -1, u"返回报文：")
		self.responseXMlText = wx.TextCtrl(parent, -1, value='fdas')

		vbox = wx.BoxSizer(orient=wx.VERTICAL)
		vbox.Add(responseXMlLabel, proportion=0, flag=wx.EXPAND, border=0)
		vbox.Add(self.responseXMlText, proportion=1, flag=wx.EXPAND, border=0)
		parent.SetSizer(vbox)

	# 产品树双击事件
	def OnProudctTreeActivated(self, evt):
		self.ClearComponentText()

		treeRoot = self.productTree.GetRootItem()
		item = evt.GetItem() # 返回与事件相关的项的wx.TreeItemId
		if treeRoot == item:
			return
		itemText = ""
		if item:
			itemText = self.productTree.GetItemText(item)

		self.ruleGridTitle.SetLabel(itemText)
		column = re.split(u'【|】', itemText)

		riskcode = itemText
		if len(column) > 1:
			riskcode = column[1]

		# 根据险种加载规则：主险加载主险的，主附搭配时加载附加险的
		productIniPath = dir + os.sep + itemText + os.sep + ProductConfigFile
		cf = self.GetProductIniParser(productIniPath)
		ruleXlsxFileName = cf.get(ProductConfigBaseTag, 'rulecase.xlsx')
		ruleXlsxFile = dir + os.sep + itemText + os.sep + ruleXlsxFileName
		self.LoadGridTable(ruleXlsxFile)

	def ClearComponentText(self):
		'产品切换时，清空部分控件内容'
		self.ruleGridTitle.SetLabel('')
		# 表格
		self.requestXMlText.SetValue('')
		self.responseXMlText.SetValue('')

	def LoadGridTable(self, rulecaseFile):
		'解析规则用例文件中的内容'
		data = xlrd.open_workbook(rulecaseFile)
		table = data.sheets()[RuleSheetIndex]          # 通过索引顺序获取

		row = []
		for i in range(len(table.row(RuleSheetTitleIndex))):
			row.append(table.row(RuleSheetTitleIndex)[i].value)
		colLabels = tuple(row) # 表头

		dataList = []
		for i in range(RuleSheetTitleIndex + 1, table.nrows):
			row = []
			for j in range(len(table.row(i))):
				row.append(table.row(i)[j].value)
			dataList.append(tuple(row))
		self.ruletuple = tuple(dataList)

		rowLabels = tuple(range(1, len(dataList) + 1))

		tableBase = GenericTable(self.ruletuple, rowLabels, colLabels)
		self.ruleGrid.SetTable(tableBase, True)

		self.ruleGrid.SetDefaultCellOverflow(True)
		self.ruleGrid.AutoSize() # http://blog.sina.com.cn/s/blog_56146dc501009jir.html

		self.ruleGrid.SetSelectionMode(wx.grid.Grid.SelectRows) # 一次选择整行

		self.ruleGrid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.OnRuleGridLEFTDCLICK)

	def OnRuleGridLEFTDCLICK(self, evt):
		productIniPath = dir + os.sep + self.ruleGridTitle.GetLabel() + os.sep + ProductConfigFile # 配置文件
		templateXmlPath = dir + os.sep + self.ruleGridTitle.GetLabel() + os.sep + RequestTemplateXMLFile # 报文模板

		# 生成报文模板
		file_object = open(templateXmlPath)
		templateContent = file_object.read()
		template = string.Template(templateContent)

		# 默认成功的请求参数
		cf = self.GetProductIniParser(productIniPath)
		kvs = cf.items(ProductConfigTemplateTag)

		# 提取excel中定义的动态属性，覆盖默认请求参数；在G列
		# 提取G列内容，即动态请求参数
		dynKvs = self.ruleGrid.GetCellValue(evt.GetRow(), RuleCaseXlsxParasCol)
		print dynKvs

		xml = unicode(template.substitute(dict(kvs)))
		# Python字符串处理出现错误：
		# UnicodeDecodeError: ‘ascii’ codec can’t decode byte 0xe6 in position 0: ordinal not in range(128)
		# http://www.crifan.com/python_unicodedecodeerror_codec_can_not_decode_byte_in_position_ordinal_not_in_range/
		# gVal['newPostPatStr'] = unicode(gVal['newPostPatStr'], "utf-8");
		self.requestXMlText.SetValue(xml)

		evt.Skip()

	def GetProductIniParser(self, file):
		'获取配置文件解析器'
		cf = MyConfigParser()
		fp = codecs.open(file, "r", "utf-8-sig")
		cf.readfp(fp)
		return cf

class GenericTable(wx.grid.PyGridTableBase):
	def __init__(self, data, rowLabels=None, colLabels=None):
		wx.grid.PyGridTableBase.__init__(self)
		self.data = data
		self.rowLabels = rowLabels
		self.colLabels = colLabels
	def GetNumberRows(self):
		return len(self.data)
	def GetNumberCols(self):
		if len(self.data) == 0 and None != self.colLabels:
			return len(self.colLabels)
		if len(self.data) == 0:
			return 0
		return len(self.data[0])
	def GetColLabelValue(self, col):
		if self.colLabels:
			return self.colLabels[col]
	def GetRowLabelValue(self, row):
		if self.rowLabels:
			return self.rowLabels[row]
	def IsEmptyCell(self, row, col):
		return False
	def GetValue(self, row, col):
		return self.data[row][col]
	def SetValue(self, row, col, value):
		pass

if __name__ == '__main__':
	print 'start ...'
	app = wx.App(False)
	frame = RuleCheckMainFrame()
	frame.Show(True)
	app.MainLoop()
	print 'end ...'

