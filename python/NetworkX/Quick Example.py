#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'Cheney'

'''
http://networkx.github.io/examples.html#quick-example

安装说明：http://blog.sina.com.cn/s/blog_720448d301018px7.html
安装顺序：
http://pypi.python.org/pypi/networkx/下载networkx-1.1-py2.6.egg
http://sourceforge.net/projects/pywin32/下载pywin32-214.win32-py2.6.exe
matplotlib：http://sourceforge.net/projects/matplotlib/
numpy：http://sourceforge.net/projects/numpy/files/

egg文件安装：
启动DOS控制台（在“运行”里输入cmd），输入C:\Python26\Lib\site-packages\easy_install.py C:\networkx-1.1-py2.6.egg，回车后会自动执行安装
'''

import networkx as nx

G=nx.Graph()
G.add_node("spam")
G.add_edge(1,2)

print(G.nodes())

print(G.edges()