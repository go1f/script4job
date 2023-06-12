#coding=utf-8
from bs4 import BeautifulSoup
import html5lib
import xlwt
import glob
import pandas

def get_cve_cvss(path):
	print("提取 "+path+"/index.html 扫描报告\r")
	file = open(path+"/index.html",encoding='utf-8')
	text = file.read()
	file.close()
	soup = BeautifulSoup(text,'html5lib')

	f = xlwt.Workbook()
	sheet1 = f.add_sheet('CVSS',cell_overwrite_ok=True)
	sheet1.write(0,0,"CVE编号")
	sheet1.write(0,1,"CVSS评分")

	i = 1
	for cvss in soup.find_all("th",string="CVSS评分",recursive=True):		
		score = cvss.find_next_sibling()
		cve = cvss.find_parent().find_parent().find("th",string="CVE编号").find_next_sibling()
		# print(cve.text + score.text)
		sheet1.write(i,0,cve.text)
		sheet1.write(i,1,float(score.text))
		i = i+1

	sheet1.write(i+1,0,'0')
	sheet1.write(i+1,1,"")
	f.save(path+'/cvss.xls')	
	return path+'/cvss.xls'


def concat_xls(path):
	host_all = pandas.DataFrame()	
	# print(glob.glob(path+'/*.*.xls'))
	for file in glob.glob(path+'/*.*.xls'):
	    df = pandas.read_excel(file,usecols="D:S",sheet_name="漏洞信息",index_col=0)
	    host_all = host_all.append(df)
	# print(host_all.columns)
	host_all.drop_duplicates(inplace=True)
	print("合并 "+path+" 文件夹，共"+str(host_all.shape)+"组记录\r")
	host_all.to_excel(path+"/hosts.xls")
	return path+"/hosts.xls"


report = pandas.DataFrame()
for _dir_xls in glob.glob("*大鹏*xls"):
	# # 读取CVSS评分，返回生成文件路径
	# _dir_html = _dir_xls.replace("xls","html")
	# cvss = get_cve_cvss(_dir_html)

	# 合并主机扫描表，返回生成文件路径
	hosts = concat_xls(_dir_xls)

	# 读取漏洞列表
	_f = pandas.read_excel(_dir_xls+"/index.xls",sheet_name="漏洞信息",usecols="C,D,F,K",skiprows=1)
	_f.columns=['威胁度','漏洞名称',"应用分类","影响资产"]

	# # 整合CVSS评分
	# _cvss = pandas.read_excel(cvss)
	# _f = pandas.merge(_f,_cvss,on=['CVE编号'],how='left')

	# 整合更多漏洞详情
	_hosts = pandas.read_excel(hosts,usecols="A,O,P")
	_hosts.rename(columns={'详细描述':'漏洞说明','解决办法':'加固建议'}, inplace = True)
	_f = pandas.merge(_f,_hosts,on=['漏洞名称'],how='left')

	# 生成报告
	print("已生成 "+_dir_xls+"/子报告.xls !!!\r\n\r\n")
	_f.to_excel(_dir_xls+"/子报告.xls")
	# 整合报告到大区
	report = report.append(_f)

print("合并所有子报告（拼接漏洞主机IP列）\r\n")
ips = report.groupby(by='漏洞名称').apply(lambda x:' '.join(x['影响资产']))
report.drop_duplicates('漏洞名称',inplace=True)
report = report.drop(columns=["影响资产"])
report = pandas.merge(report,ips.rename('影响资产'),how='left',on='漏洞名称')
report = report[['应用分类','漏洞名称','威胁度','漏洞说明','加固建议','影响资产']]
report.to_excel("主机扫描-漏洞报告.xls")

print("主机扫描-漏洞报告-初版出炉!!!\r\n")
