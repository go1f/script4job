
#coding=utf-8
from bs4 import BeautifulSoup
import html5lib
import xlwt
import glob

def get_cve_cvss(path):
	f = xlwt.Workbook()
	sheet1 = f.add_sheet('CVSS',cell_overwrite_ok=True)
	row0 = ["CVE编号","CVSS评分"]
	sheet1.write(0,0,row0[0])
	sheet1.write(0,1,row0[1])
	file = open(path+"/index.html",encoding='utf-8')
	text = file.read()
	file.close()
	soup = BeautifulSoup(text,'html5lib')
	# file = open("praser.html","w",encoding='utf-8')
	# file.write(soup)
	# print(soup)
	i = 1
	for cvss in soup.find_all("th",string="CVSS评分",recursive=True):
		# print(vuln)
		score = cvss.find_next_sibling()
		print(score.text)
		cve = cvss.find_parent().find_parent().find("th",string="CVE编号").find_next_sibling()
		print(cve.text)

		sheet1.write(i,0,cve.text)
		sheet1.write(i,1,float(score.text))
		i=i+1

	sheet1.write(i,0,"")
	sheet1.write(i,1,"")
	sheet1.write(i+1,0,'0')
	sheet1.write(i+1,1,"")
	f.save(path+'/cvss.xls')
	
	return path+'/cvss.xls'

