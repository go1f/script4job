#coding=utf-8
import xlwt
import pandas

def make_main_sheet():
	_f = pandas.read_excel("data.xlsx",sheet_name="Sheet1",usecols="I,E,D")
	_f.rename(columns={'名称（中文）':'漏洞名称','风险等级':'风险级别'}, inplace=True)
	_f.drop_duplicates(['漏洞名称','主机'],inplace=True)
	_f1 = _f.groupby(by='漏洞名称').apply(lambda x:' '.join(x['主机']))
	_f.drop_duplicates('漏洞名称',inplace=True)
	_f = _f.drop(columns=["主机"])
	_f = pandas.merge(_f,_f1.rename('主机'),how='left',on='漏洞名称')

	_f.rename(columns={'主机':'相关服务器'},inplace=True)
	_f.drop(columns=["漏洞名称"])
	_f.to_excel("main-sheet.xls")

def make_sub_sheet():
	_f = pandas.read_excel("data.xlsx",sheet_name="Sheet1",usecols="E,I,D,M,O")
	_f.rename(columns={'名称（中文）':'漏洞名称','风险等级':'风险级别','描述（中文）':'漏洞描述','解决方案（中文）':'修复建议','主机':'服务器IP'}, inplace = True)
	_f.drop_duplicates(subset=['漏洞名称', '服务器IP'],inplace=True)

	# print(type(_f))
	grouped = _f.groupby('服务器IP')
	with pandas.ExcelWriter('sub_sheet.xlsx') as writer:
		for name,group in grouped:
			print(name)
			group.to_excel(writer, sheet_name=name)

make_sub_sheet()
make_main_sheet()